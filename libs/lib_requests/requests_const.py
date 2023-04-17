#!/usr/bin/env python
# encoding: utf-8

############################################################
# 响应需要的内容
HTTP_CONST_SIGN = "HTTP_CONST_SIGN"
HTTP_REQ_URL = "HTTP_REQ_URL"

HTTP_RESP_STATUS = "HTTP_RESP_STATUS"
HTTP_RESP_REDIRECT_URL = "HTTP_RESP_REDIRECT_URL"
HTTP_RESP_TEXT_HASH = "HTTP_RESP_TEXT_HASH"
HTTP_RESP_TEXT_TITLE = "HTTP_RESP_TEXT_TITLE"
HTTP_RESP_TEXT_SIZE = "HTTP_RESP_TEXT_SIZE"
HTTP_RESP_CONTENT_LENGTH = "HTTP_RESP_CONTENT_LENGTH"
HTTP_RESP_BYTES_HEAD = "HTTP_RESP_BYTES_HEAD"
############################################################
# 一些响应值的常量
HTTP_NONE = None
# 状态码常量
HTTP_STATUS_MINUS = -1
HTTP_STATUS_ZERO = 0
HTTP_STATUS_ONE = 1
# 重定向常量
HTTP_NULL_REDIRECT_URL = "HTTP_NULL_REDIRECT_URL"
HTTP_RAW_REDIRECT_URL = "HTTP_RAW_REDIRECT_URL"
# 响应内容常量
HTTP_BLANK_BYTES = "HTTP_BLANK_BYTES"
HTTP_NULL_BYTES = "HTTP_NULL_BYTES"
# 文本HASH常量
HTTP_IGNORE_TEXT_HASH = "HTTP_IGNORE_TEXT_HASH"
HTTP_NULL_TEXT_HASH = "HTTP_NULL_TEXT_HASH"
# 文本标题常量
HTTP_BLANK_TITLE = "HTTP_BLANK_TITLE"
HTTP_NULL_TITLE = "HTTP_NULL_TITLE"
HTTP_IGNORE_TITLE = "HTTP_IGNORE_TITLE"
############################################################
# 默认的响应字典,使用前被copy一份
HTTP_DEFAULT_RESP_DICT = {
    HTTP_REQ_URL: None,  # 请求的URL 必须在请求时填充
    HTTP_CONST_SIGN: None,  # 请求自定义的标记, 必须在请求时填充 原样返回
    HTTP_RESP_STATUS: HTTP_STATUS_MINUS,  # 响应状态码 赋值默认值
    HTTP_RESP_BYTES_HEAD: HTTP_NULL_BYTES,  # 响应头字节 赋值默认值
    HTTP_RESP_CONTENT_LENGTH: HTTP_STATUS_MINUS,  # 响应内容长度 赋值默认值
    HTTP_RESP_TEXT_SIZE: HTTP_STATUS_MINUS,  # 响应内容大小 赋值默认值
    HTTP_RESP_TEXT_TITLE: HTTP_NULL_TITLE,  # 响应文本标题 赋值默认值
    HTTP_RESP_TEXT_HASH: HTTP_NULL_TEXT_HASH,  # 响应文本HASH 赋值默认值
    HTTP_RESP_REDIRECT_URL: HTTP_NULL_REDIRECT_URL,  # 响应重定向URL 赋值默认值
}
############################################################
# 每个响应键的默认值或空值，在动态筛选时被忽略
HTTP_FILTER_VALUE_DICT = {
    HTTP_REQ_URL: [HTTP_NONE, ""],
    HTTP_CONST_SIGN: [HTTP_NONE, ""],
    HTTP_RESP_STATUS: [HTTP_STATUS_MINUS, HTTP_STATUS_ZERO, HTTP_STATUS_ONE],
    HTTP_RESP_BYTES_HEAD: [HTTP_NULL_BYTES, HTTP_BLANK_BYTES],
    HTTP_RESP_CONTENT_LENGTH: [HTTP_STATUS_MINUS, HTTP_STATUS_ZERO],
    HTTP_RESP_TEXT_TITLE: [HTTP_NULL_TITLE, HTTP_IGNORE_TITLE, HTTP_BLANK_TITLE],
    HTTP_RESP_TEXT_HASH: [HTTP_NULL_TEXT_HASH, HTTP_IGNORE_TEXT_HASH],
    HTTP_RESP_TEXT_SIZE: [HTTP_STATUS_MINUS, HTTP_STATUS_ZERO],
    HTTP_RESP_REDIRECT_URL: [HTTP_NULL_REDIRECT_URL, HTTP_RAW_REDIRECT_URL],
}
############################################################
# 记录由于代理服务器导致的协议判断不正确响应关键字
HTTP_ERROR_PAGE_KEY = ["burp suite"]
# burpsuite中可通过 [勾选抑制错误消息] 修复该问题
############################################################
# 随机HTTP头
HTTP_USER_AGENTS = [
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
