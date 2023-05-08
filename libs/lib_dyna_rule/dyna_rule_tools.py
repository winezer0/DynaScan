#!/usr/bin/env python
# encoding: utf-8

import itertools

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


# 冻结(账号-密码)集合列表, 将集合列表转为字符串列表
def frozen_tuple_list(tuple_list, link_symbol="<-->"):
    unique_lst = []
    for str1, str2 in tuple_list:
        unique_lst.append(f"{str1}{link_symbol}{str2}")
    return unique_lst


# 解冻(账号-密码)字符串列表, 将字符串列表转为元组列表
def unfrozen_tuple_list(str_list, link_symbol="<-->"):
    tuple_list = []
    for str_ in str_list:
        tuple_list.append(tuple(str_.split(link_symbol, 1)))
    return tuple_list


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
    tuple_list = []
    for str_ in str_list:
        tuple_list.append(tuple(str_.split(link_symbol)))
    return tuple_list


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


# 得到{"路径”:频率}字典中频率大于指定值的列表
def get_key_list_with_frequency(frequency_dict, frequency_min):
    if frequency_dict is None:
        frequency_dict = {}
    frequency_list = []
    for key, value in frequency_dict.items():
        if frequency_min <= value:
            frequency_list.append(key)
    return frequency_list


# 去除已经爆破过的元素
def reduce_str_str_tuple_list(str_str_tuple_list, history_tuple_list, str_link_symbol):
    """去除已经爆破过的元素"""
    if str_str_tuple_list and history_tuple_list:
        # 去重 user_name_pass_pair_list 中 被  history_user_pass_tuple_list包含的元素
        history_tuple_list = frozen_tuple_list(history_tuple_list, link_symbol=str_link_symbol)
        str_str_tuple_list = frozen_tuple_list(str_str_tuple_list, link_symbol=str_link_symbol)
        str_str_tuple_list = list(set(str_str_tuple_list) - set(history_tuple_list))
        str_str_tuple_list = unfrozen_tuple_list(str_str_tuple_list, link_symbol=str_link_symbol)
    return str_str_tuple_list
