#!/usr/bin/env python
# encoding: utf-8

# 定义一些常量名称
#########################
# 去重
DE_DUPLICATE = "DE_DUPLICATE"
# 长度过滤时忽略包含特定字符的字符串
IGNORE_SYMBOLS = "IGNORE_SYMBOLS"
# 长度过滤时忽略 空 字符操作
IGNORE_EMPTY = "IGNORE_EMPTY"  # 忽略空字符的处理
#########################
# 长度过滤
FILTER_MAX_LEN = "FILTER_MAX_LEN"
FILTER_MIN_LEN = "FILTER_MIN_LEN"
#########################
FILTER_LIST_OPTIONS = {
    DE_DUPLICATE: True,
    FILTER_MIN_LEN: 0,
    FILTER_MAX_LEN: 12,
    IGNORE_SYMBOLS: ["%"],
    IGNORE_EMPTY: True,
}
#########################
NAME_MAX_LEN = "NAME_MAX_LEN"  # 过滤账号密码元组
NAME_MIN_LEN = "NAME_MIN_LEN"  # 过滤账号密码元组
PASS_MAX_LEN = "PASS_MAX_LEN"  # 过滤账号密码元组
PASS_MIN_LEN = "PASS_MIN_LEN"  # 过滤账号密码元组
#########################
FILTER_TUPLE_OPTIONS = {
    DE_DUPLICATE: True,
    NAME_MAX_LEN: 12,
    NAME_MIN_LEN: 0,
    PASS_MAX_LEN: 12,
    PASS_MIN_LEN: 0,
    IGNORE_SYMBOLS: ["%"],
    IGNORE_EMPTY: True,
}