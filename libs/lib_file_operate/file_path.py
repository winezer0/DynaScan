#!/usr/bin/env python
# encoding: utf-8

import os
from pathlib import Path


def auto_make_dir(path):
    # 自动创建目录
    if not os.path.exists(path):
        os.makedirs(path)


def file_is_exist(filepath):
    # 判断文件是否存在
    if filepath:
        path = Path(filepath)
        if path.is_file():
            return True
        else:
            return False


# 获取目录下的文件列表,返回目录下的文件名列表【相对路径】
def get_dir_path_file_name(file_dir, ext_list=['.txt'], relative=True):
    """
    获取目录下的文件列表,返回目录下的文件名列表
    处理 输入的扩展后缀, 预期是一个后缀列表
    """
    if ext_list and isinstance(ext_list, str):
        ext_list = [ext_list]

    file_list = []
    for root, dirs, files in os.walk(file_dir):
        """
        root #当前目录路径
        dirs #当前路径下所有子目录
        files #当前路径下所有非目录子文件
        """
        for file in files:
            for ext in ext_list:
                if file.endswith(ext):
                    if relative:
                        file_list.append(file)
                    else:
                        file_list.append(os.path.join(root, file))
    return file_list
