#!/usr/bin/env python
# encoding: utf-8

# 获取URL中的目录单词
import re
import urllib
from urllib.parse import urlparse
from tldextract import extract

from libs.lib_log_print.logger_printer import output
from libs.lib_url_analysis.url_split_parser import UrlSplitParser


def list_ele_in_str(list_=None, str_=None, default=True):
    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag


# 获取URL的脚本语言后缀
def get_url_ext_urlsplit(url):
    """
    url = 'http://www.baidu.com' # 没有后缀,返回None
    url = 'http://www.baidu.com/xxx' # 没有后缀, 返回None
    url = 'http://www.baidu.com/xxx.xxx'  # 有后缀,返回 xxx
    """
    parser_obj = UrlSplitParser(urlparse(url))
    extension = parser_obj.get_extension()
    return extension


# 从URL中获取HOST:PORT
def get_host_port(url, replace_symbol=False):
    """
    从URL中获取HOST头部
    output(get_host_port('http://www.baidu.com.cn:8080/111/222/3.aspx?p=123')) #www.baidu.com.cn:8080
    """
    path_obj = urlparse(url)
    host_port = path_obj.netloc
    if replace_symbol:
        host_port = host_port.replace(":", "_")
    return host_port


def get_segment_urls_urlsplit(url):
    """
    # 获取URL中的目录单词
    #UrlSplitParser(urlparse('http://www.baidu.com.cn:8080/xxxxx/xxx.aspx?p=123'))
    #output(parser_obj.get_paths()) # {'segment': ['/', '/xxxxx'], 'path': ['xxxxx', 'xxx']}
    """
    url_web_dirs = []
    parser_url = urlparse(url)
    parser_obj = UrlSplitParser(parser_url)
    segment_list = parser_obj.get_paths()['segment']
    for segment in segment_list:
        url_web_dirs.append(parser_obj.baseurl + segment)
    return url_web_dirs


# 获取URL目录单词和参数单词列表
def get_path_words_urlsplit(url, symbol_replace_dict=None, not_allowed_symbol=None):
    """
    # 获取URL目录单词和参数单词
    # UrlSplitParser(urlparse('http://www.baidu.com.cn:8080/xxxxx/xxx.aspx?p=123'))
    # output(parser_obj.get_paths()) # {'segment': ['/', '/xxxxx'], 'path': ['xxxxx', 'xxx']}

    UrlSplitParser中的其他方法
    #output(parser_obj.get_extension()) # aspx
    #output(parser_obj.get_urlfile()) # /xxxxx/xxx.aspx
    #output(parser_obj.get_dependent()) # ['p', 'xxx', 'baidu', 'www', '123', 'aspx', 'xxxxx']
    #output(parser_obj.get_domain_info()) # ['www', 'baidu', 'baidu'] ???
    """
    if not_allowed_symbol is None:
        not_allowed_symbol = [':']

    if symbol_replace_dict is None:
        symbol_replace_dict = {}
    parser_obj = UrlSplitParser(urlparse(url))
    path_words_list = parser_obj.get_paths()['path']
    # 对所有结果再进行一次替换和添加
    for path_var in path_words_list:
        for key, value in symbol_replace_dict.items():
            for sysbol in value:
                if key in path_var:
                    path_words_list.append(path_var.replace(key, sysbol))
    path_words_list = list(set(path_words_list))

    # 如果开启删除非路径字符开关
    if not_allowed_symbol:
        tmp_words_list = []
        for word in path_words_list:
            if not list_ele_in_str(not_allowed_symbol, word):
                tmp_words_list.append(word)
        path_words_list = tmp_words_list

    return path_words_list


def get_domain_words(url, ignore_ip_format=True, symbol_replace_dict={}, not_allowed_symbol=None):
    """
    从URL中获取域名相关的单词
    ('http://www.baidu.com/xxx.aspx?p=123'))  # ['www.baidu.com', 'baidu.com', 'baidu']
    ('http://www.baidu.com.cn:8080/xxx.aspx?p=123'))  # ['www.baidu.com.cn:8080', 'www.baidu.com.cn', 'baidu.com.cn', 'baidu']
    ('http://1.1.1.1:8080/xxx.aspx?p=123'))  # ['1.1.1.1:8080', '1.1.1.1', '1.1.1.1']

    print(get_domain_words('http://www.baidu.com.cn:8080/xxx.aspx?p=123'))  # ['www.baidu.com.cn:8080', 'www.baidu.com.cn', 'baidu.com.cn', 'baidu']
    print(get_domain_words('http://1.1.1.1:8080/xxx.aspx?p=123'))  # ['1.1.1.1:8080', '1.1.1.1', '1.1.1.1']
    ['www.baidu.com.cn:8080', 'www.baidu.com.cn', 'www.baidu.com.cn_8080', 'baidu.com.cn', 'baidu']
    ['1.1.1.1:8080', '1.1.1.1', '1.1.1.1_8080', '1.1.1.1']
    """
    real_domain_val_list = []

    try:
        # www.baidu.com.cn:8080
        domain_val_1 = urlparse(url).netloc

        # 获取IP格式的主机名
        re_ip_format = re.compile(r'^[\d.:]+$')
        re_search_ip_result = re_ip_format.search(domain_val_1)
        # 如果从域名中搜索到IP,就直接返回
        if ignore_ip_format and re_search_ip_result:
            return real_domain_val_list

        # baidu.com.cn
        domain_val_2 = extract(url).registered_domain
        # baidu
        domain_val_3 = extract(url).domain
        # www
        domain_val_4 = extract(url).subdomain

        real_domain_val_list = [domain_val_1, domain_val_2, domain_val_3, domain_val_4]

        # 根据字典动态替换 symbol_replace_dict = {":": ["_"],".": ["_"]}
        if symbol_replace_dict:
            tmp_list = []
            # 对所有结果再进行一次替换和添加
            for domain_val in real_domain_val_list:
                for old_symbol, new_symbol_list in symbol_replace_dict.items():
                    for symbol in new_symbol_list:
                        new_domain_val = domain_val.replace(old_symbol, symbol)
                        tmp_list.append(new_domain_val)
            real_domain_val_list = tmp_list

        # 如果存在出现不允许的字符,就忽略该条
        if not_allowed_symbol:
            tmp_list = []
            for domain_val in real_domain_val_list:
                if not list_ele_in_str(not_allowed_symbol, domain_val, default=False):
                    tmp_list.append(domain_val)
            real_domain_val_list = tmp_list

        real_domain_val_list = list(set(real_domain_val_list))
    except Exception as e:
        output(f"[!] Get Base Domain Occur UnKnow Error: {e} !!!", level="error")
    finally:
        return real_domain_val_list


