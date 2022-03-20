#!/usr/bin/env python
# encoding: utf-8

# 全局配置文件
import os
import random
import pathlib
import time

from libs.Data import config
# 使用config存储主要的设置用户变量更加优雅,注意使用config存储logger后会导致不能用logger打印config,由于死循环调用的问题
# 所有需要用户输入的变量[就是说cmd直接解析的参数,非直接解析的参数不需要加],需要添加config.作为前缀,
from libs.ToolUtils import get_random_str

##################################################################
# 获取setting.py脚本所在路径作为的基本路径
BASE_DIR = pathlib.Path(__file__).parent.resolve()

# 是否属于测试模式 # 测试模式每个目标URL只获取生成的前100个URL进行测试
TEST_MODE_HANDLE = False  # True False

# 默认设置日志显示级别 # False 输出INFO级别信息 True 显示DEBUG级别信息
config.debug = False  # True False
##################################################################
# 版本号配置
version = "Ver 0.1.2 2022-03-19 00:54"

##################################################################
# 请求编码设置 设置当前的编码 #已弃用
# NOW_ENCODE = 'utf-8'

# 中文路径、特殊字符会以列表内的编码作为基础编码，再进行URL编码
ALL_BASE_ENCODE = ['utf-8', 'gb2312']

# 是否对所有最终PATH开启URL编码模式,解决中文路径乱码问题
ENCODE_ALL_PATH = True

# URL路径列表编码处理包含两种模式,一种是仅处理中文路径（使用正则匹配出中文）,一种是所有路径都会处理,所有特殊字符都会被编码,
# 是否仅对包含中文的路径使用URL编码模式
ENCODE_CHINESE_ONLY = True # True # False
##################################################################
# 在配置文件中输入目标文件等参数 比cmd输入参数优先级低 一般作为默认参数使用
config.target = None
config.target_file = "target.txt"
####################程序基本配置开始##################################
# 是否对符合URL格式的目标直接开启目标URL可访问性判断
ACCESS_TEST_URL = True

# 是否对HOST:PORT格式的目标进行URL访问模式,根据响应结果自动添加协议头
ACCESS_ADD_PROTO_HEAD = True

# 是否URL访问模式的基础上,进一步判断不同协议的返回结果是否相同,最终确定是否添加https协议头
SMART_ADD_PROTO_HEAD = True

# 是否开启多目标模式  # 对URL路径进行分解,一个目标能够变成多个目标,每多一个目标,请求URL就会多一倍
# https://baike.baidu.com/item/DD/ 会被分解为 https://baike.baidu.com/item/DD/,https://baike.baidu.com/item/,https://baike.baidu.com/
MULTI_TARGET_PATH_MODE = False

# 程序开始运行时间
RUN_TIME = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

# 设置日志输出文件路径 #目录不存在会自动创建
info_log_file_path = BASE_DIR.joinpath("runlog/runlog_{time}_info.log".format(time=RUN_TIME))
dbg_log_file_path = BASE_DIR.joinpath("runlog/runlog_{time}_debug.log".format(time=RUN_TIME))
err_log_file_path = BASE_DIR.joinpath("runlog/runlog_{time}_error.log".format(time=RUN_TIME))

# 设置输出结果文件目录
result_dir_path = BASE_DIR.joinpath("result")
if not os.path.exists(result_dir_path): os.makedirs(result_dir_path)

# 字典来自文件列表 #从文件夹获得所有文件列表
dir_base_var = 'dict/base_var'
dir_direct_path = 'dict/direct_path'
dir_combin_folder = 'dict/combin_folder'
dir_combin_files = 'dict/combin_files'

# 字典文件后缀
dict_file_suffix = '.lst'

# 是否读取DIRECT目录下的字典
DIRECT_DICT_MODE = True

# 指定仅读取的 direct 目录指定的文件字典,,不再读取 direct 目录下的所有文件
SPECIFY_DIRECT_DICT = []

# 指定仅读取 combin-xxx目录指定的文件字典,不再读取 combin-xxx 目录下的所有文件
SPECIFY_COMBIN_FOLDER_DICT = []
SPECIFY_COMBIN_FILES_DICT = []

# 是否读取COMBIN-XX目录下的字典
COMBIN_DICT_MODE = True

