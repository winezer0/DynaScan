#!/usr/bin/env python
# encoding: utf-8

import itertools
import re

from libs.lib_dyna_rule.base_rule_parser import base_rule_render_list


# 判断列表内的元素是否存在有包含在字符串内的
def list_ele_in_str(list_=None, str_=None, default=False):
    if list_ is None:
        list_ = []

    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag


# 对 替换规则字典中的 值列表 进行 动态规则解析
def dict_content_base_rule_render(var_dict):
    # 对 替换规则字典中的 值列表 进行 动态规则解析
    for var_name, value_list in var_dict.items():
        if value_list:
            # 解析列表中的每一个元素
            result_list, render_count, run_time = base_rule_render_list(value_list)
            var_dict[var_name] = result_list
    return var_dict


# 得到{"路径”:频率}字典中频率大于指定值的列表
def get_key_list_with_freq(freq_dict, freq_min):
    if freq_dict is None:
        return []

    freq_list = []
    for key, value in freq_dict.items():
        if freq_min <= value:
            freq_list.append(key)
    return freq_list


# 将变量列表转换为正则表达式
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
