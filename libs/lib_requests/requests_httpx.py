import asyncio
from datetime import datetime
from urllib.parse import urlparse, urljoin

from httpx import AsyncClient

# 声明该方法为异步方法对象
from libs.lib_log_print.logger_printer import *
from libs.lib_requests.requests_const import *
from libs.lib_requests.requests_utils import random_str
from libs.lib_requests.response_handle import retry_action_check, analysis_resp_body, analysis_resp_header, \
    get_resp_redirect_url, show_requests_error, handle_common_error, get_resp_body_content_httpx


async def httpx_plus(req_url, **kwargs):
    # 参数的获取方式
    req_method = kwargs.get('req_method', 'GET')  # 获取 req_method 参数，默认值为 'GET'
    req_headers = kwargs.get('req_headers', None)
    req_data = kwargs.get('req_data', None)
    req_proxies = kwargs.get('req_proxies', None)
    req_timeout = kwargs.get('req_timeout', 10)
    verify_ssl = kwargs.get('verify_ssl', False)
    req_allow_redirects = kwargs.get('req_allow_redirects', False)
    req_stream = kwargs.get('req_stream', False)
    retry_times = kwargs.get('retry_times', 3)
    const_sign = kwargs.get('const_sign', None)
    add_host_header = kwargs.get('add_host_header', None)
    add_refer_header = kwargs.get('add_refer_header', None)
    ignore_encode_error = kwargs.get('ignore_encode_error', None)
    resp_headers_need = kwargs.get('resp_headers_need', True)
    resp_content_need = kwargs.get('resp_content_need', False)  # 获取 resp_content_need 参数，默认值为 False
    active_retry_dict = kwargs.get('active_retry_dict', None)
    thread_count = kwargs.get('thread_count', 100)

    # 通过创建信号量 semaphore ，限制同时执行的异步任务数量
    semaphore = asyncio.Semaphore(thread_count)
    async with semaphore:
        # const_sign # 设置本请求的标记
        const_sign = const_sign or datetime.now().strftime(f'%Y%m%d-%H%M%S-{random_str(length=5, num=True)}')
        # 设置默认请求头
        if not req_headers:
            req_headers = HTTP_HEADERS
        # 需要动态添加host字段
        if add_host_header:
            req_headers["Host"] = urlparse(req_url).netloc
        # 需要动态添加refer字段
        if add_refer_header:
            req_headers["Referer"] = urljoin(req_url, "./")

        # 设置需要接受的参数的默认值 #如果返回结果是默认值,说明程序异常没有获取到
        resp_status = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_STATUS]  # 响应状态码 # 完成
        resp_headers_opt = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_HEADERS_OPT]  # 响应实际头部 (OP=可选) # 完成
        resp_hash_headers = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_HEADERS_CRC]  # 响应实际头部 HASH标记 # 完成
        resp_length = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_LENGTH]  # 响应头中的CL头部 # 完成
        resp_content_opt = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_CONTENT_OPT]  # 响应实际内容 (OP=可选)
        resp_text_size = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_SIZE]  # 响应内容 大小标记
        resp_text_title = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_TITLE]  # 响应内容 网页标题
        resp_hash_content = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_CONTENT_CRC]  # 响应实际内容 HASH标记
        resp_redirect_url = DEFAULT_HTTP_RESP_DICT[HTTP_RESP_REDIRECT]  # 从响应中获取302的请求URL 应该有别的办法

        async with AsyncClient(proxies=req_proxies, verify=verify_ssl, follow_redirects=req_allow_redirects) as client:
            try:
                resp = await client.request(url=req_url, method=req_method, headers=req_headers, data=req_data,
                                            timeout=req_timeout)
                resp_status = resp.status_code
            except Exception as error:
                resp_status = RESP_STATUS_ERROR
                # 把常规错误的关键字加入列表内,列表为空时都作为非常规错误处理
                current_module = HTTP_RESP_STATUS
                module_common_error_list = ["without response", "Max retries exceeded",
                                            "Read timed out", "ConnectTimeoutError",
                                            "codec can't encode", "No host supplied",
                                            "Exceeded 30 redirects", 'WSAECONNRESET']
                show_requests_error(req_url, module_common_error_list, current_module, error)
                # 不进行错误重试的类型
                resp_status = handle_common_error(req_url, error, ignore_encode_error)
                if not resp_status:
                    # 如果是其他访问错误,就进程访问重试
                    if retry_times <= 0:
                        resp_status = RESP_STATUS_ERROR
                        output(f"[-] 当前目标 {req_url} 剩余重试次数为0, 返回错误状态!", level=LOG_ERROR)
                    else:
                        # 处理一种需要额外修改请求头的情况
                        if "Exceeded 30 redirects" in str(error):
                            req_headers = HTTP_HEADERS
                            output(f"[-] 当前目标 {req_url} 将自动进行请求头修改重试操作", level=LOG_ERROR)
                        output(f"[-] 当前目标 {req_url} 开始进行倒数第 {retry_times} 次重试, TIMEOUT * 1.5...", level=LOG_ERROR)
                        kwargs['retry_times'] = retry_times - 1
                        return await httpx_plus(req_url=req_url, **kwargs)
            else:
                # #############################################################
                # 当获取到响应结果时,获取响应关键匹配项目
                # #############################################################
                # 1 获取响应头相关的数据 resp_headers_opt | resp_hash_headers | resp_length # 流模式|普通模式都可以获取
                resp_headers_opt, resp_hash_headers, resp_length = analysis_resp_header(req_url, resp.headers,
                                                                                        resp_headers_need)
                # #############################################################
                # 2、获取响应内容相关的信息 # resp_content_opt | resp_text_title | resp_hash_content | resp_text_size
                encode_content = await get_resp_body_content_httpx(req_url, resp, resp_length, HTTP_MAXIMUM_READ, req_stream)
                text_info = analysis_resp_body(req_url, encode_content, resp_content_need)
                resp_content_opt, resp_hash_content, resp_text_title, resp_text_size = text_info
                #############################################################
                # 3 获取重定向后的URL 通过判断请求的URL是不是响应的URL #需要跟随重定向才行
                resp_redirect_url = get_resp_redirect_url(req_url, resp)
                #############################################################

            # 最终合并所有获取到的结果
            current_resp_dict = {
                HTTP_REQ_TARGET: req_url,  # 请求的URL
                HTTP_CONST_SIGN: const_sign,  # 请求的标记,自定义标记,原样返回

                HTTP_RESP_STATUS: resp_status,  # 响应状态码

                HTTP_RESP_HEADERS_CRC: resp_hash_headers,  # 响应头HASH
                HTTP_RESP_LENGTH: resp_length,  # 响应头中的长度

                HTTP_RESP_SIZE: resp_text_size,  # 响应内容大小
                HTTP_RESP_TITLE: resp_text_title,  # 响应文本标题

                HTTP_RESP_CONTENT_CRC: resp_hash_content,  # 响应内容HASH
                HTTP_RESP_REDIRECT: resp_redirect_url,  # 响应重定向URL

                HTTP_RESP_HEADERS_OPT: resp_headers_opt,  # 实际响应头
                HTTP_RESP_CONTENT_OPT: resp_content_opt,  # 实际响应内容
            }
            #############################################################
            #  active_retry_dict 主动重试动作 当满足条件时,进行主动请求重试
            if retry_times and retry_action_check(active_retry_dict, current_resp_dict):
                output(f"[!] 满足主动重试条件 {req_url} 开始倒数第 {retry_times} 次重试.")
                kwargs['retry_times'] = retry_times - 1
                return await httpx_plus(req_url=req_url, **kwargs)
            #############################################################
            output(f"[*] 当前目标 {req_url} 请求返回结果集合:{current_resp_dict}")

            return current_resp_dict


if __name__ == '__main__':
    from libs.lib_requests.requests_thread import async_httpx
    from libs.lib_file_operate.rw_csv_file import write_dict_to_csv

    urls = [
        'http://www.baidu.com/201902.iso',
        'http://www.baidu.com:7777/201804.rar',
        'http://www.baidu.com/%%path%%_4_.gz',
        'http://www.baidu.com/2013.7z',
        'http://www.baidu.com:7777/201706.z'
    ]

    action_dict = {
        HTTP_RESP_STATUS: [429, 500, 503, 504,404],  # 当状态码处于其中时,需要主动重试
        HTTP_RESP_TITLE: ["浏览器安全检查"],  # 当 标题  包含关键字时,需要重试
        HTTP_RESP_CONTENT_OPT: ["浏览器安全检查"],  # 当 请求体 包含关键字时,需要重试
        HTTP_RESP_HEADERS_OPT: ["浏览器安全检查"],  # 当 请求头  包含关键字时,需要重试
    }

    result_dict_list = async_httpx(urls, active_retry_dict=action_dict)
    write_dict_to_csv("tmp.csv", dict_data=result_dict_list, mode="w+", encoding="utf-8")

