#!/usr/bin/env python
# encoding: utf-8

# 获取基本变量 替换字典
import copy
import os

from libs.lib_rule_dict.util_dict import dict_content_base_rule_render
from libs.util_file import get_dir_path_file_name, read_file_to_list, file_encoding, read_file_to_frequency_dict


def set_base_var_dict(base_var_dir,
                      dict_suffix,
                      base_replace_dict):
    base_var_replace_dict = copy.copy(base_replace_dict)
    # 获取文件名
    base_var_file_list = get_dir_path_file_name(base_var_dir, ext=dict_suffix)
    # print(base_var_file_list)

    # 生成文件名对应基础变量
    # 并 同时读文件组装 {基本变量名: [基本变量文件内容列表]}
    for base_var_file_name in base_var_file_list:
        base_file_pure_name = base_var_file_name.rsplit(dict_suffix, 1)[0]
        base_var_name = f'%{base_file_pure_name}%'

        # 读文件到列表
        base_var_file_path = os.path.join(base_var_dir, base_var_file_name)
        base_var_file_content = read_file_to_list(base_var_file_path,
                                                  encoding=file_encoding(base_var_file_path),
                                                  de_strip=True,
                                                  de_weight=True,
                                                  de_unprintable=True)

        # 组装 {基本变量名: [基本变量文件内容列表]}
        base_var_replace_dict[base_var_name] = base_var_file_content

    # 对 内容列表 中的规则进行 进行 动态解析
    base_var_replace_dict = dict_content_base_rule_render(base_var_replace_dict)

    return base_var_replace_dict



