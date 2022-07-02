#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件
import sys

sys.dont_write_bytecode = True  # 设置不生成pyc文件

import os
import random
import pathlib
import time

from libs.DataType import config
# 使用config存储主要的设置用户变量更加优雅,注意使用config存储logger后会导致不能用logger打印config,由于死循环调用的问题
# 所有需要用户输入的变量[就是说cmd直接解析的参数,非直接解析的参数不需要加],需要添加config.作为前缀,
from libs.ToolUtils import get_random_str, file_is_exist, read_file_to_list_de_weight

##################################################################
# 获取setting.py脚本所在路径作为的基本路径
BASE_DIR = pathlib.Path(__file__).parent.resolve()
##################################################################
# 是否显示DEBUG级别信息,默认False
config.debug = False

# 是否属于测试模式,默认False
TEST_MODE_HANDLE = False
# 测试模式每个目标URL只获取生成的前100个URL进行测试,
##################################################################
# 版本号配置
version = "Ver 0.1.8 2022-07-02 08:54"
##################################################################
# 停止扫描阈值,默认True
STOP_SCAN_SWITCH = True
STOP_SCAN_NUM = 20
# 如果非正常响应超过这个阈值, 就关闭多线程中的所有线程任务
##################################################################
# 中文路径、特殊字符会以列表内的编码作为基础编码，再进行URL编码
ALL_BASE_ENCODE = ['utf-8']  # ['utf-8', 'gbk']
# 注意:gb2312编码繁体中文可能报错,此时可使用gbk编码,GBK与G2312编码结果相同
# 中文编码模式: 路径列表中的元素[/說明.txt] 已基于 [utf-8] 编码 URL编码为:/%E8%AA%AA%E6%98%8E.txt
# 中文编码模式: 路径列表中的元素[/說明.txt] 已基于 [gbk] 编码 URL编码为:/%D5f%C3%F7.txt
# 中文编码模式: 路径列表中的元素[/說明.txt] 基于 [gb2312] 编码进行URL编码时,发生错误:'gb2312' codec can't encode character '\u8aaa' in position 1: illegal multibyte sequence
# 中文编码模式: 路径列表中的元素[/服务器.rar4] 已基于 [gb2312] 编码 URL编码为:/%B7%FE%CE%F1%C6%F7.rar4
# 中文编码模式: 路径列表中的元素[/服务器.rar4] 已基于 [gbk] 编码 URL编码为:/%B7%FE%CE%F1%C6%F7.rar4

# 是否对所有最终PATH开启URL编码模式,解决中文路径乱码问题
ENCODE_ALL_PATH = True

# URL路径列表编码处理包含两种模式,一种是仅处理中文路径（使用正则匹配出中文）,一种是所有路径都会处理,所有特殊字符都会被编码,
# 是否仅对包含中文的路径使用URL编码模式,默认True
ENCODE_CHINESE_ONLY = True
##################################################################
# 在配置文件中配置默认目标文件等参数 比cmd输入参数优先级低 一般作为默认参数使用
config.target = None
config.target_file = "target.txt"
# 当没有输入目标时,默认加载该文件,可日常使用
###################程序基本配置开始##################################
# 是否对符合URL格式的目标直接开启目标URL可访问性判断,默认True
ACCESS_TEST_URL = True

# 是否对HOST:PORT格式的目标进行URL访问测试,根据响应结果自动添加协议头,默认True
ACCESS_ADD_PROTO_HEAD = True

# 是否URL访问模式的基础上,动态判断是否添加https协议头,默认True
SMART_ADD_PROTO_HEAD = True

# 是否开启多目标模式,默认True
# 对URL路径进行分解,一个目标能够变成多个目标,每多一个目标,请求URL就会多一倍
MULTI_TARGET_PATH_MODE = True
# 示例：https://XXX/item/DD/ 会被分解为 https://XXX/item/DD/,https://XXX/item/,https://XXX/

# 程序开始运行时间
RUN_TIME = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

# 是否将每一次批量扫描的扫描结果分别按照多个HOST_PORT进行拆分
WRITE_RESULT_DIFF_SWITCH = False

# 是否在结果文件和日志文件中添加程序启动时间,默认添加
FILE_RUN_TIME_SWITCH = False

