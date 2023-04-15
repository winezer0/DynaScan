#!/usr/bin/env python
# encoding: utf-8

import re
import urllib

from libs.lib_log_print.logger_printer import output, LOG_ERROR
from libs.lib_url_analysis.url_tools import get_url_ext_urlsplit


# 保留指定后缀的URL目标
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


# 移除指定后缀列表的内容
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
    if url_list:
        url_list = list(set(url_list))
    return url_list


# 对列表中的所有URL去除指定结尾字符并去重
def remove_url_end_symbol(url_list, remove_symbol_list=[]):
    if remove_symbol_list:
        remove_symbol = ''.join(remove_symbol_list)
        url_list = [url.rstrip(remove_symbol) for url in url_list]
        if url_list:
            url_list = list(set(url_list))

    return url_list


# 对列表中的所有URL小写处理并去重
def url_path_lowercase(url_list):
    url_list = [str(url).lower() for url in url_list]
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
                    output(f"[-] 元素[{path}] 基于 [{encoding}] 进行中文编码时,发生错误:{error}", level=LOG_ERROR)
    if new_path_list:
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
                output(f"[-] 元素 [{path}] 基于 [{encoding}] 进行URL编码时,发生错误:{error}", level=LOG_ERROR)
    new_path_list = list(set(new_path_list))
    return new_path_list
