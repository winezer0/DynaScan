#!/usr/bin/env python
# encoding: utf-8
from pathlib import Path
import time
from libs.input_const import *
from libs.lib_dyna_rule.dyna_rule_const import *


def initialize(config):
    # 需要读取的字典文件后缀 通过file.endswith匹配
    config[GB_DICT_SUFFIX] = ['.lst']
    # 基本变量文件路径
    config[GB_BASE_VAR_DIR] = config[GB_BASE_DIR].joinpath("dict_base")
    # 设置默认调用的字典目录
    config[GB_DICT_RULE_PATH] = config[GB_BASE_DIR].joinpath("dict_rule")
    ###########################
    # 默认调用的字典目录
    config[GB_DICT_RULE_SCAN] = None  # 为空表示所有目录
    # 基于当前目录、进行拼接扫描的字典
    config[GB_BASE_PATH_STR] = config[GB_DICT_RULE_PATH].joinpath("{RULE_DIR}", STR_BASE_PATH).as_posix()
    # 基于根目录、进行拼接扫描的字典
    config[GB_BASE_ROOT_STR] = config[GB_DICT_RULE_PATH].joinpath("{RULE_DIR}", STR_BASE_ROOT).as_posix()
    # 开启基于根目录的文件字典读取
    config[GB_SCAN_BASE_ROOT] = True
    # 开启基于当前目录下的文件字典读取
    config[GB_SCAN_BASE_PATH] = True
    ###########################
    # 指定path和频率的分隔符,如果每一行的内容为/xxx/xxx  <-->10,那么切割符为'<-->'
    config[GB_FREQUENCY_SYMBOL] = '<-->'
    # 要提取的最小路径频率阈值，大于等于 FREQUENCY_MIN 的字典会被提取
    config[GB_FREQUENCY_MIN] = 10
    # 字典文件的行注释符号
    config[GB_ANNOTATION_SYMBOL] = '#'

    ##################################################################
    # 存储自定义基本变量  # 已弃用
    config[GB_BASE_REPLACE_DICT] = {}
    #########################
    # 存储自定义 因变量 # 考虑都合并到 DEPENDENT
    config[GB_DEPENDENT_REPLACE_DICT] = {
        STR_VAR_DEPENDENT: [],  # 存储自定义因变量  %%DEPENDENT%%
        STR_VAR_BLANK: [''],  # 存储空字符-默认存储   %%BLANK%%
        # STR_VAR_DOMAIN: [],  # 存储动态PATH因变量-自动生成-自动生成  %%DOMAIN%%
        # STR_VAR_PATH: [],  # 存储动态域名因变量-自动生成-自动生成  %%PATH%%
        # STR_VAR_FILE_NAME: [],  # 存储文件名变量-带扩展-自动生成  %%FILE_NAME%%
        # STR_VAR_PURE_NAME: [],  # 存储文件名变量-无扩展-自动生成  %%PURE_NAME%%
    }

    # DOMAIN PATH 因变量中的 符号替换规则, 替换后追加到域名因子列表
    config[GB_SYMBOL_REPLACE_DICT] = {":": ["_"], ".": ["_"]}
    # 删除带有 特定符号 的因变量（比如:）的元素
    config[GB_NOT_ALLOW_SYMBOL] = [":"]
    # 当域名是IP时,忽略从域名获取因变量
    config[GB_IGNORE_IP_FORMAT] = True
    ##################################################################
    # 中文路径、特殊字符会以列表内的编码作为基础编码，再进行URL编码
    config[GB_CHINESE_ENCODE] = ['utf-8']  # ['utf-8', 'gbk', 'gb2312']
    # 注意:gb2312编码繁体中文可能报错,此时可使用gbk编码,GBK与G2312编码结果相同
    # 是否仅对包含中文的路径使用URL编码模式,默认True 否则所有路径都会处理,所有特殊字符都会被编码,
    config[GB_ONLY_ENCODE_CHINESE] = True
    ##################################################################
    ##################################################################
    # 最终生成的扫描路径处理、过滤、格式化
    # 替换路径中的多个//为一个/
    config[GB_REMOVE_MULTI_SLASHES] = True
    # 去除以特定字符结尾的URL
    config[GB_REMOVE_END_SYMBOLS] = ['.']
    # URL路径全部小写
    config[GB_URL_PATH_LOWERCASE] = True
    # 为每个路径添加自定义前缀 # 例如 ['/admin']
    config[GB_CUSTOM_URL_PREFIX] = None
    # 仅扫描指定后缀的URL目标,注意:后缀不需要加[.] # 例如 ['php','html']
    config[GB_ONLY_SCAN_SPECIFY_EXT] = None
    # 仅移除指定后缀的URL, 注意:后缀不需要加[.] # 例如 ['php','html']
    config[GB_NO_SCAN_SPECIFY_EXT] = None
    # 当保留指定后缀和移除指定后缀同时存在时,先进行指定后缀URL保留,后进行指定后缀URL排除
    ##################################################################