# 设置日志输出文件路径 #目录不存在会自动创建
if FILE_RUN_TIME_SWITCH:
    LOG_FILE_PATH = str(BASE_DIR.joinpath("runtime/runtime_{time}_module.log")).format(time=RUN_TIME)
else:
    LOG_FILE_PATH = str(BASE_DIR.joinpath("runtime/runtime_module.log"))

INFO_LOG_FILE_PATH = LOG_FILE_PATH.replace('module', 'info')
DBG_LOG_FILE_PATH = LOG_FILE_PATH.replace('module', 'debug')
ERR_LOG_FILE_PATH = LOG_FILE_PATH.replace('module', 'error')

# 记录已完成扫描的目标 # 固定命名,不需要添加时间戳
# 可访问目标已访问记录
ACCESSIBLE_TARGET_VISITED_RECORD_FILE = str(BASE_DIR.joinpath("runtime/runtime_module.log")).replace('module', 'visited_accessible')
# 不可访问目标已访问记录
INACCESSIBLE_TARGET_VISITED_RECORD_FILE = str(BASE_DIR.joinpath("runtime/runtime_module.log")).replace('module', 'visited_inaccessible')

# 扫描时是否排除可访问目标的测试记录,默认True
EXCLUDE_ACCESSIBLE_VISITED_RECORD = True
ACCESSIBLE_VISITED_TARGET_LIST = []
# 读取命中记录文件
if EXCLUDE_ACCESSIBLE_VISITED_RECORD and file_is_exist(ACCESSIBLE_TARGET_VISITED_RECORD_FILE):
    ACCESSIBLE_VISITED_TARGET_LIST = read_file_to_list_de_weight(ACCESSIBLE_TARGET_VISITED_RECORD_FILE, encoding='utf-8')

# 扫描时是否排除不可访问目标的测试记录,默认True
EXCLUDE_INACCESSIBLE_VISITED_RECORD = True
INACCESSIBLE_VISITED_TARGET_LIST = []
# 读取命中记录文件
if EXCLUDE_INACCESSIBLE_VISITED_RECORD and file_is_exist(INACCESSIBLE_TARGET_VISITED_RECORD_FILE):
    INACCESSIBLE_VISITED_TARGET_LIST = read_file_to_list_de_weight(INACCESSIBLE_TARGET_VISITED_RECORD_FILE, encoding='utf-8')

# 设置输出结果文件目录
RESULT_DIR_PATH = BASE_DIR.joinpath("result")
if not os.path.exists(RESULT_DIR_PATH): os.makedirs(RESULT_DIR_PATH)

# 字典来自文件列表 #从文件夹获得所有文件列表
ALL_DICT_PATH = ["dict-max", "dict-mid", "dict-min"]
base_var = "base_var"
direct_path = "direct_path"
group_folder = "group_folder"
group_files = "group_files"
all_dir_name = [base_var, direct_path, group_folder, group_files]

config.dict_path = "dict-max"  # 设置默认调用的字典路径

# 字典文件后缀
dict_file_suffix = '.lst'

# 是否读取DIRECT目录下的字典
DIRECT_DICT_MODE = True

# 指定仅读取 group-xxx目录指定的文件字典,不再读取 group-xxx 目录下的所有文件
SPECIFY_GROUP_FOLDER_DICT = []
SPECIFY_GROUP_FILES_DICT = []

# 是否读取GROUP-XX目录下的字典
GROUP_DICT_MODE = True

# 要提取的路径频率阈值，大于等于FREQUENCY_MIN 小于等于 FREQUENCY_MAX的字典会被提取
# # 读取命中的后缀文件时的频率阈值 # 由于后缀文件不好进行进一步的解析,所以加到每个后缀以后
# FREQUENCY_MIN_HIT = 10
# FREQUENCY_MAX_HIT = 999
#
# # 是否将历史命中扩展的值扩展到每一个基本变量中
# APPEND_HIT_EXT = False

# 读取BASE目录下字典时的频率阈值
FREQUENCY_MIN_BASE = 1
FREQUENCY_MAX_BASE = 999

# 读取DIRECT目录下字典时的频率阈值
FREQUENCY_MIN_DIRECT = 1
FREQUENCY_MAX_DIRECT = 999

