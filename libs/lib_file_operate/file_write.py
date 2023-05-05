from libs.lib_file_operate.file_path import file_is_exist
from libs.lib_file_operate.file_read import read_file_to_frequency_dict


def write_title(file_path, title, encoding="utf-8", new_line=True, mode="a+"):
    # 文本文件写入表头,仅在文件不存在时,写入
    if not file_is_exist(file_path):
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


def write_path_list_to_frequency_file(file_path=None,
                                      path_list=None,
                                      encoding='utf-8',
                                      frequency_symbol="<-->",
                                      annotation_symbol="#",
                                      hit_over_write=True):
    # 写入列表到频率文件中
    if not hit_over_write:
        # 不需要频率计算,直接追加
        result_str_list = [f"{path} {frequency_symbol} 1" for path in path_list]
        write_lines(file_path, result_str_list, encoding=encoding, new_line=True, mode="a+")
    else:
        # 存储最终的频率字典
        frequency_dict = {}
        # 先读取以前的命中文件文件内容
        if file_is_exist(file_path):
            frequency_dict = read_file_to_frequency_dict(file_path=file_path,
                                                         encoding=encoding,
                                                         frequency_symbol=frequency_symbol,
                                                         annotation_symbol=annotation_symbol)

        # 遍历命中结果列表对结果列表进行添加
        for path in path_list:
            if path in frequency_dict.keys():
                frequency_dict[path] += 1
            else:
                frequency_dict[path] = 1

        # 根据字典的值进行排序
        sorted_dict = dict(sorted(frequency_dict.items(), key=lambda item: item[1], reverse=True))
        # 将结果字典写入文件
        result_str_list = [f"{path}  {frequency_symbol}{frequency}" for path, frequency in sorted_dict.items()]
        write_lines(file_path, result_str_list, encoding=encoding, new_line=True, mode="w+")
    return True
