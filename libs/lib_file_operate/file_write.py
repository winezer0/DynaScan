from libs.lib_file_operate.file_utils import file_is_empty


def write_title(file_path, title, encoding="utf-8", new_line=True, mode="a+"):
    # 文本文件写入表头,仅在文件不存在时,写入
    if file_is_empty(file_path):
        with open(file_path, mode=mode, encoding=encoding) as f_open:
            if new_line:  # 换行输出
                title = f"{title.strip()}\n"
            f_open.write(title)
            f_open.close()


def write_line(file_path, data, encoding="utf-8", new_line=True, mode="a+"):
    # 文本文件写入数据 默认追加
    with open(file_path, mode=mode, encoding=encoding) as f_open:
        if new_line:  # 换行输出
            data = f"{data.strip()}\n"
        f_open.write(data)
        f_open.close()


def write_lines(file_path, data_list, encoding="utf-8", new_line=True, mode="w+"):
    # 文本文件写入数据 默认追加
    with open(file_path, mode=mode, encoding=encoding) as f_open:
        if new_line:  # 换行输出
            data_list = [f"{data}\n" for data in data_list]
        f_open.writelines(data_list)
        f_open.close()


