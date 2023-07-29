#!/usr/bin/env python
# encoding: utf-8


# 判断列表内的元素是否存在有包含在字符串内的
import binascii
import copy
import hashlib
import json


def dict_dumps(dict_data={}):
    """
    将字典转为字符串
    :param dict_data:
    :return:
    """
    if isinstance(dict_data, dict):
        dict_data = json.dumps(dict_data, sort_keys=True)
    return dict_data


def dict_loads(json_data=""):
    """
    将字符串转为字典
    :param json_data:
    :return:
    """
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    return json_data


def search_key_in_list(data_dict={}, search_keys=[]):
    # 在参数字典的键中，查找是否有 存在于列表中的键
    for key, value in data_dict.items():
        if any(s in str(key).lower() for s in search_keys):
            return key
    return None


def sorted_data_dict(data_dict):
    # 快速将响应头字典固定为字符串
    sorted_items = sorted(data_dict.items())
    stores_string = ', '.join([f'{key}: {value}' for key, value in sorted_items])
    return stores_string


def calc_dict_info_hash(data_dict, crc_mode=True):
    # 计算响应结果的特征值

    # 对字典的键值对进行固定和排序
    str_sorted_items = data_dict if isinstance(data_dict, str) else sorted_data_dict(data_dict)

    if crc_mode:
        # 计算crc32的值,比md5更快
        mark_value = binascii.crc32(str_sorted_items.encode())
        mark_value = f"CRC32_{mark_value}"
    else:
        mark_value = hashlib.md5(str_sorted_items.encode()).hexdigest()
        mark_value = f"MD5_{mark_value}"
    return mark_value


def copy_dict_remove_keys(resp_dict, remove_keys):
    # 移除响应字典中和URL相关的选项, 仅保留响应部分
    # {'HTTP_REQ_TARGET': 'https://www.baidu.com/home.rar',  # 需要排除
    # 'HTTP_CONST_SIGN': 'https://www.baidu.com/home.rar',  # 需要排除
    # 'HTTP_RESP_REDIRECT': 'RESP_REDIRECT_ORIGIN'}   # 可选排除
    # 保留原始dict数据
    copy_resp_dict = copy.copy(resp_dict)
    for remove_key in remove_keys:
        # copy_resp_dict[remove_key] = ""  # 清空指定键的值
        copy_resp_dict.pop(remove_key, "")  # 删除指定键并返回其对应的值 # 删除不存在的键时，指定默认值，不会引发异常
    # output(f"[*] 新的字典键数量:{len(copy_resp_dict.keys())}, 原始字典键数量:{len(data_dict.keys())}", level=LOG_DEBUG)
    return copy_resp_dict