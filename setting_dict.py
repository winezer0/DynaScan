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
# 读取字典文件时的处理
# 指定path和频率的分隔符,如果每一行的内容为/xxx/xxx  <-->10,那么切割符为'<-->'
GB_FREQUENCY_SYMBOL = '<-->'

# 要提取的最小路径频率阈值，大于等于 FREQUENCY_MIN 小于等于 FREQUENCY_MAX 的字典会被提取
FREQUENCY_MIN = 1

# 字典的行注释符号
GB_ANNOTATION_SYMBOL = '#'
##################################################################