# 移除指定后缀列表的内容
def specify_ext_store(url_list, ext_list):
    new_url_list_ = []
    if ext_list:
        try:
            for url in url_list:
                ext = get_url_ext_urlsplit(url)
                # 对于没有后缀的扩展也保留
                if not ext:
                    new_url_list_.append(url)
                # 如果URL后缀不在排除列表内,就保留这个URL,
                elif ext not in ext_list:
                    new_url_list_.append(url)
        except Exception as error:
            output(f"[-] 获取后缀进行列表匹配时发生错误!!! Error: {error}")
            new_url_list_ = url_list
    else:
        new_url_list_ = url_list
    return new_url_list_


# 保留指定后缀的URL目标
def specify_ext_delete(url_list, ext_list):
    new_url_list_ = []
    if ext_list:
        try:
            for url in url_list:
                ext = get_url_ext_urlsplit(url)
                # 对于没有后缀的扩展也保留
                if not ext:
                    new_url_list_.append(url)
                # 如果URL后缀在EXT列表内,也保留这个URL
                elif ext in ext_list:
                    new_url_list_.append(url)
        except Exception as error:
            output(f"[-] 获取后缀进行列表匹配时发生错误!!! Error: {error}")
            new_url_list_ = url_list
    else:
        new_url_list_ = url_list
    return new_url_list_


# 替换列表中所有元素的///为一个/
def replace_multi_slashes(url_list):
    url_list = [re.sub("/+", '/', url) for url in url_list]
    url_list = list(set(url_list))
    return url_list


# 对列表中的所有URL去除指定结尾字符并去重
def remove_url_end_symbol(url_list, remove_symbol_list=[]):
    if remove_symbol_list:
        remove_symbol = ''.join(remove_symbol_list)
        url_list = [url.rstrip(remove_symbol) for url in url_list]
        url_list = list(set(url_list))

    return url_list


# 对列表中的所有URL小写处理并去重
def url_path_lowercase(url_list):
    url_list = [url.lower() for url in url_list]
    return url_list


# 对列表中的元素进行中文判断和处理
def url_path_chinese_encode(path_list, encode_list=['utf-8']):
    """
    对列表中的元素进行中文判断和多个编码处理
    show_differ_path=True
    # new_path = urllib.parse.quote(path.encode("gb2312")) #解决/备份.zip读取问题失败
    # new_path = urllib.parse.quote(path.encode("utf-8")) #解决/备份.zip读取问题成功
    # new_path = urllib.parse.quote(path) #解决/备份.zip读取问题成功
    """
    zh_model = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
    new_path_list = []
    for path in path_list:
        new_path_list.append(path)
        match = zh_model.search(path)
        if match:
            for encoding in encode_list:
                try:
                    new_path = urllib.parse.quote(str(path).encode(encoding))  # 解决/备份.zip读取问题失败
                    if path != new_path:
                        new_path_list.append(new_path)
                except Exception as error:
                    output(f"[-] 元素[{path}] 基于 [{encoding}] 进行中文编码时,发生错误:{error}", level="error")
    new_path_list = list(set(new_path_list))
    return new_path_list


# 对列表中的所有元素进行URL编码
def url_path_url_encode(path_list, encode_list=['utf-8']):
    """
    # 对列表中的所有元素进行URL编码,
    # new_path = urllib.parse.quote(path.encode("gb2312")) #解决/备份.zip读取问题失败
    # new_path = urllib.parse.quote(path.encode("utf-8")) #解决/备份.zip读取问题成功
    # new_path = urllib.parse.quote(path) #解决/备份.zip读取问题成功
    """
    new_path_list = []
    for path in path_list:
        new_path_list.append(path)
        for encoding in encode_list:
            try:
                new_path = urllib.parse.quote(str(path).encode(encoding))  # 解决/备份.zip读取问题失败
                if path != new_path:
                    new_path_list.append(new_path)
            except Exception as error:
                output(f"[-] 元素 [{path}] 基于 [{encoding}] 进行URL编码时,发生错误:{error}", level="error")
    new_path_list = list(set(new_path_list))
    return new_path_list


# 从URL中提取无参数无目录的URL
def get_base_url(url):
    netloc = urlparse(url).netloc
    if netloc:
        split_url = url.split(netloc)
        baseurl = '%s%s' % (split_url[0], netloc)
        return baseurl
