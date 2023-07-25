#!/usr/bin/env python
# encoding: utf-8

############################################################
# 需要返回的响应内容
HTTP_REQ_TARGET = "HTTP_REQ_TARGET"  # 用户输入的请求地址
HTTP_CONST_SIGN = "HTTP_CONST_SIGN"  # 用户输入的自定义标记

HTTP_RESP_STATUS = "HTTP_RESP_STATUS"  # 响应状态码

HTTP_RESP_LENGTH = "HTTP_RESP_LENGTH"  # 响应头中的CL头部
HTTP_RESP_HEADERS_CRC = "HTTP_RESP_HEADERS_CRC"  # 响应实际头部 HASH标记
HTTP_RESP_HEADERS_OPT = "HTTP_RESP_HEADERS_OPT"  # 响应实际头部 (OP=可选)

HTTP_RESP_REDIRECT = "HTTP_RESP_REDIRECT"  # 响应中的请求URL,302时不一定相同

HTTP_RESP_CONTENT_CRC = "HTTP_RESP_CONTENT_CRC"  # 响应实际内容 HASH标记
HTTP_RESP_CONTENT_OPT = "HTTP_RESP_CONTENT_OPT"  # 响应实际内容 (OP=可选)
HTTP_RESP_SIZE = "HTTP_RESP_SIZE"  # 响应内容标记 大小标记
HTTP_RESP_TITLE = "HTTP_RESP_TITLE"  # 响应文本的标题
############################################################
# 一些响应值的常量
HTTP_MAXIMUM_READ = 1024000  # 设置最大读取的响应内容(字数) 一般网页有150字X3000行
NONE = None
NULL = ""

# 状态码常量
RESP_STATUS_DEFAULT = "RESP_STATUS_DEFAULT"  # 0    # 没有任何操作时候的 默认值
RESP_STATUS_IGNORE = "RESP_STATUS_IGNORE"  # 1      # 已知 错误 情况的 标记赋值   # 不需要手动处理
RESP_STATUS_ERROR = "RESP_STATUS_ERROR"  # -1    # 未知 错误 情况的 标记赋值  # 需要手动处理

# 响应头长度常量
RESP_LENGTH_DEFAULT = "RESP_LENGTH_DEFAULT"  # 没有任何操作时候的 默认值
RESP_LENGTH_BLANK = "RESP_LENGTH_BLANK"  # 获取结果为空白
RESP_LENGTH_ERROR = "RESP_LENGTH_ERROR"  # 未知 错误 情况的 标记赋值

# 响应实际头部HASH
RESP_HEADERS_CRC_DEFAULT = "RESP_HEADERS_CRC_DEFAULT"  # 没有任何操作时候的 默认值
RESP_HEADERS_CRC_ERROR = "RESP_HEADERS_CRC_ERROR"  # 未知 错误 情况的 标记赋值
RESP_HEADERS_CRC_BLANK = "RESP_HEADERS_CRC_BLANK"  # 获取结果为空白

# 响应实际头部
RESP_HEADERS_DEFAULT = "RESP_HEADERS_DEFAULT"  # 没有任何操作时候的 默认值
RESP_HEADERS_ERROR = "RESP_HEADERS_ERROR"  # 未知 错误 情况的 标记赋值
RESP_HEADERS_BLANK = "RESP_HEADERS_BLANK"  # 获取结果为空白
RESP_HEADERS_IGNORE = "RESP_HEADERS_IGNORE"  # 已知 错误 情况的 标记赋值

# 重定向常量
RESP_REDIRECT_DEFAULT = "RESP_REDIRECT_DEFAULT"  # 没有任何操作时候的 默认值
RESP_REDIRECT_ORIGIN = "RESP_REDIRECT_ORIGIN"  # 获取结果为原始情况
RESP_REDIRECT_ERROR = "RESP_REDIRECT_ERROR"  # 未知 错误 情况的 标记赋值

# 响应实际内容HASH
RESP_CONTENT_CRC_DEFAULT = "RESP_CONTENT_CRC_DEFAULT"  # 没有任何操作时候的 默认值
RESP_CONTENT_CRC_ERROR = "RESP_CONTENT_CRC_ERROR"  # 未知 错误 情况的 标记赋值
RESP_CONTENT_CRC_BLANK = "RESP_CONTENT_CRC_BLANK"  # 获取结果为空白
RESP_CONTENT_CRC_LARGE = "RESP_CONTENT_CRC_LARGE"  # 获取结果为空白 超限

# 响应实际内容
RESP_CONTENT_DEFAULT = "RESP_CONTENT_DEFAULT"  # 没有任何操作时候的 默认值
RESP_CONTENT_LARGE = "RESP_CONTENT_LARGE"  # 获取结果为空白
RESP_CONTENT_ERROR = "RESP_CONTENT_ERROR"  # 未知 错误 情况的 标记赋值
RESP_CONTENT_IGNORE = "RESP_CONTENT_IGNORE"  # 已知 情况的 标记赋值
RESP_CONTENT_BLANK = "RESP_CONTENT_BLANK"  # 已知 情况的 标记赋值

