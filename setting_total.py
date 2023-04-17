#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件
import sys
import time

from libs.lib_file_operate.file_path import auto_make_dir
from libs.lib_requests.requests_const import HTTP_USER_AGENTS
from libs.lib_requests.requests_tools import random_useragent, random_x_forwarded_for
from setting_dict import *

sys.dont_write_bytecode = True  # 设置不生成pyc文件
##################################################################
# 程序开始运行时间
GB_RUN_TIME = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
##################################################################
# 获取setting.py脚本所在路径作为的基本路径
GB_BASE_DIR = pathlib.Path(__file__).parent.resolve()
##################################################################
# 是否显示DEBUG级别信息,默认False
GB_DEBUG_FLAG = False
##################################################################
# 每个目标的最大扫描URL阈值[数字] 辅助调试 或 其他用途
GB_MAX_URL_NUM = None
##################################################################
# 版本号配置
GB_VERSION = "Ver 0.2.2 2023-04-17 01:00"
##################################################################
# 停止扫描阈值[数字] # 如果每个目标的非正常响应超过这个阈值, 就停止任务
GB_MAX_ERROR_NUM = None
##################################################################
# 在配置文件中配置默认目标参数  支持文件 或 URL
GB_TARGET = "target.txt"
##################################################################
# 输入目标的处理
# 对HOST:PORT格式的目标进行测试,动态判断是否添加https协议头
GB_DEFAULT_PROTO_HEAD = "auto"  # 可选 http|https|auto

# 对URL目标开启目标URL可访问性判断
GB_URL_ACCESS_TEST = True

# 目标URL拆分,默认True # 对输入的URL路径进行分解
GB_SPLIT_TARGET_PATH = False
# 示例：https://XXX/item/DD/ 会被分解为 https://XXX/item/DD/,https://XXX/item/,https://XXX/
##################################################################
# 设置日志输出文件路径 #目录不存在会自动创建
GB_LOG_FILE_DIR = str(GB_BASE_DIR.joinpath("runtime"))

GB_LOG_FILE_PATH = os.path.join(GB_LOG_FILE_DIR, "runtime_module.log")
# LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, "runtime_{GB_RUN_TIME}_module.log")

GB_INFO_LOG_FILE = GB_LOG_FILE_PATH.replace('module', 'info')
GB_DBG_LOG_FILE = GB_LOG_FILE_PATH.replace('module', 'debug')
GB_ERR_LOG_FILE = GB_LOG_FILE_PATH.replace('module', 'error')

# 记录不可访问的目标 # 没啥用
GB_INACCESSIBLE_RECORD = GB_LOG_FILE_PATH.replace('module', 'inaccessible')
# 记录可以访问的目标 # 没啥用
GB_ACCESSIBLE_RECORD = GB_LOG_FILE_PATH.replace('module', 'accessible')

# 记录扫描已完成的URL 针对每个目标生成不同的记录文件
GB_PER_HOST_HISTORY_FILE = GB_LOG_FILE_PATH.replace('module', 'history.{host_port}')
# 每个HOST扫描URL的过滤,建议开启
GB_EXCLUDE_HOST_HISTORY = True
##################################################################
# 设置输出结果文件目录
GB_RESULT_DIR = GB_BASE_DIR.joinpath("result")

# 结果文件名称
# GB_RESULT_FILE_PATH = os.path.join(GB_RESULT_DIR,f"result_{GB_RUN_TIME}.csv")
GB_RESULT_FILE_PATH = "auto"  # auto 根据主机名自动生成
#######################################################################
# 请求速度限制
# 默认线程数
GB_THREADS_COUNT = 100

# 每个线程之间的延迟 单位S秒
GB_THREAD_SLEEP = 0

# 任务分块大小 所有任务会被分为多个列表
GB_TASK_CHUNK_SIZE = GB_THREADS_COUNT
#######################################################################
# HTTP请求相关默认配置
# 默认请求方法
GB_REQ_METHOD = "get"

# 默认请求数据
GB_REQ_BODY = None

# 对外请求代理
GB_PROXIES = {
    # "http": "http://127.0.0.1:8080",
    # "https": "http://127.0.0.1:8080",
    # "http": "http://user:pass@10.10.1.10:3128/",
    # "https": "https://192.168.88.1:8080",
    # "http": "socks5://192.168.88.1:1080",
}

# 采用流模式访问 流模式能够解决大文件读取问题
GB_STREAM_MODE = True
# 是否开启https服务器的证书校验
GB_SSL_VERIFY = False
# 超时时间 # URL重定向会严重影响程序的运行时间
GB_TIMEOUT = 5
# 是否允许URL重定向 # URL重定向会严重影响程序的运行时间
GB_ALLOW_REDIRECTS = False
# 访问没有结果时,自动重试的最大次数
GB_RETRY_TIMES = 3

# 是否自动根据URL设置动态HOST头
GB_ADD_DYNAMIC_HOST = True
# 是否自动根据URL设置动态refer头
GB_ADD_DYNAMIC_REFER = True
# 随机User-Agent # 可能会导致无法建立默认会话 # 报错内容 Exceeded 30 redirects
GB_ADD_RANDOM_USERAGENT = True
# 是否允许随机X-Forwarded-For
GB_ADD_RANDOM_XFF = True

# HTTP 头设置
GB_HEADERS = {
    'User-Agent': random_useragent(HTTP_USER_AGENTS, GB_ADD_RANDOM_USERAGENT),
    'X_FORWARDED_FOR': random_x_forwarded_for(GB_ADD_RANDOM_XFF),
    'Accept-Encoding': ''
}

########################扩展的调用函数###################################
# 排除指定结果
# 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
GB_EXCLUDE_STATUS = [404, 401, 403, 405, 406, 410, 500, 501, 502, 503]

# 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
GB_EXCLUDE_REGEXP = r"页面不存在|未找到|not[ -]found|403|404|410"
##################################################################
auto_make_dir(GB_HIT_FILE_DIR)
auto_make_dir(GB_RESULT_DIR)
########################扩展的调用函数###################################
