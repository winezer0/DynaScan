#!/usr/bin/env python
# encoding: utf-8

# 获得随机字符串
import random
import re

import chardet

from libs.lib_collect_opera.dict_operate import calc_dict_info_hash, copy_dict_remove_keys
from libs.lib_file_operate.file_write import write_line
from libs.lib_file_operate.rw_csv_file import write_dict_to_csv
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_DEBUG, LOG_ERROR
from libs.lib_requests.requests_const import *


def replace_content(content):
    # 替换 \n 为空格
    content = content.replace('\n', ' ')
    # 替换双引号为单引号
    content = content.replace('"', "'")
    # 替换 \ 为 /
    content = content.replace('\\', '/')
    return content


def content_encode(content):
    # 自动分析响应编码
    # 1、使用import chardet
    code_result = chardet.detect(content)  # 利用chardet来检测这个网页使用的是什么编码方式
    # output(content,code_result)  # 扫描到压缩包时,没法获取编码结果
    # 取code_result字典中encoding属性，如果取不到，那么就使用utf-8
    encoding = code_result.get("encoding", "utf-8")
    if not encoding:
        encoding = "utf-8"
    content = content.decode(encoding, 'replace')
    # 2、字符集编码，可以使用r.encoding='xxx'模式，然后再r.text()会根据设定的字符集进行转换后输出。
    # resp.encoding='utf-8'
    # output(resp.text)，

    # 3、请求后的响应response,先获取bytes 二进制类型数据，再指定encoding，也可
    # output(resp.content.decode(encoding="utf-8"))

    # 4、使用apparent_encoding可获取程序真实编码
    # resp.encoding = resp.apparent_encoding
    # content = req.content.decode(encoding, 'replace').encode('utf-8', 'replace')
    # content = resp.content.decode(resp.encoding, 'replace')  # 如果设置为replace，则会用?取代非法字符；
    return content


# 获得随机字符串
def random_str(length=12, num=False, char=False, capital=False, symbol=False, dot=False, slash=False):
    base_str = ""
    if char:
        base_str += 'abcdefghigklmnopqrstuvwxyz'
    if num:
        base_str += '0123456789'
    if capital:
        base_str += 'ABCDEFGHIGKLMNOPQRSTUVWXYZ'
    if symbol:
        base_str += '~!@#$%^&*()_+-=><'

    str_ = ''
    for i in range(0, length - 1):
        if dot and i == length - 5:
            str_ += '.'
        else:
            str_ += base_str[random.randint(0, len(base_str) - 1)]
    if slash:
        str_ = '/' + str_
    return str_


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
        return '127.0.0.1'


