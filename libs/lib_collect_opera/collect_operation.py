#!/usr/bin/env python
# encoding: utf-8

import itertools


def frozen_tuple_list(tuple_list, link_symbol="<-->"):
    """
    # 冻结(账号-密码)集合列表, 将集合列表转为字符串列表
    :param tuple_list:
    :param link_symbol:
    :return:
    """
    unique_lst = []
    for str1, str2 in tuple_list:
        unique_lst.append(f"{str1}{link_symbol}{str2}")
    return unique_lst


def unfrozen_tuple_list(str_list, link_symbol="<-->"):
    """
    # 解冻(账号-密码)字符串列表, 将字符串列表转为元组列表
    :param str_list:
    :param link_symbol:
    :return:
    """
    tuple_list = []
    for str_ in str_list:
        tuple_list.append(tuple(str_.split(link_symbol, 1)))
    return tuple_list


def de_duplicate_tuple_list(tuple_list):
    """
    # 去重(账号-密码)元组列表  PS:列表元素如果是元组也可以直接set去重
    :param tuple_list:
    :return:
    """
    # 将元组转换为元素不可变的类型，字符串列表
    # 然后使用set()函数将其转换为集合，
    # 最后再将集合转换回列表即可
    # frozenset(tuple) 会导致元组导致无序 # 不能用
    unique_lst = frozen_tuple_list(tuple_list, link_symbol="<-->")
    if unique_lst:
        unique_lst = list(set(unique_lst))
    tuple_list = unfrozen_tuple_list(unique_lst, link_symbol="<-->")
    return tuple_list


def frozen_collect_list(tuple_list, link_symbol="<-->"):
    """
    # 冻结(不定长)集合列表, 将集合列表转为字符串列表
    :param tuple_list:
    :param link_symbol:
    :return:
    """
    unique_lst = []
    for tpl in tuple_list:
        unique_lst.append(link_symbol.join(map(str, tpl)))
    return unique_lst


def unfrozen_collect_list(str_list, link_symbol="<-->"):
    """
    # 解冻(不定长)字符串列表, 将字符串列表转为元组列表
    :param str_list:
    :param link_symbol:
    :return:
    """
    tuple_list = []
    for str_ in str_list:
        tuple_list.append(tuple(str_.split(link_symbol)))
    return tuple_list


def de_duplicate_collect_list(collect_list):
    """
    # 去重(不定长)集合列表
    :param collect_list:
    :return:
    """
    unique_lst = frozen_collect_list(collect_list, link_symbol="<-->")
    if unique_lst:
        unique_lst = list(set(unique_lst))
    collect_list = unfrozen_collect_list(unique_lst, link_symbol="<-->")
    return collect_list


def cartesian_product_merging(name_list, pass_list):
    """
    # 笛卡尔积合并两个列表 结果格式[(a,b),(a,b)] 基于 itertools 生成
    :param name_list:
    :param pass_list:
    :return:
    """
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


def freeze_list_subtract(reduced_tuples, reduce_tuples, link_symbol):
    """
    冻结 元组 解冻并相减 （去除已经爆破过的元素 ）
    :param reduced_tuples:
    :param reduce_tuples:
    :param link_symbol:
    :return:
    """
    if reduced_tuples and reduce_tuples:
        # 去重 user_name_pass_pair_list 中 被  history_user_pass_tuple_list包含的元素
        reduce_tuples = frozen_tuple_list(reduce_tuples, link_symbol=link_symbol)
        reduced_tuples = frozen_tuple_list(reduced_tuples, link_symbol=link_symbol)
        reduced_tuples = list(set(reduced_tuples) - set(reduce_tuples))
        reduced_tuples = unfrozen_tuple_list(reduced_tuples, link_symbol=link_symbol)
    return reduced_tuples
