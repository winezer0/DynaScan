#!/usr/bin/env python
# encoding: utf-8

import re
from urllib.parse import urlparse, urljoin
from tldextract import extract
from libs.lib_log_print.logger_printer import output, LOG_ERROR


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


def get_path_words(url, symbol_replace_dict=None, not_allowed_symbol=None):
    # 获取URL目录中的单词
    if not_allowed_symbol is None:
        not_allowed_symbol = [':']

    if symbol_replace_dict is None:
        symbol_replace_dict = {}

    # 拆分长URL为多个URL目录
    parser_url = urlparse(urljoin(url, "./"))
    path_words_list = [dirs for dirs in parser_url.path.split('/') if dirs.strip()]

    # 对所有结果再进行一次替换和添加
    for path_var in path_words_list:
        for key, value in symbol_replace_dict.items():
            for symbol in value:
                if key in path_var:
                    path_words_list.append(str(path_var).replace(key, symbol))

    if path_words_list:
        path_words_list = [i for i in path_words_list if i and str(i).strip()]
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
            # 去除''的域名单词
            real_domain_val_list = [i for i in real_domain_val_list if i and str(i).strip()]
            # 去重
            real_domain_val_list = list(set(real_domain_val_list))
    except Exception as e:
        output(f"[!] Get Base Domain Occur UnKnow Error: {e} !!!", level=LOG_ERROR)
    finally:
        return real_domain_val_list


def split_path_to_words(path):
    # 切割path路径为多个单词
    words = [dirs for dirs in path.split('/') if dirs.strip()]
    return words


