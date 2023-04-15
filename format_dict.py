#!/usr/bin/env python
# encoding: utf-8

# 格式化目录下的字典 （统计频率）
from libs.lib_log_print.logger_printer import output, LOG_INFO
from libs.lib_file_operate.file_write import write_path_list_to_frequency_file
from libs.lib_file_operate.file_path import get_dir_path_file_name
from libs.lib_file_operate.file_coding import file_encoding
from setting import *


# 去除不可见字符、频率倒序计算
def format_dict_dir(dict_dir_list, file_ext_list):
    dict_file_list = []
    for dict_dir in dict_dir_list:
        for dict_ext in file_ext_list:
            # 获取目录下所有【指定后缀的】文件
            file_list = get_dir_path_file_name(dict_dir, ext_list=dict_ext, relative=False)
            dict_file_list.extend(file_list)

    for dict_file in dict_file_list:
        output(f"[*] 格式化 {dict_file}",level=LOG_INFO)
        write_path_list_to_frequency_file(file_name=dict_file,
                                          path_list=[],
                                          encoding=file_encoding(dict_file),
                                          frequency_symbol=GB_FREQUENCY_SYMBOL,
                                          annotation_symbol=GB_ANNOTATION_SYMBOL,
                                          hit_over_write=True)


if __name__ == '__main__':
    dict_dirs = [GB_HIT_FILE_DIR, GB_BASE_VAR_DIR, GB_DIRECT_PATH_DIR, GB_GROUP_FOLDER_DIR, GB_GROUP_FILES_DIR]
    dict_ext_list = [GB_DICT_SUFFIX]  # '.txt'
    format_dict_dir(dict_dirs, dict_ext_list)
