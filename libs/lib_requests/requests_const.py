#!/usr/bin/env python
# encoding: utf-8

############################################################

# 响应需要的内容
CONST_SIGN = "const_sign"
REQ_URL = "req_url"
RESP_REDIRECT_URL = "resp_redirect_url"
RESP_TEXT_HASH = "resp_text_hash"
RESP_TEXT_TITLE = "resp_text_title"
RESP_TEXT_SIZE = "resp_text_size"
RESP_CONTENT_LENGTH = "resp_content_length"
RESP_BYTES_HEAD = "resp_bytes_head"
RESP_STATUS = "resp_status"
############################################################
# 一些响应值的常量
NONE = None
RAW_REDIRECT_URL = "Raw-Redirect-Url"
NULL_REDIRECT_URL = "Null-Redirect-Url"
BLANK_BYTES = "Blank-Bytes"
NULL_BYTES = "Null-Bytes"
NUM_ZERO = 0
NUM_MINUS = -1
NUM_ONE = 1
IGNORE_TEXT_HASH = "Ignore-Text-Hash"
NULL_TEXT_HASH = "Null-Text-Hash"
BLANK_TITLE = "Blank-Title"
NULL_TITLE = "Null-Title"
IGNORE_TITLE = "Ignore-Title"
############################################################
# 默认的响应字典,使用前被copy一份
DEFAULT_RESP_DICT = {
    REQ_URL: None,  # 请求的URL 必须在请求时填充
    CONST_SIGN: None,  # 请求自定义的标记, 必须在请求时填充 原样返回
    RESP_STATUS: NUM_MINUS,  # 响应状态码 赋值默认值
    RESP_BYTES_HEAD: NULL_BYTES,  # 响应头字节 赋值默认值
    RESP_CONTENT_LENGTH: NUM_MINUS,  # 响应内容长度 赋值默认值
    RESP_TEXT_SIZE: NUM_MINUS,  # 响应内容大小 赋值默认值
    RESP_TEXT_TITLE: NULL_TITLE,  # 响应文本标题 赋值默认值
    RESP_TEXT_HASH: NULL_TEXT_HASH,  # 响应文本HASH 赋值默认值
    RESP_REDIRECT_URL: NULL_REDIRECT_URL,  # 响应重定向URL 赋值默认值
}
############################################################
# 每个响应键的默认值或控制，在动态筛选时被忽略
FILTER_MODULE_DEFAULT_VALUE_DICT = {
    REQ_URL: [NONE,""],
    CONST_SIGN: [NONE,""],
    RESP_STATUS: [NUM_MINUS, NUM_ZERO, NUM_ONE],
    RESP_BYTES_HEAD: [NULL_BYTES, BLANK_BYTES],
    RESP_CONTENT_LENGTH: [NUM_MINUS, NUM_ZERO],
    RESP_TEXT_TITLE: [NULL_TITLE, IGNORE_TITLE, BLANK_TITLE],
    RESP_TEXT_HASH: [NULL_TEXT_HASH, IGNORE_TEXT_HASH],
    RESP_TEXT_SIZE: [NUM_MINUS, NUM_ZERO],
    RESP_REDIRECT_URL: [NULL_REDIRECT_URL, RAW_REDIRECT_URL],
}
############################################################
# 记录由于代理服务器导致的协议判断不正确响应关键字
ERROR_PAGE_KEY = ["burp suite"]
# burpsuite中可通过 [勾选抑制错误消息] 修复该问题
############################################################