# 文本大小常量
RESP_SIZE_DEFAULT = "RESP_SIZE_DEFAULT"  # 没有任何操作时候的 默认值
RESP_SIZE_ERROR = "RESP_SIZE_ERROR"  # 未知 错误 情况的 标记赋值
RESP_SIZE_LARGE = "RESP_SIZE_LARGE"  # 已知 情况的 内容太大
RESP_SIZE_BLANK = "RESP_SIZE_BLANK"  # 获取结果为空白

# 文本标题常量
RESP_TITLE_DEFAULT = "RESP_TITLE_DEFAULT"  # 没有任何操作时候的 默认值
RESP_TITLE_ERROR = "RESP_TITLE_ERROR"  # 未知 错误 情况的 标记赋值
RESP_TITLE_LARGE = "RESP_TITLE_LARGE"  # 已知 情况的 内容太大
RESP_TITLE_BLANK = "RESP_TITLE_BLANK"  # 获取结果为空白
############################################################
# 默认的响应字典,使用前被copy一份
DEFAULT_HTTP_RESP_DICT = {
    HTTP_REQ_TARGET: NONE,  # 请求的URL, 必须在请求时填充
    HTTP_CONST_SIGN: NONE,  # 请求自定义的标记, 必须在请求时填充 原样返回

    HTTP_RESP_STATUS: RESP_STATUS_DEFAULT,  # 响应状态码 赋值默认值
    HTTP_RESP_LENGTH: RESP_LENGTH_DEFAULT,  # 响应CL长度 赋值默认值

    HTTP_RESP_SIZE: RESP_SIZE_DEFAULT,  # 响应文本大小 赋值默认值
    HTTP_RESP_TITLE: RESP_TITLE_DEFAULT,  # 响应文本标题 赋值默认值

    HTTP_RESP_REDIRECT: RESP_REDIRECT_DEFAULT,  # 响应重定向URL 赋值默认值

    HTTP_RESP_HEADERS_CRC: RESP_HEADERS_CRC_DEFAULT,  # 响应头部HASH 赋值默认值
    HTTP_RESP_CONTENT_CRC: RESP_CONTENT_CRC_DEFAULT,  # 响应文本HASH 赋值默认值

    HTTP_RESP_HEADERS_OPT: RESP_HEADERS_DEFAULT,  # 响应头部信息 赋值默认值
    HTTP_RESP_CONTENT_OPT: RESP_CONTENT_DEFAULT,  # 响应内容信息 赋值默认值
}
############################################################
# 每个响应键的默认值或空值，在动态筛选时被忽略
FILTER_HTTP_VALUE_DICT = {
    HTTP_REQ_TARGET: [NONE, NULL],
    HTTP_CONST_SIGN: [NONE, NULL],

    HTTP_RESP_STATUS: [RESP_STATUS_DEFAULT, RESP_STATUS_ERROR, RESP_STATUS_IGNORE, NONE, NULL],
    HTTP_RESP_LENGTH: [RESP_LENGTH_DEFAULT, RESP_LENGTH_ERROR, RESP_LENGTH_BLANK, NONE, NULL],
    HTTP_RESP_SIZE: [RESP_SIZE_DEFAULT, RESP_SIZE_ERROR, RESP_SIZE_LARGE, RESP_SIZE_BLANK, NONE, NULL],
    HTTP_RESP_TITLE: [RESP_TITLE_DEFAULT, RESP_TITLE_ERROR, RESP_TITLE_LARGE, RESP_TITLE_BLANK , NONE, NULL],

    HTTP_RESP_REDIRECT: [RESP_REDIRECT_DEFAULT, RESP_REDIRECT_ERROR, RESP_REDIRECT_ORIGIN, NONE, NULL],

    HTTP_RESP_HEADERS_CRC: [RESP_HEADERS_CRC_DEFAULT, RESP_HEADERS_CRC_ERROR, RESP_HEADERS_CRC_BLANK, NONE, NULL],
    HTTP_RESP_HEADERS_OPT: [RESP_HEADERS_DEFAULT, RESP_HEADERS_ERROR, RESP_HEADERS_BLANK, RESP_HEADERS_IGNORE, NONE, NULL],

    HTTP_RESP_CONTENT_CRC: [RESP_CONTENT_CRC_DEFAULT, RESP_CONTENT_CRC_ERROR, RESP_CONTENT_CRC_BLANK, RESP_CONTENT_CRC_LARGE, NONE, NULL],
    HTTP_RESP_CONTENT_OPT: [RESP_CONTENT_DEFAULT, RESP_CONTENT_ERROR, RESP_CONTENT_BLANK, RESP_CONTENT_LARGE, RESP_CONTENT_IGNORE, NONE, NULL],
}

# 分析动态排除字典时，需要被忽略的键列表, 应该动态性强的（用户输入的、响应头的时间戳、）
FILTER_DYNA_IGNORE_KEYS = [HTTP_CONST_SIGN,
                           HTTP_REQ_TARGET,
                           HTTP_RESP_CONTENT_OPT,
                           HTTP_RESP_HEADERS_OPT,
                           ]
############################################################
# 默认请求头
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Accept-Encoding': ''
}
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