# 读取GROUP目录下字典时的频率阈值
FREQUENCY_MIN_GROUP = 1
FREQUENCY_MAX_GROUP = 999

# 指定path和频率的分隔符,如果每一行的内容为/xxx/xxx  frequency==10,那么切割符为'frequency=='
SEPARATOR = 'frequency=='

# 如果结果字典中已有的值,是否进行追加频率,False时直接进行频率覆盖
ADDITIONAL = True

# 行注释符号
ANNOTATION = '#'
# 替换字符列表-不再需要手动指定－从文件名和文件内容中自动提取键值对
# 自动读取base目录所有文件并进行自动赋值

# 全局变量,存储基本变量替换字典 #此处可设置其他默认值
BASE_VAR_REPLACE_DICT = {"%BLANK%": ['']}

# 因变量替换对应表,初值为空,后根据URL变量自动填充替换  #此处可设置其他默认值
DEPEND_VAR_REPLACE_DICT = {"%%DOMAIN%%": [], "%%PATH%%": []}
# %%DOMAIN%% 在URL中,域名因变量列表所代表的字符串
# %%PATH%% 在URL中,路径因变量列表所代表的字符串
# 由于需要动态改变,内容实际在代码内部实现,

# 域名变量如果是IP是否需要忽略
IGNORE_IP_FORMAT = True

# 存储自定义变量单词,会自动加入到%%DOMAIN%% 和%%PATH%% 中
# CUSTOME_REPLACE_VAR = ['admin', 'product', 'wwwroot', 'www', '网站']
CUSTOME_REPLACE_VAR = []
# 是否在每个因变量内追加自定义变量
APPEND_CUSTOM_VAR = True

# DOMAIN因变量中HOST:PORt中的替换规则,替换后追加到域名因子列表
DOMAIN_SYSBOL_REPLACE_DICT = {
    ":": ["_"],
    ".": ["_"]}

# PATH因变量中HOST:PORt中的替换规则,替换后追加到域名因子列表
PATH_SYSBOL_REPLACE_DICT = {
    ":": ["_"],  # 获取的路径相关单词中的[:]会替换为[_]
    ".": ["_"]  # 获取的路径相关单词中的[.]会替换为[_]
}

# 路径中不该有的字符 # 解析出来的域名单词和路径单词中有这个符号的元素会删除
NOT_PATH_SYMBOL = [":"]

# 是否去除路径中包含不该有的字符（比如:）的元素
REMOVE_NOT_PATH_SYMBOL = True

# 是否替换路径中的多个//为一个/
REMOVE_MULTI_SLASHES = True

# 去除URL[. /]结尾列表与开关
REMOVE_SYMBOL_LIST = ['.', '/']
REMOVE_END_SYMBOL_SWITCH = False

# URL路径全部小写
PATH_LOWERCASE_SWITCH = False

# 为每个路径添加自定义前缀
CUSTOM_PREFIX_LIST = ['/admin']
# 为每个路径添加自定义前缀功能开关
CUSTOM_PREFIX_SWITCH = False

# 命中文件保存路径
HIT_FILE_PATH = "dict-hit"
if not os.path.exists(HIT_FILE_PATH): os.makedirs(HIT_FILE_PATH)
HIT_EXT_PATH = os.path.join(HIT_FILE_PATH, 'HIT_EXT.hit')
HIT_DIRECT_PATH = os.path.join(HIT_FILE_PATH, 'HIT_DIRECT.hit')
HIT_FOLDER_PATH = os.path.join(HIT_FILE_PATH, 'HIT_FLODER.hit')
HIT_FILES_PATH = os.path.join(HIT_FILE_PATH, 'HIT_FILE.hit')

# 是否保存命中结果到HIT_XXX文件
SAVE_HIT_RESULT = True

# 命中结果文件追加模式
# True,计算频率后覆盖写入、后期写入时内存占用大,磁盘占用小,读取效率高
# False 直接追加命中记录、后期写入时内存占用小,磁盘占用大,读取效率低
HIT_OVERWRITE_MODE = False

# 保留指定后缀的URL目标,注意:后缀不需要加[.]前缀
STORE_SPECIFY_EXT_SWITCH = False
STORE_SPECIFY_EXT_LIST = ['xxx']

