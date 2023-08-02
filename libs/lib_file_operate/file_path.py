#!/usr/bin/env python
# encoding: utf-8
import os


def get_dirs_file_info_dict(dir_path, ext_list=['.txt']):
    """
    获取目录下的（指定后缀的）文件名信息, 返回 {文件绝对路径:文件名}
    :param dir_path:
    :param ext_list:
    :return:
    """
    if ext_list and isinstance(ext_list, str):
        ext_list = [ext_list]

    info_dict = {}
    # root #当前目录路径
    # dirs #当前路径下所有子目录
    # files #当前路径下所有非目录子文件
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if ext_list:
                for ext in ext_list:
                    if file.endswith(ext):
                        info_dict[os.path.join(root, file)] = file
                        break
            else:
                info_dict[os.path.join(root, file)] = file
    return info_dict


def get_dirs_dir_info_dict(dir_path):
    """
    获取目录下的目录名信息, 返回 {目录名绝对路径:目录名}
    :param dir_path:
    :return:
    """
    info_dict = {}
    for root, dirs, files in os.walk(dir_path):
        for sub_dir in dirs:
            info_dict[os.path.join(root, sub_dir)] = sub_dir
    return info_dict


def get_dirs_path_info_dict(dir_path, ext_list=['.txt']):
    """
    获取目录下的文件名|目录名信息, 返回 {文件名|目录名绝对路径: 文件名|目录名}
    :param dir_path:
    :param ext_list:
    :return:
    """
    info_dict = {}
    info_dict.update(get_dirs_file_info_dict(dir_path, ext_list=ext_list))
    info_dict.update(get_dirs_dir_info_dict(dir_path))
    return info_dict


def get_sub_dirs(dir_path):
    """
    获取第一层目录下的目录名信息, 返回 {目录名绝对路径: 目录名}
    :param dir_path:
    :return:
    """
    info_dict = {}
    for item in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, item)):
            info_dict[os.path.join(dir_path, item)] = item
    return info_dict


def get_dirs_all_info_dict(dir_path):
    """
    获取目录下的目录名|文件名信息, 返回 {'dir': {path : name}, 'file':{path : name}}
    :param dir_path:
    :return:
    """
    info_dict = {"dir": {}, "file": {}}
    for root, dirs, files in os.walk(dir_path):
        for sub_dir in dirs:
            info_dict["dir"][os.path.join(root, sub_dir)] = sub_dir
        for sub_file in files:
            info_dict["file"][os.path.join(root, sub_file)] = sub_file
    return info_dict


def get_dirs_sub_info_dict(dir_path):
    """
    获取第一层目录下的目录名|文件名信息, 返回 file_info_dict
    {'dir': {path : name}, 'file':{path : name}}
    :param dir_path:
    :return:
    """
    info_dict = {"dir": {}, "file": {}}
    for item in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, item)):
            info_dict["dir"][os.path.join(dir_path, item)] = item
        else:
            info_dict["file"][os.path.join(dir_path, item)] = item
    return info_dict