# 访问结果处理
def access_result_handle(result_dict_list,
                         dynamic_exclude_dict=None,
                         ignore_file="ignore.csv",
                         result_file="result.csv",
                         history_file="history.csv",
                         access_fail_count=0,
                         exclude_status_list=None,
                         exclude_title_regexp=None,
                         max_error_num=None,
                         history_field=HTTP_CONST_SIGN,
                         hit_saving_field=HTTP_CONST_SIGN,
                         hit_info_hashes=None):
    # 错误结果超出阈值
    should_stop_run = False

    # 本次扫描的所有命中结果 默认保存的是 请求响应的 CONST_SIGN 属性
    hit_result_list = []

    # 响应结果处理
    for access_resp_dict in result_dict_list:
        resp_dict_without_keys = copy_dict_remove_keys(access_resp_dict, FILTER_DYNA_IGNORE_KEYS)

        # 是否忽略响应结果
        IGNORE_RESP = False

        # # 访问失败的结果 不再需要, 通过响应状态码判断即可
        # # 1、除去URL和SING之外都是默认值
        # default_resp_without_keys = copy_dict_remove_keys(DEFAULT_HTTP_RESP_DICT, FILTER_DYNA_IGNORE_KEYS)
        # default_resp_without_keys[HTTP_RESP_STATUS] = RESP_STATUS_ERROR
        # # 判断请求是否默认（排除url和const_sign等） 所有的值都是默认值
        # if dict_eq_dict(default_resp_without_keys, resp_dict_without_keys):
        #     access_fail_count += 1
        #     IGNORE_RESP = True
        # # 2、除去URL和SING之外都是错误值
        # filter_resp_without_keys = copy_dict_remove_keys(FILTER_HTTP_VALUE_DICT, FILTER_DYNA_IGNORE_KEYS)
        # # 判断请求是否都是被过滤的 所有的值都在需要过滤的值中
        # if dict_in_dict(resp_dict_without_keys, filter_resp_without_keys):
        #     access_fail_count += 1
        #     IGNORE_RESP = True

        # 3、判断响应是否正常，不正常就是请求错误
        resp_status = access_resp_dict[HTTP_RESP_STATUS]
        if resp_status in FILTER_HTTP_VALUE_DICT[HTTP_RESP_STATUS]:
            access_fail_count += 1
            IGNORE_RESP = True

        # 排除状态码被匹配的情况
        if not IGNORE_RESP and exclude_status_list and resp_status in exclude_status_list:
            IGNORE_RESP = True

        # 排除标题被匹配的情况
        if not IGNORE_RESP and isinstance(exclude_title_regexp,str) \
                and re.match(exclude_title_regexp, access_resp_dict[HTTP_RESP_TITLE], re.IGNORECASE):
            IGNORE_RESP = True

        # 排除响应结果被匹配的情况
        if not IGNORE_RESP and dynamic_exclude_dict:
            for filter_key in list(dynamic_exclude_dict.keys()):
                resp_value = access_resp_dict[filter_key]  # 实际的值
                filter_value = dynamic_exclude_dict[filter_key]  # 被排除的值
                ignore_values = FILTER_HTTP_VALUE_DICT[filter_key]  # 应该被忽略的值
                if resp_value not in ignore_values and resp_value != filter_value:
                    # 存在和排除关键字不同的项, 并且 这个值不是被忽略的值时 写入结果文件
                    break
            else:
                IGNORE_RESP = True

        # 计算结果hash并判断是否是已命中结果
        if not IGNORE_RESP and isinstance(hit_info_hashes, list):
            hit_info_hash = calc_dict_info_hash(resp_dict_without_keys)
            if hit_info_hash in hit_info_hashes:
                output(f"[!] 忽略命中 [{hit_info_hash}] <--> {access_resp_dict[HTTP_REQ_TARGET]}", level=LOG_ERROR)
                IGNORE_RESP = True
            else:
                # output(f"[!] 保留命中 [{hit_info_hash}]", level=LOG_INFO)
                hit_info_hashes.append(hit_info_hash)

        # 当前需要保存和显示的字段
        saving_field = access_resp_dict[hit_saving_field]

        if IGNORE_RESP:
            write_dict_to_csv(ignore_file, access_resp_dict, mode="a+", encoding="utf-8", title_keys=None)
            output(f"[-] 忽略结果 [{saving_field}]", level=LOG_DEBUG)
        else:
            write_dict_to_csv(result_file, access_resp_dict, mode="a+", encoding="utf-8", title_keys=None)
            # 加入到命中结果列表
            hit_result_list.append(saving_field)
            output(f"[+] 可能存在 [{saving_field}]", level=LOG_INFO)

        # 取消继续访问进程 错误太多
        if isinstance(max_error_num, int) and access_fail_count >= max_error_num:
            output(f"[*] 错误数量超过阈值 取消访问任务!!!", level=LOG_ERROR)
            should_stop_run = True

        # 写入历史爆破记录文件
        write_line(history_file, f"{access_resp_dict[history_field]}", encoding="utf-8", new_line=True, mode="a+")
    return should_stop_run, hit_result_list
