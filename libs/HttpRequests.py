#!/usr/bin/env python
# encoding: utf-8
import re
import sys

sys.dont_write_bytecode = True  # 设置不生成pyc文件

import urllib

import chardet
import requests
import hashlib
from libs.ToolUtils import get_host_port

requests.packages.urllib3.disable_warnings()

# 输出时产生了序列问题,尝试枷锁解决,发现问题时由于python3 print的自动换行时线程不再安全导致
# import threading
# lock = threading.Lock()

# from colorama import init, Fore  # 需要添加有颜色的结果输出,便于区分错误结果
# init(autoreset=True) #使用logger进行输出,本文件没有导入logeer,从外部传参进入

from binascii import b2a_hex


# 判断列表内的元素是否存在有包含在字符串内的
def list_element_in_str(common_error_list=[], error_string=""):
    common_error_flag = False
    if len(common_error_list) > 0:
        for common_error in common_error_list:
            if common_error in error_string:
                common_error_flag = True
                break
    return common_error_flag


def handle_error(url, common_error_list, module, error, logger):
    # 把常规错误的关键字加入列表common_error_list内,列表为空时都作为非常规错误处理
    common_error_flag = list_element_in_str(common_error_list, str(error))
    if common_error_flag:
        logger.debug("[-] 当前目标 {} COMMON ERROR ON Acquire {}: {}".format(url, module, error))
    else:
        logger.error("[-] 当前目标 {} OTHERS ERROR ON Acquire {}: {}".format(url, module, error))


