#!/usr/bin/env python
# encoding: utf-8


def frozen_collects(tuple_list, link_symbol="<-->"):
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


def unfrozen_collects(str_list, link_symbol="<-->"):
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


def de_dup_collects(collect_list):
    """
    # 去重(不定长)集合列表
    :param collect_list:
    :return:
    """
    unique_lst = frozen_collects(collect_list, link_symbol="<-->")
    if unique_lst:
        unique_lst = list(set(unique_lst))
    collect_list = unfrozen_collects(unique_lst, link_symbol="<-->")
    return collect_list


def collects_subtract(reduced_collects, reduce_collects, link_symbol):
    """
    两个(不定长)集合相减
    :param reduced_collects:
    :param reduce_collects:
    :param link_symbol:
    :return:
    """
    if reduced_collects and reduce_collects:
        # 去重 user_name_pass_pair_list 中 被  history_user_pass_tuple_list包含的元素
        reduce_collects = frozen_collects(reduce_collects, link_symbol=link_symbol)
        reduced_collects = frozen_collects(reduced_collects, link_symbol=link_symbol)
        collects = list(set(reduced_collects) - set(reduce_collects))
        collects = unfrozen_collects(collects, link_symbol=link_symbol)
        return collects
    return reduced_collects


def list_ele_in_str(list_=None, str_=None, default=False):
    # 判断列表内的元素是否存在有包含在字符串内的
    if not list_:
        flag = default
    else:
        # flag = False
        # for ele in list_:
        #     if ele in str_:
        #         flag = True
        #         break
        # 在 lists为空列表时，any(key in string for key in lists) 会返回 False。
        flag = any(key in str(str_) for key in list_)
    return flag
