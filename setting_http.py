#!/usr/bin/env python
# encoding: utf-8
from libs.lib_args.input_const import *


def init_custom(config):
    ##################################################################
    # 对HOST:PORT格式的目标进行测试,动态判断是否添加https协议头
    config[GB_DEFAULT_PROTO] = None  # 可选 http|https|None表示自动获取
    ##################################################################
    # 对URL目标开启目标URL可访问性判断
    config[GB_URL_ACCESS_TEST] = True
    ##################################################################
    # 默认线程数
    config[GB_THREADS_COUNT] = 100
    # 每个线程之间的延迟 单位S秒
    config[GB_THREAD_SLEEP] = 0
    # 任务分块大小 所有任务会被分为多个列表
    config[GB_TASK_CHUNK_SIZE] = config[GB_THREADS_COUNT]
    ##################################################################
    # 默认请求方法
    config[GB_REQ_METHOD] = "HEAD"  # 使用get等方法需要进行全下载,会卡顿
    # 默认请求数据
    config[GB_REQ_BODY] = None
    # 对外请求代理
    config[GB_PROXIES] = {
        # "http": "http://127.0.0.1:8080",
        # "https": "http://127.0.0.1:8080",  # 此处不能使用https
        # "http": "http://user:pass@10.10.1.10:3128/",
        # "https": "https://192.168.88.1:8080",
        # "http": "socks5://127.0.0.1:10808",
        # "https": "socks5://127.0.0.1:10808",
    }

    # 采用流模式访问 流模式能够解决大文件读取问题
    config[GB_STREAM_MODE] = True
    # 是否开启https服务器的证书校验
    config[GB_SSL_VERIFY] = False
    # 超时时间 # URL重定向会严重影响程序的运行时间
    config[GB_TIME_OUT] = 10
    # 是否允许URL重定向 # URL重定向会严重影响程序的运行时间
    config[GB_ALLOW_REDIRECTS] = False
    # 访问没有结果时,自动重试的最大次数
    config[GB_RETRY_TIMES] = 3
    ##################################################################
    # 默认请求头配置
    config[GB_REQ_HEADERS] = {
        # 'Host': 'testphp.vulnweb.com',    # 默认会自动添加请求HOST
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Origin': 'http://www.baidu.com/',   # 默认会自动添加请求URL
        # 'Referer': 'http://www.baidu.com/',  # 默认会自动添加请求URL
        # 'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
        # 'Transfer-Encoding': 'identity',      # 多个请求头综合影响响应头CL的获取|不建议设置,部分服务器不支持
        'Connection': 'close',
    }
    ##################################################################
    # 是否自动根据URL设置动态HOST头
    config[GB_DYNA_REQ_HOST] = True
    # 是否自动根据URL设置动态refer头
    config[GB_DYNA_REQ_REFER] = True
    # 随机User-Agent # 可能会导致无法建立默认会话 # 报错内容 Exceeded 30 redirects
    config[GB_RANDOM_UA] = False
    # 是否允许随机X-Forwarded-For
    config[GB_RANDOM_XFF] = False # 需要优化多个XFF头支持
    ########################扩展的调用函数###################################
    # 排除指定结果
    # 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
    config[GB_EXCLUDE_STATUS] = [301, 302, 404, 401, 405, 406, 410, 500, 501, 502, 503]

    # 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
    config[GB_EXCLUDE_REGEXP] = r"页面不存在|未找到|not[ -]found|403|404|410"
    ##################################################################