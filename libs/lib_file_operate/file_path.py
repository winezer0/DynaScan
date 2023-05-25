#!/usr/bin/env python
# encoding: utf-8

import os
from pathlib import Path


def file_is_empty(file_path):
    # 判断一个文件是否为空
    return not os.path.exists(file_path) or os.path.getsize(file_path) == 0


def auto_create_file(file_path):
    # 自动创建空文件
    if not os.path.exists(file_path):
        open(file_path, 'w').close()
        return True
    return False


def auto_make_dir(path):
    # 自动创建目录
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False


def file_is_exist(file_path):
    # 判断文件是否存在
    if file_path:
        path = Path(file_path)
        if path.is_file():
            return True
    return False


# 获取目录下的文件名信息, 返回 {文件名:文件绝对路径}
def get_dir_path_file_info_dict(dir_path, ext_list=['.txt']):
    """
    获取目录下的文件名信息, 返回 {文件名:文件绝对路径}
    存在问题,如果目录下存在同名文件|目录,会被覆盖.
    """
    if ext_list and isinstance(ext_list, str):
        ext_list = [ext_list]

    file_info_dict = {}
    for root, dirs, files in os.walk(dir_path):
        """
        root #当前目录路径
        dirs #当前路径下所有子目录
        files #当前路径下所有非目录子文件
        """
        for file in files:
            if not ext_list:
                file_info_dict[file] = os.path.join(root, file)
            else:
                for ext in ext_list:
                    if file.endswith(ext):
                        if file in file_info_dict.keys():
                            print(f"[!] Exists Same Name File [{file}], It Will Be Over Written !!!")
                        file_info_dict[file] = os.path.join(root, file)
                        break
    return file_info_dict


# 获取目录下的目录名信息, 返回 {目录名:目录名绝对路径}
def get_dir_path_dir_info_dict(dir_path):
    """
    获取目录下的目录名信息, 返回 {目录名:目录名绝对路径}
    存在问题,如果目录下存在同名文件|目录,会被覆盖.
    """
    dir_info_dict = {}
    for root, dirs, files in os.walk(dir_path):
        """
        root #当前目录路径
        dirs #当前路径下所有子目录
        files #当前路径下所有非目录子文件
        """
        for sub_dir in dirs:
            if sub_dir in dir_info_dict.keys():
                print(f"[!] Exists Same Name Dir [{sub_dir}], It Will Be Over Written !!!")
            dir_info_dict[sub_dir] = os.path.join(root, sub_dir)
    return dir_info_dict


# 获取目录下的目录名|文件名信息, 返回 {文件目录名绝对路径:文件目录名}
def get_dir_path_info_dict(dir_path, ext_list=['.txt']):
    """
    # 获取目录下的目录名|文件名信息, 返回 {文件目录名绝对路径:文件目录名}
    """
    info_dict = {}
    for root, dirs, files in os.walk(dir_path):
        """
        root #当前目录路径
        dirs #当前路径下所有子目录
        files #当前路径下所有非目录子文件
        """
        for sub_dir in dirs:
            if sub_dir in info_dict.keys():
                print(f"[!] Exists Same Name Dir [{sub_dir}], It Will Be Over Written !!!")
            info_dict[os.path.join(root, sub_dir)] = sub_dir

        for file in files:
            if not ext_list:
                info_dict[os.path.join(root, file)] = file
            else:
                for ext in ext_list:
                    if file.endswith(ext):
                        info_dict[os.path.join(root, file)] = file
                        break
    return info_dict


# 切割去除文件名的后缀,支持后缀列表
def file_name_remove_ext_list(file_name, ext_list):
    """
    切割去除文件名的后缀,支持后缀列表
    :param file_name: 文件名
    :param ext_list: 后缀名列表
    :return: 无后缀的文件名
    """
    # 去除文件名中的路径
    file_name = os.path.basename(file_name)
    # 去重并按长度排序后缀列表
    ext_list = sorted(list(set(ext_list)), key=len, reverse=True)
    for ext in ext_list:
        if ext in file_name:
            file_name = file_name.rsplit(ext, 1)[0]
            break
    return file_name


# 获取第一层子目录名称
def get_sub_dirs(directory):
    """
    获取第一层子目录名称
    """
    sub_dirs = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            sub_dirs.append(item)
    return sub_dirs
