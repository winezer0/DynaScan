#!/usr/bin/env python
# encoding: utf-8

# 获取基本变量 替换字典
import copy
import os

from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_path import get_dir_path_file_name
from libs.lib_file_operate.file_read import read_file_to_list, read_file_to_frequency_dict
from libs.lib_dyna_rule.dyna_rule_tools import dict_content_base_rule_render, get_key_list_with_frequency


def set_base_var_dict(base_var_dir,
                      dict_suffix,
                      base_replace_dict):
    # 保留原有字典
    base_var_replace_dict = copy.copy(base_replace_dict)
    # 获取文件名
    base_var_file_list = get_dir_path_file_name(base_var_dir, ext_list=dict_suffix)
    # print(base_var_file_list)

    # 生成文件名对应基本变量
    # 并 同时读文件组装 {基本变量名: [基本变量文件内容列表]}
    for base_var_file_name in base_var_file_list:
        base_file_pure_name = os.path.basename(base_var_file_name)
        base_file_pure_name = base_file_pure_name.rsplit('.',1)[0]
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


# 获取基本变量替换字典
def set_base_var_dict_frequency(base_var_dir,
                                dict_suffix,
                                base_replace_dict,
                                frequency_symbol,
                                annotation_symbol,
                                frequency_min):
    """
    # 1 读取 所有基本替换变量字典 到频率字典
    # 2 按频率筛选 并加入到 基本变量替换字典
    # 3 对 基本变量替换字典 进行规则解析
    """
    base_var_replace_dict = copy.copy(base_replace_dict)
    # 获取文件名
    base_var_file_list = get_dir_path_file_name(base_var_dir, ext_list=dict_suffix)

    # 生成文件名对应基本变量
    # 并 同时读文件组装 {基本变量名: [基本变量文件内容列表]}
    for base_var_file_name in base_var_file_list:
        base_file_pure_name = base_var_file_name.rsplit('.', 1)[0]
        base_file_pure_name = base_file_pure_name.rsplit('.',1)[0]
        base_var_name = f'%{base_file_pure_name}%'

        # 读文件到列表
        base_var_file_path = os.path.join(base_var_dir, base_var_file_name)
        # 获取频率字典 # 筛选频率字典
        frequency_dict = read_file_to_frequency_dict(base_var_file_path,
                                                     encoding=file_encoding(base_var_file_path),
                                                     frequency_symbol=frequency_symbol,
                                                     annotation_symbol=annotation_symbol)
        frequency_list = get_key_list_with_frequency(frequency_dict, frequency_min)
        # 组装 {基本变量名: [基本变量文件内容列表]}
        base_var_replace_dict[base_var_name] = frequency_list

    # 对 内容列表 中的规则进行 进行 动态解析
    base_var_replace_dict = dict_content_base_rule_render(base_var_replace_dict)

    return base_var_replace_dict
