#!/usr/bin/env python
# encoding: utf-8

import pathlib
from libs.lib_dyna_rule.dyna_rule_const import *

##################################################################
# 获取setting.py脚本所在路径作为的基本路径
GB_BASE_DIR = pathlib.Path(__file__).parent.resolve()
##################################################################
# 扫描字典设置
# 基本变量文件路径
GB_BASE_VAR_DIR = GB_BASE_DIR.joinpath("dict_base")

# 设置默认调用的字典目录
GB_DICT_RULE_PATH = GB_BASE_DIR.joinpath("dict_rule")
STR_BASE_PATH = "base_path"
STR_BASE_ROOT = "base_root"
GB_BASE_PATH_STR = str(GB_DICT_RULE_PATH.joinpath("{RULE_DIR}", STR_BASE_PATH))   # 基于当前目录、进行拼接扫描的字典
GB_BASE_ROOT_STR = str(GB_DICT_RULE_PATH.joinpath("{RULE_DIR}", STR_BASE_ROOT))   # 基于根目录、进行拼接扫描的字典

# 默认扫描的目录
GB_DICT_RULE_SCAN = None  # 为空表示所有目录
###########################
# 需要读取的字典文件后缀 通过file.endswith匹配
GB_DICT_SUFFIX = ['.lst']
###########################
# 读取字典文件时的处理
# 指定path和频率的分隔符,如果每一行的内容为/xxx/xxx  <-->10,那么切割符为'<-->'
GB_FREQUENCY_SYMBOL = '<-->'
# 要提取的最小路径频率阈值，大于等于 FREQUENCY_MIN 小于等于 FREQUENCY_MAX 的字典会被提取
GB_FREQUENCY_MIN = 10
# 字典文件的行注释符号
GB_ANNOTATION_SYMBOL = '#'
##################################################################
# 存储自定义 基本变量
GB_BASE_REPLACE_DICT = {}
#########################
# 存储自定义 因变量 # 考虑都合并到 DEPENDENT
GB_DEPENDENT_REPLACE_DICT = {
    STR_VAR_DEPENDENT:['admin', 'product', 'wwwroot', 'www', '网站'],  # 存储自定义因变量
    STR_VAR_DOMAIN: [],  # 存储动态PATH因变量-自动生成
    STR_VAR_PATH: [],  # 存储动态域名因变量-自动生成
    STR_VAR_BLANK: [''],  # 存储空字符
}

# DOMAIN PATH 因变量中的 符号替换规则, 替换后追加到域名因子列表
GB_SYMBOL_REPLACE_DICT = {":": ["_"], ".": ["_"]}
# 删除带有 特定符号 的因变量（比如:）的元素
GB_NOT_ALLOW_SYMBOL = [":"]
# 当域名是IP时,忽略从域名获取因变量
GB_IGNORE_IP_FORMAT = True
##################################################################
# 命中文件保存路径
GB_HIT_FILE_DIR = GB_BASE_DIR.joinpath("dict_hit")
# 存储命中的后缀
GB_HIT_EXT_FILE = GB_HIT_FILE_DIR.joinpath('HIT_EXT.hit')
# 存储命中的路径
GB_HIT_DIRECT_FILE = GB_HIT_FILE_DIR.joinpath('HIT_DIRECT.hit')
# 存储命中的目录
GB_HIT_FOLDER_FILE = GB_HIT_FILE_DIR.joinpath('HIT_FOLDER.hit')
# 存储命中的文件
GB_HIT_FILES_FILE = GB_HIT_FILE_DIR.joinpath('HIT_FILE.hit')
# 是否保存命中结果到HIT_XXX文件
GB_SAVE_HIT_RESULT = True
# 命中结果文件追加模式
GB_HIT_OVER_CALC = True
# True,计算频率后覆盖写入、后期写入时内存占用大,磁盘占用小,读取效率高
# False 直接追加命中记录、后期写入时内存占用小,磁盘占用大,读取效率低
##################################################################
# 中文路径、特殊字符会以列表内的编码作为基础编码，再进行URL编码
GB_CHINESE_ENCODE = ['utf-8']  # ['utf-8', 'gbk', 'gb2312']
# 注意:gb2312编码繁体中文可能报错,此时可使用gbk编码,GBK与G2312编码结果相同

# 是否仅对包含中文的路径使用URL编码模式,默认True 否则所有路径都会处理,所有特殊字符都会被编码,
GB_ONLY_ENCODE_CHINESE = True
##################################################################
# 最终生成的扫描路径处理、过滤、格式化
# 替换路径中的多个//为一个/
GB_REMOVE_MULTI_SLASHES = True

# 去除以特定字符结尾的URL
GB_REMOVE_END_SYMBOLS = ['.']

# URL路径全部小写
GB_URL_PATH_LOWERCASE = True

# 为每个路径添加自定义前缀 # 例如 ['/admin']
GB_CUSTOM_URL_PREFIX = None

# 仅扫描指定后缀的URL目标,注意:后缀不需要加[.] # 例如 ['php','html']
GB_ONLY_SCAN_SPECIFY_EXT = None

# 仅移除指定后缀的URL, 注意:后缀不需要加[.] # 例如 ['php','html']
GB_NO_SCAN_SPECIFY_EXT = None
# 当保留指定后缀和移除指定后缀同时存在时,先进行指定后缀URL保留,后进行指定后缀URL排除
##################################################################
