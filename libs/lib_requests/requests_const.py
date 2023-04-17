#!/usr/bin/env python
# encoding: utf-8

############################################################

# 响应需要的内容
CONST_SIGN = "CONST_SIGN"
REQ_URL = "REQ_URL"
RESP_REDIRECT_URL = "RESP_REDIRECT_URL"
RESP_TEXT_HASH = "RESP_TEXT_HASH"
RESP_TEXT_TITLE = "RESP_TEXT_TITLE"
RESP_TEXT_SIZE = "RESP_TEXT_SIZE"
RESP_CONTENT_LENGTH = "RESP_CONTENT_LENGTH"
RESP_BYTES_HEAD = "RESP_BYTES_HEAD"
RESP_STATUS = "RESP_STATUS"
############################################################
# 一些响应值的常量
NONE = None
# 状态码常量
NUM_MINUS = -1
NUM_ZERO = 0
NUM_ONE = 1
# 重定向常量
NULL_REDIRECT_URL = "NULL_REDIRECT_URL"
RAW_REDIRECT_URL = "RAW_REDIRECT_URL"
# 响应内容常量
BLANK_BYTES = "BLANK_BYTES"
NULL_BYTES = "NULL_BYTES"
# 文本HASH常量
IGNORE_TEXT_HASH = "IGNORE_TEXT_HASH"
NULL_TEXT_HASH = "NULL_TEXT_HASH"
# 文本标题常量
BLANK_TITLE = "BLANK_TITLE"
NULL_TITLE = "NULL_TITLE"
IGNORE_TITLE = "IGNORE_TITLE"
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
# 每个响应键的默认值或空值，在动态筛选时被忽略
FILTER_MODULE_DEFAULT_VALUE_DICT = {
    REQ_URL: [NONE, ""],
    CONST_SIGN: [NONE, ""],
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
# 随机HTTP头
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
############################################################
