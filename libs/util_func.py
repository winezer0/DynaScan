#!/usr/bin/env python
# encoding: utf-8


# 判断列表内的字符串是否某个字符串内 # 如果列表为空,就返回default值
import random
import re

from libs.lib_log_print.logger_printer import output

# 列表中的任一元素是否在字符串内
from libs.lib_url_analysis.url_tools import get_base_url, get_url_ext_urlsplit


# 获得随机字符串
def get_random_str(length=12, has_num=True, has_capital=True, has_symbols=False, has_dot=False, with_slash=False):
    base_str = 'abcdefghigklmnopqrstuvwxyz'
    if has_num:
        base_str += '0123456789'
    if has_capital:
        base_str += 'ABCDEFGHIGKLMNOPQRSTUVWXYZ'
    if has_symbols:
        base_str += '~!@#$%^&*()_+-=><'

    random_str = ''
    for i in range(0, length - 1):
        if has_dot and i == length - 5:
            random_str += '.'
        else:
            random_str += base_str[random.randint(0, len(base_str) - 1)]
    if with_slash:
        random_str = '/' + random_str
    return random_str


# 移除字典内没有值、或值为'()'的键
def remove_dict_none_value_key(dict_, bracket=True):
    """
    移除字典内没有值、或 值为'()'的键
    bracket 是否移除值为'()'括号的键
    """
    for key in list(dict_.keys()):
        if not dict_.get(key) or dict_.get(key) is None:
            del dict_[key]
        elif bracket and dict_.get(key) == '()':
            del dict_[key]
    return dict_


# 分析 多个 字典列表 的 每个键的值是否相同, 并且不为默认值或空值
def analysis_dict_same_keys(result_dict_list, default_value_dict={}):
    same_key_value_dict = {}
    # 对结果字典的每个键做对比
    for key in list(result_dict_list[0].keys()):
        value_list = [value_dict[key] for value_dict in result_dict_list]
        # all() 是 Python 的内置函数之一，用于判断可迭代对象中的所有元素是否都为 True
        if all(value == value_list[0] for value in value_list):
            value = value_list[0]
            if key in list(default_value_dict.keys()):
                if value not in default_value_dict[key]:
                    output(f"[*] 所有字典的 [{key}] 值 [{value}] 相等 且不为默认或空值 [{default_value_dict[key]}]")
                    same_key_value_dict[key] = value
                else:
                    output(f"[-] 所有字典的 [{key}] 值 [{value}] 相等 但是默认或空值 [{default_value_dict[key]}]", level="debug")
            else:
                output(f"[!] 存在未预期的键{key},该键不在默认值字典[{list(default_value_dict.keys())}]内!!!", level="error")
    return same_key_value_dict


# URL转原始规则（做反向变量替换）
def url_to_raw_rule_classify(hit_url_list,
                             reverse_replace_dict_list,
                             hit_ext_file,
                             hit_direct_file,
                             hit_folder_file,
                             hit_files_file
                             ):
    hit_classify = {hit_ext_file: [],
                    hit_direct_file: [],
                    hit_folder_file: [],
                    hit_files_file: []}

    for url_str in hit_url_list:
        # 提取路径
        url_path = url_str.split(get_base_url(url_str), 1)[-1]  # /config.inc.php
        print(f'替换因变量值前:{url_path}')
        # 循环替换因变量值为%%键%%
        # print(depend_var_replace_dict)
        # {'%%DOMAIN%%': ['baidu', 'www_baidu_com', 'www.baidu.com', 'baidu.com', 'baidu_com']}
        for reverse_replace_dict in reverse_replace_dict_list:
            for key, value in reverse_replace_dict.items():
                url_path = re.sub(list_to_re_str(value), key, url_path, count=0)
        print(f'替换因变量值后:{url_path}')

        # 提取URL中的后缀
        url_ext = get_url_ext_urlsplit(url_str)
        # 如果URL中确实存在后缀
        if url_ext and url_ext.strip():
            hit_classify[hit_ext_file].append(url_ext)

        if url_path.strip('/'):
            hit_classify[hit_direct_file].append(url_path)

        folders_path = '/' + url_path.rsplit("/", 1)[0].rsplit("/", 1)[-1]
        if folders_path.strip('/'):
            hit_classify[hit_folder_file].append(folders_path)

        file_path = '/' + url_path.rsplit("/", 1)[-1]
        if file_path.strip('/'):
            hit_classify[hit_files_file].append(file_path)

    return hit_classify


# 将URL转换为原始规则
def list_to_re_str(replace_list, bracket=True):
    """
    将后缀字典列表转为一个正则替换规则字符串
    replace_list: 列表，如 ['.ccc', '.bbb']
    bracket: 是否给正则结果添加括号
    返回值: 一个正则表达式模式字符串，如 '(\\.ccc|\\.bbb)'
    """
    if replace_list:
        # 使用列表推导式和re.escape()自动转义为正则表达式中的文字字符
        regexp = '|'.join(re.escape(item) for item in replace_list)
    else:
        regexp = ""

    if bracket:
        replace_str = f'({regexp})'
    else:
        replace_str = f'{regexp}'

    return replace_str
