#!/usr/bin/env python
# encoding: utf-8

# 获得随机字符串
import copy
import random
import re

from libs.lib_file_operate.file_write import write_line, write_title
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_DEBUG, LOG_ERROR
from libs.lib_requests.requests_const import *


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
                    output(f"[*] 所有DICT [{key}] 值 [{value}] 相等 且不为默认或空值 [{default_value_dict[key]}]")
                    same_key_value_dict[key] = value
                else:
                    output(f"[-] 所有DICT [{key}] 值 [{value}] 相等 但是默认或空值 [{default_value_dict[key]}]", level=LOG_DEBUG)
            else:
                output(f"[!] 存在未预期的键{key},该键不在默认值字典[{list(default_value_dict.keys())}]内!!!", level=LOG_ERROR)
    return same_key_value_dict


# 访问结果处理
def access_result_handle(result_dict_list,
                         dynamic_exclude_dict,
                         ignore_file,
                         result_file,
                         history_file,
                         access_fail_count,
                         exclude_status_list,
                         exclude_title_regexp,
                         max_error_num,
                         hit_saving_field=HTTP_CONST_SIGN):
    # 错误结果超出阈值
    should_stop_run = False

    # 访问失败的结果 # 就是除去URL和SING之外都是默认值
    access_fail_resp_dict = copy.copy(HTTP_DEFAULT_RESP_DICT)

    # 本次扫描的所有命中结果 默认保存的是 请求响应的 CONST_SIGN 属性
    hit_result_list = []

    # 响应结果处理
    for access_resp_dict in result_dict_list:
        # 结果格式
        result_format = "\"%s\"," * len(access_resp_dict.keys()) + "\n"

        # 写入历史爆破记录文件 CONST_SIGN == URL
        # history_file_open = open(history_file, "a+", encoding="utf-8", buffering=1)
        # history_file_open.write(f"{access_resp_dict[CONST_SIGN]}\n")
        write_line(history_file, f"{access_resp_dict[HTTP_CONST_SIGN]}", encoding="utf-8", new_line=True, mode="a+")

        # 按照指定的顺序获取 dict 的 values
        key_order_list = list(access_resp_dict.keys())
        key_order_list.sort()  # 按字母排序
        access_resp_values = tuple([access_resp_dict[key] for key in key_order_list])

        # 当前请求的标记
        resp_status = access_resp_dict[HTTP_RESP_STATUS]
        resp_text_title = access_resp_dict[HTTP_RESP_TEXT_TITLE]
        # 当前需要保存和显示的字段
        saving_field = access_resp_dict[hit_saving_field]

        # 过滤结果 并分别写入不同的结果文件
        IGNORE_RESP = True  # 忽略响应结果
        if resp_status not in exclude_status_list and \
                not re.match(exclude_title_regexp, resp_text_title, re.IGNORECASE):
            # 过滤结果 并分别写入不同的结果文件
            for filter_key in list(dynamic_exclude_dict.keys()):
                filter_value = dynamic_exclude_dict[filter_key]  # 被排除的值
                access_resp_value = access_resp_dict[filter_key]
                ignore_value_list = HTTP_FILTER_VALUE_DICT[filter_key]

                if access_resp_value != filter_value and access_resp_value not in ignore_value_list:
                    # 存在和排除关键字不同的项, 并且 这个值不是被忽略的值时 写入结果文件
                    IGNORE_RESP = False
                    break

        if IGNORE_RESP:
            # 写入结果表头
            write_title(ignore_file, result_format % tuple(key_order_list), encoding="utf-8", new_line=True, mode="a+")
            write_line(ignore_file, result_format % access_resp_values, encoding="utf-8", new_line=True, mode="a+")
            output(f"[-] 忽略结果 [{saving_field}]", level=LOG_DEBUG)
        else:
            # 写入结果表头
            write_title(result_file, result_format % tuple(key_order_list), encoding="utf-8", new_line=True, mode="a+")
            write_line(result_file, result_format % access_resp_values, encoding="utf-8", new_line=True, mode="a+")
            output(f"[+] 可能存在 [{saving_field}]", level=LOG_INFO)
            # 加入到命中结果列表
            hit_result_list.append(saving_field)

        # 判断请求是否错误（排除url和const_sign）
        access_fail_resp_dict[HTTP_CONST_SIGN] = access_resp_dict[HTTP_CONST_SIGN]
        access_fail_resp_dict[HTTP_REQ_URL] = access_resp_dict[HTTP_REQ_URL]
        # 字典可以直接使用 == 运算符进行比较，要求 字典中的键必须是可哈希的（即不可变类型）
        if access_resp_dict == access_fail_resp_dict:
            access_fail_count += 1

        # 取消继续访问进程 错误太多 或者 已经爆破成功
        if isinstance(max_error_num, int) and access_fail_count >= max_error_num:
            output(f"[*] 错误数量超过阈值 取消访问任务!!!", level=LOG_ERROR)
            should_stop_run = True

    return should_stop_run, hit_result_list
