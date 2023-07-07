#!/usr/bin/env python
# encoding: utf-8
import setting_com
import setting_dict
import setting_http
from libs.input_const import *
from libs.lib_attribdict.config import CONFIG
from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_path import get_dir_path_file_info_dict
from libs.lib_file_operate.file_write import write_path_list_to_frequency_file
from libs.lib_log_print.logger_printer import output, set_logger


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
                                          frequency_symbol="<-->",
                                          annotation_symbol="###",
                                          hit_over_write=True)


if __name__ == '__main__':
    # 加载初始设置参数
    setting_com.init_custom(CONFIG)
    setting_http.init_custom(CONFIG)
    setting_dict.init_custom(CONFIG)

    # 根据用户输入的debug参数设置日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE],
               CONFIG[GB_LOG_ERROR_FILE],
               CONFIG[GB_LOG_DEBUG_FILE],
               True)

    dirs_dict = {
        CONFIG[GB_BASE_DIR].joinpath("dict_hit"): CONFIG.GB_DICT_SUFFIX,  # 命中文件目录
        CONFIG[GB_BASE_DIR].joinpath("dict_base"): CONFIG.GB_DICT_SUFFIX,  # 基本变量目录
        CONFIG[GB_BASE_DIR].joinpath("dict_rule"):CONFIG.GB_DICT_SUFFIX,  # 直接字典
    }

    # 格式化目录下的字典 （统计频率）
    format_dicts(dirs_dict)
