#!/usr/bin/env python
# encoding: utf-8

import binascii
import fnmatch
import os
import shutil

from libs.lib_file_operate.file_read import read_file_to_list


def file_is_exist(file_path):
    # 判断文件是否存在
    return os.path.exists(file_path)


def file_is_empty(file_path):
    # 判断一个文件是否为空
    return not os.path.exists(file_path) or not os.path.getsize(file_path)


def auto_create_file(file_path):
    # 自动创建空文件
    if not os.path.exists(file_path):
        open(file_path, 'w').close()
        return True
    return False


def auto_make_dir(path, is_file=False):
    # 自动创建目录  如果输入的是文件路径,就创建上一级目录
    directory = os.path.dirname(os.path.abspath(path)) if is_file else path
    # print(f"auto_make_dir:{directory}")
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False


def copy_file(src, dst):
    try:
        # 创建目标路径中的目录（如果不存在）
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
        return True
    except FileNotFoundError:
        print("源文件不存在")
        return False
    except IsADirectoryError:
        print("目标路径是目录")
        return False


def calc_file_crc32(file_path):
    """
    计算文件的CRC32值
    :param file_path:
    :return:
    """
    if os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as file:
                crc = 0
                for chunk in iter(lambda: file.read(4096), b''):
                    crc = binascii.crc32(chunk, crc)
            return crc & 0xFFFFFFFF
        except IOError:
            print("无法打开文件")
    return None


def compare_files(file1, file2):
    """
    判断两个文件是否内容相同，通过CRC32值比较
    :param file1:
    :param file2:
    :return:
    """
    crc1 = calc_file_crc32(file1)
    crc2 = calc_file_crc32(file2)

    if crc1 is not None and crc2 is not None:
        if crc1 == crc2:
            return True
        else:
            return False
    else:
        return False


def auto_copy_file(src_path, dest_path):
    if src_path and dest_path:
        if not compare_files(src_path, dest_path):
            auto_make_dir(dest_path, is_file=True)
            copy_file(src_path, dest_path)


def get_home_path(filename=None):
    """
    获取当前用户目录 或 基于当前用户目录的文件
    :param filename: 基于当前用户目录拼接的文件名
    :return: 返回当前目录
    """
    # 获取当前用户的目录
    user_dir = os.path.expanduser("~")
    if filename:
        if isinstance(filename, tuple):
            return os.path.join(user_dir, *filename)
        else:
            return os.path.join(user_dir, filename)
    else:
        return user_dir


def file_name_remove_ext(file_name, ext_list):
    """
    切割去除文件名的后缀,支持后缀列表
    :param file_name: 文件名
    :param ext_list: 后缀名列表
    :return: 无后缀的文件名
    """
    # 去除文件名中的路径
    file_name = os.path.basename(file_name)
    # 去重并按长度排序后缀列表
    ext_list = [ext_list] if isinstance(ext_list, str) else sorted(list(set(ext_list)), key=len, reverse=True)
    # 使用列表推导式简化代码 next 函数在找到第一个满足条件的元素后，会立即停止并返回该元素，
    file_name = next((file_name.rsplit(ext, 1)[0] for ext in ext_list if ext in file_name), file_name)
    return file_name


def file_name_add_new_ext(file_name, new_ext):
    # 基于当前文件名去除后缀添加新的文件名
    # 使用os.path模块来简化文件名和扩展名的处理
    file_name_base, file_ext = os.path.splitext(file_name)
    return f"{file_name_base}.{new_ext}"


def find_file_by_name(directory, binary_name, absolute=False):
    """
    使用文件名从指定目录获取文件的路径
    :param directory: 程序所在目录
    :param binary_name: 二进制文件名称
    :param absolute: 是否返回绝对路径
    :return: 程序所在路径
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if fnmatch.fnmatchcase(file, binary_name):
                relative_path = os.path.join(root, file)
                absolute_path = os.path.abspath(relative_path)
                return absolute_path if absolute else relative_path
    return None  # 如果没有找到文件，则返回 None


def exclude_history_files(str_list, exclude_files):
    # 排除文件里包含的记录
    if isinstance(exclude_files, str):
        exclude_files = [exclude_files]

    exclude_list = []
    for file_path in exclude_files:
        if file_is_exist(file_path):
            temp_list = read_file_to_list(file_path, de_strip=True, de_weight=True, de_unprintable=False)
            exclude_list.extend(temp_list)

    if exclude_list and str_list:
        str_list = list(set(str_list) - set(exclude_list))
    return str_list
