#!/usr/bin/env python
# encoding: utf-8

import os
from pathlib import Path


# 自动创建目录
def auto_make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 判断文件是否存在
def file_is_exist(filepath):
    """判断文件是否存在"""
    if filepath:
        path = Path(filepath)
        if path.is_file():
            return True
        else:
            return False


# 去除不可见字符
def remove_unprintable_chars(str_):
    """去除列表元素的\u200b等字符 https://blog.csdn.net/lly1122334/article/details/107615950 """
    if str_.isprintable():
        return str_
    else:
        new_path = ''.join(x for x in str_ if x.isprintable())
        return new_path


# 文本编码处理 判断文件类型gbk、utf-8
def file_type(file_path):
    """判断文件类型gbk、utf-8"""
    file_type = "gbk"
    try:
        data = open(file_path, 'r', encoding=file_type)
        data.read()
    except UnicodeDecodeError:
        file_type = "utf-8"
    else:
        data.close()
    return file_type


# 文本编码处理 判断文件类型gbk、utf-8
def file_encoding(file_path: str):
    """
    获取文件编码类型

    :param file_path: 文件路径
    :return:
    """
    if file_is_exist(file_path):
        with open(file_path, 'rb') as f:
            return string_encoding(f.read())
    else:
        return "utf-8"


# 文本编码处理 判断字符串编码类型gbk、utf-8
def string_encoding(data: bytes):
    # 简单的判断文件编码类型
    # 说明：UTF兼容ISO8859-1和ASCII，GB18030兼容GBK，GBK兼容GB2312，GB2312兼容ASCII
    CODES = ['UTF-8', 'GB18030', 'BIG5']
    # UTF-8 BOM前缀字节
    UTF_8_BOM = b'\xef\xbb\xbf'

    """
    获取字符编码类型

    :param data: 字节数据
    :return:
    """
    # 遍历编码类型
    for code in CODES:
        try:
            data.decode(encoding=code)
            if 'UTF-8' == code and data.startswith(UTF_8_BOM):
                return 'UTF-8-SIG'
            return code
        except UnicodeDecodeError:
            continue
    return 'unknown'


# 读文件到列表 # 去除不可见字符
def read_file_to_list(file_path, encoding='utf-8', de_strip=True, de_weight=False, de_unprintable=False):
    """文本文件处理 读文件到列表"""
    result_list = []
    if os.path.exists(file_path):
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


# 得到{"路径”:频率}字典中频率大于指定值的列表
def get_key_list_with_frequency(frequency_dict, frequency_min):
    if frequency_dict is None:
        frequency_dict = {}
    frequency_list = []
    for key, value in frequency_dict.items():
        if frequency_min <= value:
            frequency_list.append(key)
    return frequency_list


# 读取一个文件内容并返回结果字典 {"路径”:频率}
def read_file_to_frequency_dict(file_name,
                                encoding='utf-8',
                                frequency_symbol='<-->',
                                annotation_symbol='#'):
    """
    读取文件内容并返回结果字典
    文件的每一行格式类似 path frequency_symbol 10
    frequency_symbol 指定切割每一行的字符串 没有 frequency_symbol 的默认为1
    annotation_symbol = '#' 如果启用注释,对#号开头的行,和频率字符串后面的#号都会进行删除
    """
    if not encoding:
        encoding = file_encoding(file_name)

    with open(file_name, 'r', encoding=encoding) as f_obj:
        result_dict = {}
        for line in f_obj.readlines():
            # 忽略 #号开头的行
            if annotation_symbol and line.strip().startswith(annotation_symbol):
                line = ''
            if line.strip() != "":
                # 去除不可见字符
                line = remove_unprintable_chars(line)
                # 如果规则存在频率选项 path [<-->10]
                if frequency_symbol in line.strip():
                    line_string = line.rsplit(frequency_symbol, 1)[0].strip()
                    # 忽略frequency字符串后 #号开头的内容
                    line_frequency = line.rsplit(frequency_symbol, 1)[-1].split(annotation_symbol, 1)[0].strip()
                    line_frequency = int(line_frequency)
                    # output(line_string,line_frequency)
                else:
                    line_string = line.strip()
                    line_frequency = 1
                # 如果字典已经存在就追加频率,否则直接赋值
                # 判断字典是否包含键,可以使用in，__contains__()
                if line_string in result_dict.keys():
                    line_frequency += result_dict[line_string]
                    result_dict[line_string] = line_frequency
                else:
                    result_dict[line_string] = line_frequency
        return result_dict


# 读取文件内容并返回字符串 # 去除不可见字符
def read_file_to_str(file_name, encoding='utf-8', de_strip=False, de_unprintable=False):
    """
    读取文件内容并返回字符串
    """
    result_str = ""
    with open(file_name, 'r', encoding=encoding) as f_obj:
        result_str = f_obj.read()

        # 去除空字符结尾
        if de_strip:
            result_str = result_str.strip()

        # 去除不可见字符
        if de_unprintable:
            result_str = remove_unprintable_chars(result_str)

    return result_str


# 获取目录下的文件列表,返回目录下的文件名列表【相对路径】
def get_dir_path_file_name(file_dir, ext_list=['.txt'], relative=True):
    """ 获取目录下的文件列表,返回目录下的文件名列表"""
    # 处理 输入的扩展后缀, 预期是一个后缀列表
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


# 文本文件写入数据 默认追加
def write_line(file_path, data, encoding="utf-8", new_line=True, mode="a+"):
    with open(file_path, mode=mode, encoding=encoding) as f_open:
        if new_line:  # 换行输出
            data = f"{data}\n"
        f_open.write(data)
        f_open.close()


# 文本文件写入数据 默认追加
def write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="a+"):
    with open(file_path, mode=mode, encoding=encoding) as f_open:
        if new_line:  # 换行输出
            data_list = [f"{data}\n" for data in data_list]
        f_open.writelines(data_list)
        f_open.close()


# 写入频率字典到文件中
def write_hit_result_to_frequency_file(file_name=None,
                                       path_list=None,
                                       encoding='utf-8',
                                       frequency_symbol="<-->",
                                       annotation_symbol="#",
                                       hit_over_write=True):
    if not hit_over_write:
        # 不需要频率计算,直接追加
        result_str_list = [f"{path} {frequency_symbol} 1" for path in path_list]
        write_lines(file_name, result_str_list, encoding=encoding, new_line=True, mode="a+")
    else:
        # 存储最终的频率字典
        frequency_dict = {}
        # 先读取以前的命中文件文件内容
        if file_is_exist(file_name):
            frequency_dict = read_file_to_frequency_dict(file_name=file_name,
                                                         encoding=encoding,
                                                         frequency_symbol=frequency_symbol,
                                                         annotation_symbol=annotation_symbol)

        # 遍历命中结果列表对结果列表进行添加
        for path in path_list:
            print(path)
            if path in frequency_dict.keys():
                frequency_dict[path] += 1
            else:
                frequency_dict[path] = 1

        # 根据字典的值进行排序
        sorted_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True))
        # 将结果字典写入文件
        result_str_list = [f"{path}  {frequency_symbol}{frequency}" for path, frequency in sorted_dict.items()]
        write_lines(file_name, result_str_list, encoding=encoding, new_line=True, mode="w+")
    return True
