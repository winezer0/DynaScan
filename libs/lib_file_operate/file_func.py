import binascii
import fnmatch
import os
import shutil


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