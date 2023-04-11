#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件
import sys
import time
import random

from libs.util_file import auto_make_dir
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
# # 测试模式 每个目标URL只获取生成的前100个URL进行测试,
# GB_TEST_MODE = False
##################################################################
# 版本号配置
GB_VERSION = "Ver 0.2.0 2023-04-11 20:23"
##################################################################
# 停止扫描阈值 # 如果非正常响应超过这个阈值, 就停止任务
GB_MAX_ERROR_NUM = 20
##################################################################
# 中文路径、特殊字符会以列表内的编码作为基础编码，再进行URL编码
GB_CHINESE_ENCODE = ['utf-8']  # ['utf-8', 'gbk', 'gb2312']
# 注意:gb2312编码繁体中文可能报错,此时可使用gbk编码,GBK与G2312编码结果相同

# 是否仅对包含中文的路径使用URL编码模式,默认True 否则所有路径都会处理,所有特殊字符都会被编码,
GB_ONLY_ENCODE_CHINESE = True
##################################################################
# 在配置文件中配置默认目标参数  支持文件 或 URL
GB_TARGET = "target.txt"
##################################################################
# 输入目标的处理
# 对HOST:PORT格式的目标进行测试,动态判断是否添加https协议头
GB_DEFAULT_PROTO_HEAD = "auto"  # 可选 http|https|auto

# 对URL目标开启目标URL可访问性判断
GB_URL_ACCESS_TEST = False

# 目标URL拆分,默认True # 对输入的URL路径进行分解
GB_SPLIT_TARGET_PATH = True
# 示例：https://XXX/item/DD/ 会被分解为 https://XXX/item/DD/,https://XXX/item/,https://XXX/
##################################################################
# 设置日志输出文件路径 #目录不存在会自动创建
LOG_FILE_DIR = str(GB_BASE_DIR.joinpath("runtime"))

LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, "runtime_module.log")
# LOG_FILE_PATH = os.path.join(LOG_FILE_DIR, "runtime_{GB_RUN_TIME}_module.log")

GB_INFO_LOG_FILE = LOG_FILE_PATH.replace('module', 'info')
GB_DBG_LOG_FILE = LOG_FILE_PATH.replace('module', 'debug')
GB_ERR_LOG_FILE = LOG_FILE_PATH.replace('module', 'error')

# 记录不可访问的目标 # 没啥用
GB_INACCESSIBLE_RECORD = LOG_FILE_PATH.replace('module', 'inaccessible')
# 记录可以访问的目标 # 没啥用
GB_ACCESSIBLE_RECORD = LOG_FILE_PATH.replace('module', 'accessible')

# 记录扫描已完成的URL 针对每个目标生成不同的记录文件
GB_PER_HOST_HISTORY_FILE = LOG_FILE_PATH.replace('module', 'history.{host_port}')
# 每个HOST扫描URL的过滤,建议开启
GB_EXCLUDE_HOST_HISTORY = True
##################################################################
# 全局变量,存储自定义 基本变量
GB_BASE_VAR_REPLACE_DICT = {"%BLANK%": ['']}

# 全局变量,存储自定义 因变量
GB_DEPENDENT_VAR_REPLACE_DICT = {"%%DEPENDENT%%": ['admin', 'product', 'wwwroot', 'www', '网站']}
# 程序内置 %%DOMAIN%% 在URL中,域名因变量列表所代表的字符串
# 程序内置 %%PATH%% 在URL中,路径因变量列表所代表的字符串

# DOMAIN PATH 因变量中的 符号替换规则, 替换后追加到域名因子列表
GB_SYMBOL_REPLACE_DICT = {":": ["_"], ".": ["_"]}

# 删除带有 特定符号 的因变量（比如:）的元素
GB_NOT_ALLOW_SYMBOL = [":"]

GB_IGNORE_IP_FORMAT = True
##################################################################
# 最终生成的扫描路径处理

# 替换路径中的多个//为一个/
GB_REMOVE_MULTI_SLASHES = True

# 去除以特定字符结尾的URL
GB_REMOVE_SOME_SYMBOL = ['.']

# URL路径全部小写
GB_URL_PATH_LOWERCASE = True

# 为每个路径添加自定义前缀
# GB_ADD_CUSTOM_PREFIX = ['/admin']
GB_ADD_CUSTOM_PREFIX = None

# 仅扫描指定后缀的URL目标,注意:后缀不需要加[.]前缀
# GB_STORE_SPECIFY_EXT_LIST = ['xxx']
GB_ONLY_SCAN_SPECIFY_EXT = None