# 要提取的路径频率阈值，大于等于FREQUENCY_MIN 小于等于 FREQUENCY_MAX的字典会被提取
# 读取命中的后缀文件时的频率阈值 # 由于后缀文件不好进行进一步的解析,所以加到每个后缀以后
FREQUENCY_MIN_HIT = 1
FREQUENCY_MAX_HIT = 999
# 是否将历史命中扩展的值扩展到每一个基本变量中
APPEND_HIT_EXT = True

# 读取BASE目录下字典时的频率阈值
FREQUENCY_MIN_BASE = 1
FREQUENCY_MAX_BASE = 999

# 读取DIRECT目录下字典时的频率阈值
FREQUENCY_MIN_DIRECT = 1
FREQUENCY_MAX_DIRECT = 999

# 读取COMBIN目录下字典时的频率阈值
FREQUENCY_MIN_COMBIN = 1
FREQUENCY_MAX_COMBIN = 99

# 指定path和频率的分隔符,如果每一行的内容为/xxx/xxx  frequency==10,那么切割符为'frequency=='
SEPARATOR = 'frequency=='

# 如果结果字典中已有的值,是否进行追加频率,False时直接进行频率覆盖
ADDITIONAL = True

# 行注释符号
ANNOTATION = '#'
# 替换字符列表-不再需要手动指定－从文件名和文件内容中自动提取键值对
# 自动读取base目录所有文件并进行自动赋值

# 因变量替换对应表,初值为空,后根据URL变量自动填充替换
# replace_dict = {"%DOMAIN%": [], "%PATH%": [] }
# %%DOMAIN%% 在URL中,域名因变量列表所代表的字符串
# %%PATH%% 在URL中,路径因变量列表所代表的字符串
# 由于需要动态改变,因此时在代码内部实现,

# 域名变量如果是IP是否需要忽略
IGNORE_IP_FORMAT = True

# 存储自定义变量单词,会自动加入到%%DOMAIN%% 和%%PATH%% 中
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
    ".": ["_"]   # 获取的路径相关单词中的[.]会替换为[_]
}

# 路径中不该有的字符 # 解析出来的域名单词和路径单词中有这个符号的元素会删除
NOT_PATH_SYMBOL= [":"]

# 是否去除路径中包含不该有的字符（比如:）的元素
REMOVE_NOT_PATH_SYMBOL = True


# 是否替换路径中的多个//为一个/
REMOVE_MULTI_SLASHES = True

# 命中文件保存路径
hit_ext_path = dir_base_var + '/' + 'HIT_EXT' + dict_file_suffix
hit_direct_path = dir_direct_path + '/' + 'HIT_DIRECT' + dict_file_suffix
hit_folder_path = dir_combin_folder + '/' + 'HIT_FLODER' + dict_file_suffix
hit_files_path = dir_combin_files + '/' + 'HIT_FILE' + dict_file_suffix

# 是否保存命中结果到HIT_XXX文件
SAVE_HIT_RESULT = True # False # True
####################无需进行处理的初始变量赋值开始###########################
# 代码中会自动添加基本变量替换关键字
# #不需要手动填写因变量关键字,但是手动实现因变量函数
ALL_REPLACE_KEY = []

# 全局变量,用于存储请求所有已经访问过的目标URL
ALL_ACCESSED_URL = []

# 全局变量,存储基本变量替换字典
BASE_VAR_REPLACE_DICT = {}
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

# 是否允许随机User-Agent
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
# 每个筛选的变量,需要被忽略的默认值和空置
FILTER_MOUDLE_DEFAULT_VALUE_DICT = {
    "resp_text_title": ["Null-Title", "Ignore-Title", "Blank-Title"],
    "resp_text_hash": ["Null-Text-Hash", "Ignore-Text-Hash"],
    "resp_content_length": [-1, 0],
    "resp_text_size": [-1, 0],
    "resp_bytes_head": ["Null-Bytes", "Blank-Bytes"]}

# 判断URI不存在的状态码，多个以逗号隔开,符合该状态码的响应将不会写入结果文件
EXCLUDE_STATUS = [404]

# 判断URI是否不存在的正则，如果页面标题存在如下定义的内容，将从Result结果中剔除到ignore结果中 #re.IGNORECASE 忽略大小写
EXCLUDE_REGEXP = r"页面不存在|未找到|404|410|not[ -]found"

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
list__ = [dir_base_var, dir_direct_path, dir_combin_folder, dir_combin_files]
for path in list__:
    if not os.path.exists(path):
        os.makedirs(path)
########################扩展的调用函数###################################

