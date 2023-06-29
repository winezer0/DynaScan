#!/usr/bin/env python
# encoding: utf-8
import re

import setting_com
import setting_dict
import setting_http
from libs.input_const import *
from libs.lib_attribdict.config import CONFIG
from libs.lib_dyna_rule.base_rule_parser import RuleParser
from libs.lib_file_operate.file_path import get_dir_path_file_info_dict, file_name_remove_ext_list, \
    get_dir_path_dir_info_dict
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_log_print.logger_printer import output, LOG_ERROR, set_logger, LOG_INFO


# 检查每一行规则，是否符合基本变量替换规则 % XXX % 的形式
# 符合的话，看其在不在当前基本字典内, 不在的话提出警告

def base_rule_check(rule_line):
    status = True
    # 直接判断规则应该有的多个元素同时在列表内   # issubset 用于判断一个集合是否是另一个集合的子集。
    if {'{', '=', ':', '}', '$'}.issubset(set(list(rule_line))):
        # 如果行内存在合法的解析规则
        parser = RuleParser(rule_line)
        rule = parser.get_reg_rule()
        if rule:
            try:
                # 尝试解析规则
                rules, options = rule.split(':')
                _, _ = rules.split('=')
            except Exception as error:
                status = False
                if 'too many values to unpack' in str(error):
                    output(f"[-] 规则 {rule_line} 发生编写错误,每条规则仅支持单个格式规则!!!", level=LOG_ERROR)
                else:
                    output(f"[-] 规则 {rule_line} 发生未知解析错误!!! Error: {error}", level=LOG_ERROR)
        else:
            output(f"[!] 字典 {rule_line} 疑似解析规则,可能存在编写错误...", level=LOG_ERROR)
            status = False
    return status


def check_rule_base_var_format(dirs, base_vars):
    """
    检查 rule文件夹下的每一行规则，是否符合基本变量替换规则 %XXX%的形式
    符合的话，看其在不在当前基本字典内,不在的话提出警告
    :param dirs:
    :return:
    """
    error_rules_dict = {}

    # 定义正则表达式模式，使用圆括号括起要提取的部分
    base_var_pattern = r'(%[^%\s]+%)'
    # \w+，表示匹配一个或多个字母、数字或下划线
    # [\u4e00-\u9fa5] 表示匹配中文字符的 Unicode 编码范围
    # [^%\s]+，表示匹配一个或多个非 % 号、非空格的字符

    for base_var_dir, ext_list in dirs.items():
        file_info_dict = get_dir_path_file_info_dict(base_var_dir, ext_list=ext_list)
        for file_name, file_path in file_info_dict.items():
            output(f"[*] 正在检查 {file_path}")
            # 读取字典文件到列表
            rule_content = read_file_to_list(file_path)
            # output(f"[*] 文件 {file_name} 内容 {rule_content}")
            # 遍历列表提取每一条【%XXX%】规则,并判断是否在 all_base_var 内部
            for rule in rule_content:
                # output(f"[*] 检查规则 {rule}")
                rule_vars = re.findall(base_var_pattern, rule)
                if rule_vars:
                    # output(f"[*] 提取变量 {rule_vars}")
                    # 提取其中不存在的变量
                    diff_set = set(rule_vars) - set(base_vars)
                    if diff_set:
                        output(f"[!] 警告: 字典文件【{file_path}】 字典规则【{rule}】 发现非预期变量【{diff_set}】", level=LOG_ERROR)
                        error_rules_dict[f"{file_path}<-->{rule}"] = f"非预期变量 {diff_set}"
                # 进行规则解析测试
                rule_status = base_rule_check(rule)
                if not rule_status:
                    output(f"[!] 警告: 字典文件【{file_path}】 字典规则【{rule}】 进行规则解析错误", level=LOG_ERROR)
                    error_rules_dict[f"{file_path}<-->{rule}"] = "规则解析错误"
    return error_rules_dict


# 获取所有基本变量
def get_all_base_var(dirs):
    base_vars = []
    for base_var_dir, ext_list in dirs.items():
        file_info_dict = get_dir_path_file_info_dict(base_var_dir, ext_list=ext_list)
        for base_var_file_name in file_info_dict.keys():
            # 组装 {基本变量名: [基本变量文件内容列表]}
            base_var_pure_name = file_name_remove_ext_list(base_var_file_name, ext_list)
            base_vars.append(f"%{base_var_pure_name}%")
            # output(f"{base_var_file_name} <--> [%{base_var_pure_name}%]")

        dir_info_dict = get_dir_path_dir_info_dict(base_var_dir)
        for base_var_dir_name in dir_info_dict.keys():
            # 组装 {基本变量名: [基本变量文件内容列表]}
            base_vars.append(f"%{base_var_dir_name}%")
            # output(f"{base_var_dir_name} <--> [%{base_var_dir_name}%]")
    # 去重及排序
    base_vars = sorted(list(set(base_vars)))
    return base_vars


if __name__ == '__main__':
    # 加载初始设置参数
    setting_com.initialize(CONFIG)
    setting_http.initialize(CONFIG)
    setting_dict.initialize(CONFIG)

    # 根据用户输入的debug参数设置日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE],
               CONFIG[GB_LOG_ERROR_FILE],
               CONFIG[GB_LOG_DEBUG_FILE],
               True)

    base_dict_ext = [".lst"]
    base_dirs = {
        CONFIG[GB_BASE_DIR].joinpath("dict_base"): base_dict_ext,
    }

    rule_dirs = {
        CONFIG[GB_BASE_PATH_STR]: base_dict_ext,  # 直接字典
        CONFIG[GB_BASE_ROOT_STR]: base_dict_ext,  # 合并目录
    }

    # 1、获取所有基础变量
    all_base_var = get_all_base_var(base_dirs)
    output(f"[+] 目前所有基础变量【{len(all_base_var)}】个, 详情：{all_base_var}")

    # 扩充因变量字典
    all_base_var.extend(list(CONFIG[GB_BASE_REPLACE_DICT].keys()))  # 自定义 基本变量
    all_base_var.extend(list(CONFIG[GB_DEPENDENT_REPLACE_DICT].keys()))  # 动态因变量 及 自定义因变量

    output(f"[+] 目前所有替换变量【{len(all_base_var)}】个, 详情：{all_base_var}")

    # 2、检查每一行规则
    error_rules_info = check_rule_base_var_format(rule_dirs, all_base_var)
    if error_rules_info:
        output(f"[-] 发现错误变量|错误规则【{len(error_rules_info)}】个, 详情:{error_rules_info}", level=LOG_ERROR)
    else:
        output(f"[+] 没有发现错误变量|错误规则...", level=LOG_INFO)
