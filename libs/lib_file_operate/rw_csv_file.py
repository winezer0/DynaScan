#!/usr/bin/env python
# encoding: utf-8

import csv
from libs.lib_file_operate.file_utils import file_is_empty


def read_csv_to_dict(csv_file, mode="r", encoding="utf-8"):
    """
    读个CSV文件到字典格式(会自动拼接表头)
    :param csv_file:
    :param mode:
    :param encoding:
    :return:
    """
    if file_is_empty:
        return None
    with open(csv_file, mode=mode, encoding=encoding, newline='') as csvfile:
        # 自动分析分隔符
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
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
    if file_is_empty:
        return None
    with open(csv_file, mode=mode, encoding=encoding, newline='') as csvfile:
        # 自动分析分隔符
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect=dialect)
        row_list = [row for row in reader]
        return row_list


def write_dict_to_csv(csv_file, dict_data=[], mode="a+", encoding="utf-8"):
    """
    写入字典格式的数据到csv文件中
    :param csv_file:
    :param dict_data:
    :param mode:
    :param encoding:
    :return:
    """
    # 判断是否需要写入表头
    file_empty = file_is_empty(csv_file)

    # 在使用csv.writer()写入CSV文件时，通常建议将newline参数设置为''，以便按照系统的默认行为进行换行符的处理。
    with open(csv_file, mode=mode, encoding=encoding, newline='') as file_open:
        # DictWriter 直接写入字典格式的数据
        # fieldnames=data[0].keys() 将字典的键作为表头
        # quoting=csv.QUOTE_ALL  将每个元素都用双引号包裹
        csv_writer = csv.DictWriter(file_open, fieldnames=dict_data[0].keys(), quoting=csv.QUOTE_ALL)
        if file_empty:
            csv_writer.writeheader()
        csv_writer.writerows(dict_data)
