#!/usr/bin/env python
# encoding: utf-8

import itertools

from libs.lib_rule_dict.base_rule_parser import base_rule_render_list
from libs.lib_rule_dict.rule_const import *


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


# 冻结(账号-密码)集合列表, 将集合列表转为字符串列表
def frozen_tuple_list(tuple_list, link_symbol="<-->"):
    unique_lst = []
    for str1, str2 in tuple_list:
        unique_lst.append(f"{str1}{link_symbol}{str2}")
    return unique_lst


# 解冻(账号-密码)字符串列表, 将字符串列表转为元组列表
def unfrozen_tuple_list(str_list, link_symbol="<-->"):
    new_tuple_list = []
    for str_str2 in str_list:
        new_tuple_list.append(str_str2.split(link_symbol, 1))
    return new_tuple_list


# 去重(账号-密码)元组列表  PS:列表元素如果是元组也可以直接set去重
def de_duplicate_tuple_list(tuple_list):
    # 将元组转换为元素不可变的类型，字符串列表
    # 然后使用set()函数将其转换为集合，
    # 最后再将集合转换回列表即可
    # frozenset(tuple) 会导致元组导致无序 # 不能用
    unique_lst = frozen_tuple_list(tuple_list, link_symbol="<-->")
    if unique_lst:
        unique_lst = list(set(unique_lst))
    tuple_list = unfrozen_tuple_list(unique_lst, link_symbol="<-->")
    return tuple_list


# 冻结(不定长)集合列表, 将集合列表转为字符串列表
def frozen_collect_list(tuple_list, link_symbol="<-->"):
    unique_lst = []
    for tpl in tuple_list:
        unique_lst.append(link_symbol.join(map(str, tpl)))
    return unique_lst


# 解冻(不定长)字符串列表, 将字符串列表转为元组列表
def unfrozen_collect_list(str_list, link_symbol="<-->"):
    new_tuple_list = []
    for str_str2 in str_list:
        new_tuple_list.append(str_str2.split(link_symbol))
    return new_tuple_list


# 去重(不定长)集合列表
def de_duplicate_collect_list(collect_list):
    unique_lst = frozen_collect_list(collect_list, link_symbol="<-->")
    if unique_lst:
        unique_lst = list(set(unique_lst))
    collect_list = unfrozen_collect_list(unique_lst, link_symbol="<-->")
    return collect_list


# 笛卡尔积合并两个列表 结果格式[(a,b),(a,b)]
def cartesian_product_merging(name_list, pass_list):
    # 笛卡尔积合并两个列表 结果格式[(a,b),(a,b)]
    # 基于 itertools 生成
    cartesian_product_list = list(itertools.product(name_list, pass_list))

    # # 基于循环生成
    # cartesian_product_list = []
    # for name_ in name_list:
    #     for pass_ in pass_list:
    #         cartesian_product_list.append((name_,pass_))

    # 去重元组列表结果
    # cartesian_product_list = list(set(cartesian_product_list))
    cartesian_product_list = de_duplicate_tuple_list(cartesian_product_list)
    return cartesian_product_list


# 对 替换规则字典中的 值列表 进行 动态规则解析
def dict_content_base_rule_render(var_dict):
    # 对 替换规则字典中的 值列表 进行 动态规则解析
    for var_name, value_list in var_dict.items():
        if value_list:
            # 解析列表中的每一个元素
            result_list, render_count, run_time = base_rule_render_list(value_list)
            var_dict[var_name] = result_list
    return var_dict


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


# 得到{"路径”:频率}字典中频率大于指定值的列表
def get_key_list_with_frequency(frequency_dict, frequency_min):
    if frequency_dict is None:
        frequency_dict = {}
    frequency_list = []
    for key, value in frequency_dict.items():
        if frequency_min <= value:
            frequency_list.append(key)
    return frequency_list


# 对(账号,密码)元组列表进行长度过滤
def filter_pair_tuples_by_length(tuple_list,
                                 name_min_len=3,
                                 name_max_len=16,
                                 pass_min_len=3,
                                 pass_max_len=16,
                                 ignore_empty=False,
                                 ignore_symbols=[]):
    """
    tuple_list 元组列表
    ele_index   元素在元组内的索引
    """
    # 处理max_len赋值错误的情况
    if name_max_len <= name_min_len:
        name_max_len = 99

    if pass_max_len <= pass_min_len:
        pass_max_len = 99

    # 使用列表推导式获取长度在6到16之间的元素
    new_tuple_list = []
    for tuple_ in tuple_list:
        name_ = tuple_[0]
        pass_ = tuple_[1]

        # 忽略对特定字符的处理
        if ignore_symbols and (list_ele_in_str(ignore_symbols, name_) or list_ele_in_str(ignore_symbols, pass_)):
            new_tuple_list.append(tuple_)
            continue

        # 忽略对空值的处理
        if ignore_empty and (len(name_) == 0 or len(pass_) == 0):
            new_tuple_list.append(tuple_)
            continue

        if (name_min_len <= len(name_) <= name_max_len) and (pass_min_len <= len(pass_) <= pass_max_len):
            new_tuple_list.append(tuple_)
    return new_tuple_list


# 对字符串列表进行长度过滤
def filter_string_list_by_length(string_list,
                                 min_len=3,
                                 max_len=16,
                                 ignore_empty=False,
                                 ignore_symbols=[]):
    # 处理max_len赋值错误的情况
    if max_len <= min_len:
        max_len = 99

    # 使用列表推导式获取长度在6到16之间的元素
    new_string_list = []
    for string in string_list:
        # 忽略对包含特定字符的处理
        if ignore_symbols and list_ele_in_str(ignore_symbols, string, default=False):
            new_string_list.append(string)
            continue

        # 忽略对空值的处理
        if ignore_empty and len(string) == 0:
            new_string_list.append(string)
            continue

        if min_len <= len(string) <= max_len:
            new_string_list.append(string)

    return new_string_list


# 对每次生成的字符串列表进行统一的格式化
def format_string_list(string_list=[], options_dict={}):
    # 最后再处理一次字符串列表
    if string_list:
        if options_dict[DE_DUPLICATE]:
            # 去重复
            string_list = list(set(string_list)) if string_list else []

        if options_dict[FILTER_MAX_LEN]:
            # 按长度筛选
            string_list = filter_string_list_by_length(string_list,
                                                       min_len=options_dict[FILTER_MIN_LEN],
                                                       max_len=options_dict[FILTER_MAX_LEN],
                                                       ignore_empty=options_dict[IGNORE_EMPTY],
                                                       ignore_symbols=options_dict[IGNORE_SYMBOLS]
                                                       )

        # 按格式筛选
    return string_list


# 对每次生成的(账号,密码)列表进行统一的格式化
def format_tuple_list(tuple_list=[], options_dict={}):
    # 最后再处理一次字符串列表
    if tuple_list:
        if options_dict[DE_DUPLICATE]:
            # 去重复
            tuple_list = de_duplicate_tuple_list(tuple_list)

        if options_dict[NAME_MAX_LEN]:
            # 按长度筛选
            tuple_list = filter_pair_tuples_by_length(tuple_list,
                                                      name_min_len=options_dict[NAME_MIN_LEN],
                                                      name_max_len=options_dict[NAME_MAX_LEN],
                                                      pass_min_len=options_dict[PASS_MIN_LEN],
                                                      pass_max_len=options_dict[PASS_MAX_LEN],
                                                      ignore_empty=options_dict[IGNORE_EMPTY],
                                                      ignore_symbol=options_dict[IGNORE_SYMBOLS])

    return tuple_list
