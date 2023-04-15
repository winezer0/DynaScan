#!/usr/bin/env python
# encoding: utf-8

import re
from urllib.parse import urlparse

from tldextract import extract

from libs.lib_log_print.logger_printer import output, LOG_ERROR
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
        host_port = str(host_port).replace(":", "_")
    return host_port


# 获取URL中的目录单词
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
                    path_words_list.append(str(path_var).replace(key, sysbol))
    if path_words_list:
        path_words_list = list(set(path_words_list))

    # 如果开启删除非路径字符开关
    if not_allowed_symbol:
        tmp_words_list = []
        for word in path_words_list:
            if not list_ele_in_str(not_allowed_symbol, word):
                tmp_words_list.append(word)
        path_words_list = tmp_words_list

    return path_words_list


# 获取基于域名的单词
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
                        new_domain_val = str(domain_val).replace(old_symbol, symbol)
                        tmp_list.append(new_domain_val)
            real_domain_val_list = tmp_list

        # 如果存在出现不允许的字符,就忽略该条
        if not_allowed_symbol:
            tmp_list = []
            for domain_val in real_domain_val_list:
                if not list_ele_in_str(not_allowed_symbol, domain_val, default=False):
                    tmp_list.append(domain_val)
            real_domain_val_list = tmp_list

        if real_domain_val_list:
            real_domain_val_list = list(set(real_domain_val_list))
    except Exception as e:
        output(f"[!] Get Base Domain Occur UnKnow Error: {e} !!!", level=LOG_ERROR)
    finally:
        return real_domain_val_list


# 从URL中提取无参数无目录的URL
def get_base_url(url):
    netloc = urlparse(url).netloc
    if netloc:
        split_url = url.split(netloc)
        baseurl = '%s%s' % (split_url[0], netloc)
        return baseurl