def requests_plus(method='get', url=None, cookies=None, timeout=1, stream=False, proxies=None, headers=None, verify=False, allow_redirects=False,
                  dynamic_host_header=True, dynamic_refer_header=True, retry_times=0, logger=None, encode='utf-8', encode_all_path=True):
    if not headers:
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Referer': '{}'.format(url),
            'Accept-Encoding': ''}

    # 需要动态添加host字段
    if dynamic_host_header: headers["host"] = get_host_port(url)
    # 需要动态添加refer字段
    if dynamic_refer_header: headers["refer"] = url
    # 设置需要接受的参数的默认值 #如果返回结果是默认值,说明程序异常没有获取到
    resp_status = -1  # 赋值默认值
    resp_bytes_head = "Null-Bytes"  # 赋值默认值
    resp_content_length = -1  # 赋值默认值
    resp_text = None  # 赋值默认值
    resp_text_size = -1  # 赋值默认值
    resp_text_title = "Null-Title"  # 赋值默认值
    resp_text_hash = "Null-Text-Hash"  # 赋值默认值
    resp_redirect_url = "Null-Redirect-Url"  # 赋值默认值
    try:
        resp = requests.request(method=method, url=url, cookies=cookies, timeout=timeout, stream=stream, proxies=proxies, headers=headers, verify=verify, allow_redirects=allow_redirects)
        resp_status = resp.status_code
    except Exception as error:
        # 当错误原因时一般需要重试的错误时,直接忽略输出,进行访问重试
        module = "resp or resp_status"
        # 把常规错误的关键字加入列表内,列表为空时都作为非常规错误处理
        common_error_list = ["retries", "Read timed out", "codec can't encode", "No host supplied", "Exceeded 30 redirects", 'WSAECONNRESET']
        handle_error(url, common_error_list, module, error, logger)
        # 如果是数据编码错误,需要进行判断处理
        if "codec can't encode" in str(error):
            # 如果是数据编码错误,就不再进行尝试 ,返回固定结果状态码
            # 'latin-1' codec can't encode characters in position 17-18: ordinal not in range(256)
            # 原则上需要将url变换为其他几种编码格式后进行访问,但是由于return只有一个结果,因此无法直接实现动态添加任务
            # 需要重构架构为队列模式才能实现,动态添加任务
            # 本次在返回结果后判断状态码是否为1,如果是的话,就再次进行访问测试,并且将新的结果加入原结果字典
            if encode_all_path:
                # 不需要重试的结果 设置resp_status标记为1,
                resp_status = 1
                result = (url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head, resp_redirect_url)
                logger.debug("[-] 当前目标 {} 中文数据编码错误,但是已经开启中文编码处理功能,忽略本次结果 {}!!!".format(url, result))
            else:
                # 需要手动访问重试的结果
                result = (url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head, resp_redirect_url)
                logger.error("[-] 当前目标 {} 中文数据编码错误,需要针对中文编码进行额外处理,返回固定结果 {}!!!".format(url, result))
        elif "No host supplied" in str(error):
            # 不需要重试的结果 设置resp_status标记为1,
            resp_status = 1
            result = (url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head, resp_redirect_url)
            logger.error("[-] 当前目标 {} 格式输入错误,忽略本次结果{}!!!".format(url, result))
        else:
            # 如果服务器没有响应,但是也有可能存在能访问的URL,因此不能简单以状态码判断结果
            # 如果是其他访问错误,就进程访问重试
            if retry_times > 0:
                if "Exceeded 30 redirects" in str(error):
                    headers = None
                    logger.error("[-] 当前目标 {} 即将修改请求头为默认头后进行重试!!!".format(url))

                logger.debug("[-] 当前目标 {} 开始进行倒数第 {} 次重试,(HTTP_TIMEOUT = HTTP_TIMEOUT * 1.5)...".format(url, retry_times))
                result = requests_plus(method=method, url=url, proxies=proxies, cookies=cookies, headers=headers, timeout=timeout * 1.5, verify=verify, allow_redirects=allow_redirects,
                                       dynamic_host_header=dynamic_host_header, dynamic_refer_header=dynamic_refer_header, retry_times=retry_times - 1, logger=logger, encode=encode)
            else:
                # 如果重试次数为小于0,返回固定结果-1
                result = (url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head, resp_redirect_url)
                logger.error("[-] 当前目标 {} 剩余重试次数为0,返回固定结果{},需要后续手动进行验证...".format(url, result))
    else:
        # 当获取到响应结果时,获取三个响应关键匹配项目
        #############################################################
        # 1、resp_bytes_head 获取响应内容的前十字节 # 需要流模式才能获取
        try:
            resp_bytes_head = b2a_hex(resp.raw.read(10)).decode()
            if resp_bytes_head.strip() == "":
                resp_bytes_head = "Blank-Bytes"
            else:
                pass
                # print("resp_bytes_head", resp_bytes_head) #需要流模式才能获取resp_bytes_head
        except Exception as error:
            # 当错误原因时一般需要重试的错误时,直接忽略输出,进行访问重试
            module = "resp_bytes_head"
            common_error_list = []  # 把常规错误的关键字加入列表内,列表为空时都作为非常规错误处理
            handle_error(url, common_error_list, module, error, logger)
        #############################################################
        # 2、resp_content_length 获取响应的content_length头部
        try:
            resp_content_length = int(str(resp.headers.get('Content-Length')))
        except Exception as error:
            module = "resp_content_length"
            common_error_list = ["invalid literal for int()"]  # 把常规错误的关键字加入列表内,列表为空时都作为非常规错误处理
            handle_error(url, common_error_list, module, error, logger)
        #############################################################
        # 3、resp_text_size 获取响应内容实际长度,如果响应长度过大就放弃读取,从resp_content_length进行读取
        if resp_content_length >= 1024000 * 5:
            # 结果文本长度太大,不进行实际获取
            resp_text_size = resp_content_length
        else:
            try:
                resp_text = resp.text

                resp_text_size = len(resp_text)
            except Exception as error:
                module = "resp_text_size"
                common_error_list = ["content-encoding: gzip", "Connection broken: IncompleteRead"]
                # 把常规错误的关键字加入列表内,列表为空时都作为非常规错误处理
                # Received response with content-encoding: gzip, but failed to decode it. # 返回gzip不解压报错
                # ('Connection broken: IncompleteRead(22 bytes read)', IncompleteRead(22 bytes read)) # 使用流模式导致不完全读取报错
                handle_error(url, common_error_list, module, error, logger)
        #############################################################
        # 4、resp_text_title 获取网页标题,如果resp_text_size获取到了就直接获取
        # 如果resp_text_size没有获取到,说明没有resp_text 不参考上级处理结果
        encode_content = ""
        try:
            if resp_content_length >= 1024000 * 5:
                # 如果返回值太大,就忽略获取结果
                resp_text_title = "Ignore-Title"
            else:
                # 解决响应解码问题
                # 0、使用import chardet
                encode_content = resp.content  # print(type(resp.content)) # bytes类型
                code_result = chardet.detect(encode_content)  # 利用chardet来检测这个网页使用的是什么编码方式
                # print(encode_content,code_result)  # 扫描到压缩包时,没法获取编码结果
                # 取code_result字典中encoding属性，如果取不到，那么就使用utf-8
                encoding = code_result.get("encoding", "utf-8")
                if not encoding: encoding = "utf-8"
                encode_content = encode_content.decode(encoding, 'replace')
                # 1、字符集编码，可以使用r.encoding='xxx'模式，然后再r.text()会根据设定的字符集进行转换后输出。
                # resp.encoding='utf-8'
                # print(resp.text)，

                # 2、请求后的响应response,先获取bytes 二进制类型数据，再指定encoding，也可
                # print(resp.content.decode(encoding="utf-8"))

                # 3、使用apparent_encoding可获取程序真实编码
                # resp.encoding = resp.apparent_encoding
                # encode_content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
                # encode_content = resp.content.decode(resp.encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
                re_find_result_list = re.findall(r"<title.*?>(.+?)</title>", encode_content)
                resp_text_title = resp_text_title = ",".join(re_find_result_list)
                # 解决所有系统下字符串无法编码输出的问题,比如windows下控制台gbk的情况下,不能gbk解码就是BUG
                # logger.error("当前控制台输出编码为:{}".format(sys.stdout.encoding))
                # 解决windows下韩文无法输出的问题,如果不能gbk解码就是window BUG
                # if sys.platform.lower().startswith('win'):
                try:
                    resp_text_title.encode(sys.stdout.encoding)
                except Exception as error:
                    resp_text_title = urllib.parse.quote(resp_text_title.encode('utf-8'))
                    logger.error("[!] 字符串使用当前控制台编码 {} 编码失败,自动转换为UTF-8型URL编码 {}, ERROR:{}".format(sys.stdout.encoding, resp_text_title, error))
                if resp_text_title.strip() == "": resp_text_title = "Blank-Title"
        except Exception as error:
            module = "resp_text_title"
            common_error_list = []  # 把常规错误的关键字加入列表内,列表为空时都作为非常规错误处理
            handle_error(url, common_error_list, module, error, logger)
        #############################################################
        # 5、resp_text_hash 获取网页内容hash
        # resp_text_title = "Null-Title"  # 赋值默认值
        # resp_text_hash = "Null-Text-Hash"  # 赋值默认值
        # 如果resp_text_title是空值,说明结果存在问题
        if resp_text_title != "Null-Title" and encode_content != "":
            try:
                if resp_content_length >= 1024000 * 5:
                    # 如果返回值太大,就忽略获取结果
                    resp_text_hash = "Ignore-Text-Hash"
                else:
                    resp_text_hash = hashlib.md5(resp.content).hexdigest()
            except Exception as error:
                module = "resp_text_hash"
                common_error_list = []  # 把常规错误的关键字加入列表内,列表为空时都作为非常规错误处理
                handle_error(url, common_error_list, module, error, logger)
        #############################################################
        # 6、resp_redirect_url 获取重定向后的URL
        try:
            if url.strip() == resp_redirect_url.strip():
                resp_redirect_url = "Raw-Redirect-Url"
            else:
                resp_redirect_url = resp.url.strip()
        except Exception as error:
            module = "resp_redirect_url"
            common_error_list = []  # 把常规错误的关键字加入列表内,列表为空时都作为非常规错误处理
            handle_error(url, common_error_list, module, error, logger)
        # 合并所有获取到的结果
        """
        # 获取编码后URL的真实URL 忽略本步骤,解码可能会导致报错 也没有必要获取
        # 如果开启了自动替换模式,这一步骤就需要关闭,否则会报错
        if not encode_all_path:
            # 如果没有开启编码所有路径的选项,就可以考虑单独对URL解码
            # 仅对没有编码的情况进行解码,如果GB2312编码了，但是UTF8解码会报错的。
            url = urllib.parse.unquote(url, encoding=encode)  # 解码为/备份.zip成功
        """
        result = (url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head, resp_redirect_url)
        logger.debug("[*] 当前目标 {} 请求返回结果集合:{}".format(url, result))
    return result


if __name__ == '__main__':
    target_url_path_list = ['http://www.baidu.com/201902.iso', 'http://www.baidu.com/%%path%%_4_.gz',
                            'http://www.baidu.com/2013.7z', 'http://www.baidu.com/201804.rar',
                            'http://www.baidu.com/201706.z']

    # 导入PY3多线程池模块
    from concurrent.futures import ThreadPoolExecutor, as_completed

    threads_count = 3  # 线程池线程数
    with ThreadPoolExecutor(max_workers=threads_count) as pool:
        all_task = []
        for url in target_url_path_list:
            # 把请求任务加入线程池
            task = pool.submit(requests_plus, url=url)
            all_task.append(task)
        # 输出线程返回的结果
        for future in as_completed(all_task):
            print(future, future.result())
