#!/usr/bin/env python
# encoding: utf-8

# 获得随机字符串
import random

from libs.lib_log_print.logger_printer import output


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


# 随机生成User-Agent
def random_useragent(user_agents, condition=False):
    if condition:
        return random.choice(user_agents)
    else:
        return user_agents[0]


# 随机X-Forwarded-For，动态IP
def random_x_forwarded_for(condition=False):
    if condition:
        return '%d.%d.%d.%d' % (random.randint(1, 254),
                                random.randint(1, 254),
                                random.randint(1, 254),
                                random.randint(1, 254))
    else:
        return '8.8.8.8'


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
