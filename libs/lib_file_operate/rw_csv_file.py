#!/usr/bin/env python
# encoding: utf-8

import csv
from libs.lib_file_operate.file_utils import file_is_empty, auto_make_dir
from libs.lib_file_operate.file_write import write_title, write_line


def escape_quotes(data):
    return data.replace("\"", "'") if isinstance(data, str) else data


def read_csv_to_dict(csv_file, mode="r", encoding="utf-8"):
    """
    读个CSV文件到字典格式(会自动拼接表头)
    :param csv_file:
    :param mode:
    :param encoding:
    :return:
    """
    if file_is_empty(csv_file):
        return None
    with open(csv_file, mode=mode, encoding=encoding, newline='') as csvfile:
        # 方案1、使用 reader
        # reader = csv.reader(csvfile)
        # title = next(reader)  # 读取第一行
        # row_list = [dict(zip(title, row)) for row in reader]

        # 自动分析分隔符
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)

        # 方案2、使用 DictReader
        reader = csv.DictReader(csvfile, dialect=dialect)
        row_list = [row for row in reader]
        return row_list


def read_csv_to_simple_list(csv_file, mode="r", encoding="utf-8"):
    """
    读个CSV文件到列表格式(基本不做操作)
    :param csv_file:
    :param mode:
    :param encoding:
    :return:
    """
    if file_is_empty(csv_file):
        return None
    with open(csv_file, mode=mode, encoding=encoding, newline='') as csvfile:
        # 自动分析分隔符
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect=dialect)
        row_list = [row for row in reader]
        return row_list


def write_dict_to_csv(csv_file, dict_data=[], mode="a+", encoding="utf-8", title_keys=None):
    """
    写入字典格式的数据到csv文件中
    :param csv_file: 文件路径
    :param dict_data: 字典数据
    :param mode:  文件写入模式
    :param encoding: 文件写入编码
    :param title_keys: 自定义需要的表头
    :return:
    """
    auto_make_dir(csv_file, is_file=True)
    # 判断输入的是字典列表,还是单个字典
    dict_data = [dict_data] if isinstance(dict_data, dict) else dict_data
    # 判断是否需要写入表头
    file_empty = file_is_empty(csv_file)
    # 获取表头格式
    title_keys = title_keys or dict_data[0].keys()
    # 在使用csv.writer()写入CSV文件时，通常建议将newline参数设置为''，以便按照系统的默认行为进行换行符的处理。
    with open(csv_file, mode=mode, encoding=encoding, newline='') as file_open:
        # DictWriter 直接写入字典格式的数据
        # fieldnames=data[0].keys() 将字典的键作为表头
        # quoting=csv.QUOTE_ALL  将每个元素都用双引号包裹
        csv_writer = csv.DictWriter(file_open, fieldnames=title_keys, quoting=csv.QUOTE_ALL)
        if file_empty:
            csv_writer.writeheader()
        csv_writer.writerows(dict_data)
        file_open.close()


def write_dict_to_csv_s(csv_path, dict_list, mode="a+", encoding="utf-8", title_keys=None):
    # 判断输入的是字典列表,还是单个字典
    dict_list = [dict_list] if isinstance(dict_list, dict) else dict_list
    # 设计CSV表头格式
    columns = title_keys or list(dict_list[0].keys())
    # 根据表头个书生成format格式文件
    row_format = ('"{}",' * len(columns)).strip(",")
    try:
        # 写入标题
        title = row_format.format(*tuple(columns))
        write_title(csv_path, title, encoding=encoding, new_line=True, mode="w+")

        # 按 title 列表顺序格式化 dict
        data_lists = [[escape_quotes(a_dict[key]) for key in columns] for a_dict in dict_list]
        dict_list = [row_format.format(*tuple(data_list)) for data_list in data_lists]
        write_line(csv_path, dict_list, encoding=encoding, new_line=True, mode=mode)

        return csv_path
    except Exception as error:
        raise f"[-] An Error Occurred Writing:{error}"


def write_list_to_csv_s(csv_path, data_lists, encoding="utf-8", title_keys=None, mode="w+"):
    # 判断是二维列表还是一维列表
    data_lists = [data_lists] if isinstance(data_lists[0], str) else data_lists
    # 设计CSV表头格式
    columns = title_keys or list(data_lists[0].keys())
    # 根据表头个书生成format格式文件
    row_format = ('"{}",' * len(columns)).strip(",")
    try:
        # 文本文件写入标题
        title = row_format.format(*tuple(title_keys))
        write_title(csv_path, title, encoding=encoding, new_line=True, mode="w+")

        # 转义双引号数据 并 格式化
        data_lists = [row_format.format(*tuple([escape_quotes(ele) for ele in a_list])) for a_list in data_lists]
        write_line(csv_path, data_lists, encoding="utf-8", new_line=True, mode=mode)
        return csv_path
    except Exception as error:
        raise f"[-] An Error Occurred Writing:{error}"


def write_list_to_csv(csv_path, data_lists, encoding="utf-8", title_keys=None, mode="w+"):
    auto_make_dir(csv_path, is_file=True)
    with open(csv_path, mode=mode, newline='', encoding=encoding) as file:
        writer = csv.writer(file)
        # 检查是否已经写入标题行
        if file.tell() == 0 and title_keys:
            writer.writerow(title_keys)
        # 循环写入数据行
        writer.writerows(data_lists)