# 仅移除指定后缀的URL, 注意:后缀不需要加[.]前缀
GB_NO_SCAN_SPECIFY_EXT = None
# 当保留指定后缀和移除指定后缀同时存在时,先进行指定后缀URL保留,后进行指定后缀URL排除, 建议一次扫描仅开启一个开关
##################################################################
# 设置输出结果文件目录
GB_RESULT_DIR = GB_BASE_DIR.joinpath("result")
auto_make_dir(GB_RESULT_DIR)

# 结果文件名称  # auto 根据主机名和时间戳自动生成
GB_RESULT_FILE_PATH = "auto"
# GB_RESULT_FILE_PATH = os.path.join(GB_RESULT_DIR,f"result_{GB_RUN_TIME}.csv")
##################################################################
# 是否保存命中结果到HIT_XXX文件
SAVE_HIT_RESULT = True

# 命中结果文件追加模式
GB_HIT_OVER_CALC = True
# True,计算频率后覆盖写入、后期写入时内存占用大,磁盘占用小,读取效率高
# False 直接追加命中记录、后期写入时内存占用小,磁盘占用大,读取效率低

# 命中文件保存路径
GB_HIT_FILE_DIR = GB_BASE_DIR.joinpath("dict_hit")
auto_make_dir(GB_HIT_FILE_DIR)
# 存储命中的后缀
GB_HIT_EXT_FILE = os.path.join(GB_HIT_FILE_DIR, 'HIT_EXT.hit')
# 存储命中的路径
GB_HIT_DIRECT_FILE = os.path.join(GB_HIT_FILE_DIR, 'HIT_DIRECT.hit')
# 存储命中的目录
GB_HIT_FOLDER_FILE = os.path.join(GB_HIT_FILE_DIR, 'HIT_FOLDER.hit')
# 存储命中的文件
GB_HIT_FILES_FILE = os.path.join(GB_HIT_FILE_DIR, 'HIT_FILE.hit')
##################################################################

# HTTP请求相关默认配置
# 默认请求方法
GB_REQ_METHOD = "get"

# 默认线程数
GB_THREADS_COUNT = 100

# 每个线程之间的延迟 单位S秒
GB_THREAD_SLEEP = 0

# 对外请求代理
GB_PROXIES = {
    # "http": "http://127.0.0.1:8080",
    # "https": "http://127.0.0.1:8080",
    # "http": "http://user:pass@10.10.1.10:3128/",
    # "https": "https://192.168.88.1:8080",
    # "http": "socks5://192.168.88.1:1080",
}

# 采用流模式访问
GB_STREAM_MODE = False
# 是否开启https服务器的证书校验
GB_SSL_VERIFY = False
# 超时时间 # URL重定向会严重影响程序的运行时间
GB_TIMEOUT = 5
# 是否允许URL重定向 # URL重定向会严重影响程序的运行时间
GB_ALLOW_REDIRECTS = True
# 访问没有结果时,自动重试的最大次数
GB_RETRY_TIMES = 3
#############################################
# 是否自动根据URL设置动态HOST头
GB_ADD_DYNAMIC_HOST = True
# 是否自动根据URL设置动态refer头
GB_ADD_DYNAMIC_REFER = True
# 随机User-Agent # 可能会导致无法建立默认会话 # 报错内容 Exceeded 30 redirects
GB_ADD_RANDOM_USERAGENT = True
# 是否允许随机X-Forwarded-For
GB_ADD_RANDOM_XFF = True

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


# 随机生成User-Agent
def random_useragent(condition=False):
    if condition:
        return random.choice(USER_AGENTS)
    else:
        return USER_AGENTS[0]


# 随机X-Forwarded-For，动态IP
def random_x_forwarded_for(condition=False):
    if condition:
        return '%d.%d.%d.%d' % (
            random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
    else:
        return '8.8.8.8'


# HTTP 头设置
GB_HEADERS = {
    'User-Agent': random_useragent(GB_ADD_RANDOM_USERAGENT),
    'X_FORWARDED_FOR': random_x_forwarded_for(GB_ADD_RANDOM_XFF),
    'Accept-Encoding': ''
}
#######################################################################
# 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
GB_EXCLUDE_STATUS = [404, 401, 403, 405, 406, 410, 500, 501, 502, 503]

# 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
GB_EXCLUDE_REGEXP = r"页面不存在|未找到|not[ -]found|403|404|410"
########################扩展的调用函数###################################
