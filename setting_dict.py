#!/usr/bin/env python
# encoding: utf-8

##################################################################
# 扫描字典设置
# 基本变量字典目录
import os
import pathlib

##################################################################
# 获取setting.py脚本所在路径作为的基本路径
GB_BASE_DIR = pathlib.Path(__file__).parent.resolve()

GB_BASE_VAR_DIR = GB_BASE_DIR.joinpath("dict_base")
# 设置默认调用的字典目录
GB_DICT_PATH = GB_BASE_DIR.joinpath("dict_rule")
# 常规直接字典路径
GB_DIRECT_PATH_DIR = os.path.join(GB_DICT_PATH, "direct_path")

# 读取DIRECT目录下的字典
GB_ADD_DIRECT_DICT = True

# 组合-目录字典路径
GB_GROUP_FOLDER_DIR = os.path.join(GB_DICT_PATH, "group_folder")
# 组合-文件 字典路径
GB_GROUP_FILES_DIR = os.path.join(GB_DICT_PATH, "group_files")

# 读取GROUP_XX目录下的字典
GB_ADD_GROUP_DICT = True

# 大中小字典模式 通过后缀区分  max|mid|min
GB_DICT_FILE_MODE = 'mid'

# 需要读取的字典文件后缀
# GB_DICT_FILE_EXT = f'.{GB_DICT_FILE_MODE}.lst'
GB_DICT_FILE_EXT = f'.lst'
##################################################################
# 存储自定义 基本变量
GB_BASE_VAR_REPLACE_DICT = {"%BLANK%": ['']}

# 存储自定义 因变量
GB_DEPENDENT_VAR_REPLACE_DICT = {"%%DEPENDENT%%": ['admin', 'product', 'wwwroot', 'www', '网站']}
# 程序内置 %%DOMAIN%% 在URL中,域名因变量列表所代表的字符串
# 程序内置 %%PATH%% 在URL中,路径因变量列表所代表的字符串

# DOMAIN PATH 因变量中的 符号替换规则, 替换后追加到域名因子列表
GB_SYMBOL_REPLACE_DICT = {":": ["_"], ".": ["_"]}

# 删除带有 特定符号 的因变量（比如:）的元素
GB_NOT_ALLOW_SYMBOL = [":"]

GB_IGNORE_IP_FORMAT = True
##################################################################
# 读取字典文件时的处理
# 指定path和频率的分隔符,如果每一行的内容为/xxx/xxx  <-->10,那么切割符为'<-->'
GB_FREQUENCY_SYMBOL = '<-->'

# 要提取的最小路径频率阈值，大于等于 FREQUENCY_MIN 小于等于 FREQUENCY_MAX 的字典会被提取
FREQUENCY_MIN = 1

# 字典的行注释符号
GB_ANNOTATION_SYMBOL = '#'
##################################################################
# 命中文件保存路径
GB_HIT_FILE_DIR = GB_BASE_DIR.joinpath("dict_hit")
# 存储命中的后缀
GB_HIT_EXT_FILE = os.path.join(GB_HIT_FILE_DIR, 'HIT_EXT.hit')
# 存储命中的路径
GB_HIT_DIRECT_FILE = os.path.join(GB_HIT_FILE_DIR, 'HIT_DIRECT.hit')
# 存储命中的目录
GB_HIT_FOLDER_FILE = os.path.join(GB_HIT_FILE_DIR, 'HIT_FOLDER.hit')
# 存储命中的文件
GB_HIT_FILES_FILE = os.path.join(GB_HIT_FILE_DIR, 'HIT_FILE.hit')

# 是否保存命中结果到HIT_XXX文件
SAVE_HIT_RESULT = True

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
# 最终生成的扫描路径处理
# 替换路径中的多个//为一个/
GB_REMOVE_MULTI_SLASHES = True

# 去除以特定字符结尾的URL
GB_REMOVE_SOME_SYMBOL = ['.']

# URL路径全部小写
GB_URL_PATH_LOWERCASE = True

# 为每个路径添加自定义前缀 # 例如 ['/admin']
GB_ADD_CUSTOM_PREFIX = None

# 仅扫描指定后缀的URL目标,注意:后缀不需要加[.] # 例如 ['php','html']
GB_ONLY_SCAN_SPECIFY_EXT = None

# 仅移除指定后缀的URL, 注意:后缀不需要加[.] # 例如 ['php','html']
GB_NO_SCAN_SPECIFY_EXT = None
# 当保留指定后缀和移除指定后缀同时存在时,先进行指定后缀URL保留,后进行指定后缀URL排除
##################################################################
