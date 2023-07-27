#!/usr/bin/env python
# encoding: utf-8


# 判断列表内的元素是否存在有包含在字符串内的
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