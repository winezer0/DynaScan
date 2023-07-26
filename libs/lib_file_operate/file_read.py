#!/usr/bin/env python
# encoding: utf-8

import os

from libs.lib_file_operate.file_coding import file_encoding


def remove_unprintable_chars(str_):
    """
    去除列表元素的\u200b等字符
    https://blog.csdn.net/lly1122334/article/details/107615950
    """
    if str_.isprintable():
        return str_
    else:
        new_path = ''.join(x for x in str_ if x.isprintable())
        return new_path


def read_file_to_list(file_path, encoding=None, de_strip=True, de_weight=False, de_unprintable=False):
    # 文本文件处理 读文件到列表
    result_list = []
    if os.path.exists(file_path):
        # 自动获取文件编码
        if not encoding:
            encoding = file_encoding(file_path)

        with open(file_path, 'r', encoding=encoding) as f:
            for line in f.readlines():
                if line.strip():
                    # 开启字符串空字符整理
                    if de_strip:
                        line = line.strip()
                    # 去除不可见字符
                    if de_unprintable:
                        line = remove_unprintable_chars(line)
                    result_list.append(line)

    # 开启去重 # Python 列表数据去重并保留顺序 https://zhuanlan.zhihu.com/p/421797997
    if result_list and de_weight:
        result_list = sorted(set(result_list), key=result_list.index)

    return result_list


def read_file_to_str(file_path, encoding=None, de_strip=False, de_unprintable=False):
    # 读取文件内容并返回字符串
    result_str = ""

    if os.path.exists(file_path):
        # 自动获取文件编码
        if not encoding:
            encoding = file_encoding(file_path)

        with open(file_path, 'r', encoding=encoding) as f_obj:
            result_str = f_obj.read()

            # 去除空字符结尾
            if de_strip:
                result_str = result_str.strip()

            # 去除不可见字符
            if de_unprintable:
                result_str = remove_unprintable_chars(result_str)

    return result_str


def read_file_to_dict(file_path, encoding=None, de_strip=True, de_unprintable=False, split_symbol=","):
    """
    简单读取文件到字典,以指定字符进行分隔
    :param file_path: 文件路径
    :param encoding: 文件编码
    :param de_strip: 去除两端空白字符
    :param de_unprintable: 去除不可见字符
    :param split_symbol: 键值对分割符号
    :return:
    """
    result_dict = {}
    if os.path.exists(file_path):
        # 自动获取文件编码
        if not encoding:
            encoding = file_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f_obj:
            lines = f_obj.readlines()
            for line in lines:
                # 去除不可见字符
                if de_unprintable:
                    line = remove_unprintable_chars(line)

                # 分割csv
                key = line.split(split_symbol)[0]
                value = line.split(split_symbol)[-1]

                # strip空白字符
                if de_strip:
                    key = key.strip()
                    value = value.strip()

                result_dict[key] = value
    return result_dict


def read_files_to_list(file_list, encoding=None, de_strip=True, de_weight=False, de_unprintable=False):
    # 文本文件处理 读文件到列表
    result_list = []
    # 循环读取每个文件
    for file_path in file_list:
        file_content = read_file_to_list(file_path,
                                         encoding=encoding,
                                         de_strip=de_strip,
                                         de_weight=de_weight,
                                         de_unprintable=de_unprintable)
        result_list.extend(file_content)

    # 最终去重
    if result_list and de_weight:
        result_list = sorted(set(result_list), key=result_list.index)

    return result_list


