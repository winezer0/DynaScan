#!/usr/bin/env python
# encoding: utf-8

from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_path import get_dir_path_file_info_dict
from libs.lib_file_operate.file_write import write_path_list_to_frequency_file
from libs.lib_log_print.logger_printer import output, LOG_INFO, set_logger
from setting_total import *


def format_dicts(dict_dirs):
    """去除不可见字符、频率倒序计算"""
    dict_file_list = []
    for dir_path, ext_list in dict_dirs.items():
        for dict_ext in ext_list:
            # 获取目录下所有【指定后缀的】文件
            file_info_dict = get_dir_path_file_info_dict(dir_path, ext_list=dict_ext)
            dict_file_list.extend(list(file_info_dict.values()))

    for dict_file in dict_file_list:
        output(f"[*] 格式化字典文件 {dict_file}")
        write_path_list_to_frequency_file(file_path=dict_file,
                                          path_list=[],
                                          encoding=file_encoding(dict_file),
                                          frequency_symbol=GB_FREQUENCY_SYMBOL,
                                          annotation_symbol=GB_ANNOTATION_SYMBOL,
                                          hit_over_write=True)


if __name__ == '__main__':
    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    set_logger(GB_INFO_LOG_STR, GB_ERROR_LOG_STR, GB_DEBUG_LOG_STR, True)

    dirs_dict = {
        GB_HIT_FILE_DIR: GB_DICT_SUFFIX,  # 命中文件目录
        GB_BASE_VAR_DIR: GB_DICT_SUFFIX,  # 基本变量目录
        GB_DICT_RULE_PATH: GB_DICT_SUFFIX,  # 直接字典
    }

    # 格式化目录下的字典 （统计频率）
    format_dicts(dirs_dict)
