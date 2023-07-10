#!/usr/bin/env python
# encoding: utf-8
# 解析输入参数

import argparse
from libs.lib_log_print.logger_printer import output, LOG_ERROR, LOG_INFO


def extract_heads(param_len, param_dict):
    # 实现提取字符串首字母的函数,作为参数名, 需要考虑重复问题
    initials = [word[0] for word in param_len.split("_")]  # 提取每个单词的首字母
    initials = "".join(initials)  # 将所有首字母拼接成一个字符串

    # 需要 param_dict 字典的值是短参数名
    if initials not in param_dict.values():
        return initials
    else:
        # 处理重复项问题
        i = 0
        while True:
            i += 1
            new_initials = f"{initials}{i}"
            if new_initials not in param_dict.values():
                break
        return new_initials


def config_dict_add_args(config_dict, args):
    # 使用字典解压将参数 直接赋值给相应的全局变量
    # 要求args参数命名要和字典的键 统一（完全相同或可以变为完全相同）
    for param_name, param_value in vars(args).items():
        var_name = f"GB_{param_name.upper()}"
        try:
            # globals()[var_name] = param_value # 赋值全局变量,仅本文件可用
            # output(f"[*] INPUT:{var_name} -> {param_value}", level=LOG_ERROR)
            config_dict[var_name] = param_value  # 赋值全局字典,所有文件可用
            if var_name not in config_dict.keys():
                output(f"[-] 非预期参数将被赋值: {var_name} <--> {param_value}", level=LOG_ERROR)
        except Exception as error:
            output(f"[!] 更新参数发生错误: {error}", level=LOG_ERROR)
            exit()
    return


def show_config_dict(config_dict):
    # 输出 config 字典
    for index, param_name in enumerate(config_dict.keys()):
        param_val = config_dict[param_name]
        output(f"[*] Param_{index} {param_name} <--> {param_val}", level=LOG_INFO)


class StoreReverse(argparse.Action):
    """
    基于默认值自动取反的动作, 如默认True,则返回false
    """

    def __init__(self, option_strings, dest, default=False, required=False, help=None):
        super(StoreReverse, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=True,
            default=default,
            required=required,
            help=help
        )

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, not self.default)