# 移除指定后缀的URL,注意:后缀不需要加[.]前缀
DELETE_SPECIFY_EXT_SWITCH = False
DELETE_SPECIFY_EXT_LIST = ['xxx']
# 当保留指定后缀和移除指定后缀同时存在时,先进行指定后缀URL保留,后进行指定后缀URL排除, 建议一次扫描仅开启一个开关
####################无需进行处理的初始变量赋值开始###########################
# 代码中会自动添加变量替换关键字
ALL_REPLACE_KEY = []

# 全局变量,用于存储请求所有已经访问过的目标URL
ALL_ACCESSED_URL = []
####################HTTP请求相关默认配置开始##########################
# 默认请求方法
config.http_method = "get"

# 默认线程数
config.threads_count = 30

# 默认代理配置
config.proxies = {
    # "http": "http://user:pass@10.10.1.10:3128/",
    # "https": "http://192.168.88.1:8080",
    # "http": "http://192.168.88.1:8080", # TOR 洋葱路由器
}

# 是否采用流模式访问
HTTP_STREAM = True

# 是否开启https服务器的证书校验
ALLOW_SSL_VERIFY = False

# 超时时间 # URL重定向会严重影响程序的运行时间
HTTP_TIMEOUT = 2

# 是否允许URL重定向 # URL重定向会严重影响程序的运行时间
ALLOW_REDIRECTS = True

# 访问没有结果时,自动重试的最大次数
RETRY_TIMES = 3

# 是否自动根据URL设置动态HOST头
DYNAMIC_HOST_HEADER = True

# 是否自动根据URL设置动态refer头
DYNAMIC_REFER_HEADER = True

# 是否允许随机User-Agent # 随机User-Agent可能会导致无法建立默认会话 # 报错内容 Exceeded 30 redirects
ALLOW_RANDOM_USERAGENT = True

# 是否允许随机X-Forwarded-For
ALLOW_RANDOM_X_FORWARD = True

# 指定扫描时的Cookie
COOKIES = {
    # 'name1': 'value1',
    # 'name2': 'value2'
}
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


#######################################################################
# 每个自动动态筛选的变量,需要被忽略的默认值和空值
FILTER_MODULE_DEFAULT_VALUE_DICT = {
    "resp_text_title": ["Null-Title", "Ignore-Title", "Blank-Title"],
    "resp_text_hash": ["Null-Text-Hash", "Ignore-Text-Hash"],
    "resp_content_length": [-1, 0],
    "resp_text_size": [-1, 0],
    "resp_bytes_head": ["Null-Bytes", "Blank-Bytes"],
    "resp_redirect_url": ["Null-Redirect-Url", "Raw-Redirect-Url"],
}

# 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
EXCLUDE_STATUS = [404, 401, 403, 405, 406, 410, 500, 501, 502, 503]

# 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
EXCLUDE_REGEXP = r"页面不存在|未找到|not[ -]found|403|404|410"

# 动态排除模式：测试访问不存在路径,用于筛选出不正确的结果
# 动态判断404、假页面的 length、size、head、hash等多个属性来排除虚假页面
test_path_1 = get_random_str(12)
test_path_2 = get_random_str(12) + get_random_str(12)
test_path_3 = get_random_str(12) + get_random_str(12) + get_random_str(12)
TEST_PATH_LIST = [test_path_1, test_path_2, test_path_3]

# 动态排除模式开关
EXCLUDE_DYNAMIC_SWITCH = True

# HTTP 头设置
HEADERS = {
    'User-Agent': random_useragent(ALLOW_RANDOM_USERAGENT),
    'X_FORWARDED_FOR': random_x_forwarded_for(ALLOW_RANDOM_X_FORWARD),
    'Accept-Encoding': ''
}
########################扩展的调用函数###################################
# 自动创建文件字典目录
all_dict_dir = []
for dict_class in ALL_DICT_PATH:
    for dir_ in all_dir_name:
        all_dict_dir.append(os.path.join(dict_class, dir_))
for path in all_dict_dir:
    if not os.path.exists(path):
        os.makedirs(path)
########################扩展的调用函数###################################
