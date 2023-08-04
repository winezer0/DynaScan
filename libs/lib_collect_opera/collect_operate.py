#!/usr/bin/env python
# encoding: utf-8
import binascii
import hashlib


def frozen_collects(collects, link_symbol="<-->"):
    """
    # 冻结(不定长)集合列表, 将集合列表转为字符串列表
    :param collects:
    :param link_symbol:
    :return:
    """

    # 对于集合元素是 字符串|纯数字 的情况,不进行任何操作直接返回
    if isinstance(collects[0], str) or isinstance(collects[0], int):
        return collects

    unique_lst = []
    for collect in collects:
        unique_lst.append(link_symbol.join(map(str, collect)))
    return unique_lst


def unfrozen_collects(str_list, link_symbol="<-->"):
    """
    # 解冻(不定长)字符串列表, 将字符串列表转为元组列表
    :param str_list:
    :param link_symbol:
    :return:
    """
    if link_symbol not in str_list[0]:
        return str_list

    collects = []
    for str_ in str_list:
        if link_symbol in str_:
            collects.append(tuple(str_.split(link_symbol)))
        else:
            collects.append(str_)
    return collects


def de_dup_collects(collects, keep_order=False):
    """
    # 去重(不定长)集合列表
    :param collects: 任意集合
    :param keep_order: 是否保持原有顺序
    :return:
    """
    if not collects:
        return collects

    unique_lst = frozen_collects(collects, link_symbol="<-->")
    if keep_order:
        seen = set()
        unique_lst = [x for x in unique_lst if not (x in seen or seen.add(x))]
    else:
        unique_lst = list(set(unique_lst))
    collects = unfrozen_collects(unique_lst, link_symbol="<-->")
    return collects


def collects_subtract(collects_1, collects_2, link_symbol="<-->", keep_order=False):
    """
    两个(不定长)集合相减
    :param collects_1: 被减集合
    :param collects_2: 减去集合
    :param link_symbol: 链接符号
    :param keep_order: 需要保持原有顺序
    :return: 减法后的集合
    """

    collects_1 = de_dup_collects(collects_1, keep_order=False)

    if not collects_1 or not collects_2:
        return collects_1

    # 去重 collects_1 中 被  collects_2 包含的元素
    collects_1 = frozen_collects(collects_1, link_symbol=link_symbol)
    collects_2 = frozen_collects(collects_2, link_symbol=link_symbol)
    if keep_order:
        collects = [x for x in collects_1 if x not in collects_2]  # 保持原有顺序
    else:
        collects = list(set(collects_1) - set(collects_2))  # 不保持顺序

    return unfrozen_collects(collects, link_symbol=link_symbol) if collects else collects


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


def sorted_collect(data_dict):
    """
    将常见类型的集合数据转为固定的字符串
    :param data_dict:
    :return:
    """
    # 快速将响应头字典固定为字符串
    if isinstance(data_dict, str):
        return data_dict
    # 对于列表、元组、字典都需排序处理, 并且字典不能直接排序
    sorted_items = sorted(data_dict.items())
    if isinstance(data_dict,dict):
        stores_string = ', '.join([f'{key}: {value}' for key, value in sorted_items])
    else:
        stores_string = ', '.join(sorted_items)
    return stores_string


def calc_collect_hash(data_dict, crc_mode=True):
    """
    计算任意集合集合类型的字符串特征值
    :param data_dict:
    :param crc_mode:
    :return:
    """
    # 对字典的键值对进行固定和排序
    str_sorted_items = data_dict if isinstance(data_dict, str) else sorted_collect(data_dict)

    if crc_mode:
        # 计算crc32的值,比md5更快
        mark_value = binascii.crc32(str_sorted_items.encode())
        mark_value = f"CRC32_{mark_value}"
    else:
        mark_value = hashlib.md5(str_sorted_items.encode()).hexdigest()
        mark_value = f"MD5_{mark_value}"
    return mark_value