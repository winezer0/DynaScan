#!/usr/bin/env python
# encoding: utf-8

from libs.lib_file_operate.file_utils import file_is_empty, auto_make_dir


def write_title(file_path, title, encoding="utf-8", new_line=True, mode="a+"):
    auto_make_dir(file_path, is_file=True)
    # 文本文件写入表头,仅在文件不存在时,写入
    if file_is_empty(file_path):
        with open(file_path, mode=mode, encoding=encoding) as f_open:
            title = f"{title.strip()}\n" if new_line else title
            f_open.write(title)
            f_open.close()


def write_line(file_path, data_list, encoding="utf-8", new_line=True, mode="w+"):
    auto_make_dir(file_path, is_file=True)
    # 判断输入的是字符串还是列表
    data_list = [data_list] if isinstance(data_list, str) else data_list
    # 文本文件写入数据 默认追加
    with open(file_path, mode=mode, encoding=encoding) as f_open:
        data_list = [f"{data.strip()}\n" for data in data_list] if new_line else data_list
        f_open.writelines(data_list)
        f_open.close()



