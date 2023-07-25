#!/usr/bin/env python
# encoding: utf-8

from libs.lib_file_operate.file_coding import file_encoding
from libs.lib_file_operate.file_read import remove_unprintable_chars
from libs.lib_file_operate.file_utils import file_is_empty
from libs.lib_file_operate.file_write import write_lines


def write_list_to_freq_file(file_path, path_list=None, encoding='utf-8', freq_symbol="<-->", anno_symbol="###"):
    # 先读取以前的命中文件文件内容
    freq_dict = read_file_to_freq_dict(file_path=file_path, encoding=encoding, freq_symbol=freq_symbol,
                                       anno_symbol=anno_symbol)
    # 遍历命中结果列表对结果列表进行添加
    freq_dict = {
        path: freq_dict[path] + 1 if path in freq_dict.keys() else 1 for path in path_list
    }
    # 根据字典的值进行排序
    sorted_dict = dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))
    # 将结果字典写入文件
    str_list = [f"{path}  {freq_symbol}{frequency}" for path, frequency in sorted_dict.items()]
    write_lines(file_path, str_list, encoding=encoding, new_line=True, mode="w+")
    return True


def read_file_to_freq_dict(file_path, encoding=None, freq_symbol='<-->', anno_symbol="###", default_freq=1):
    """
    读取一个文件内容并返回结果字典 {"路径”:频率} 文件的每一行格式类似 path freq_symbol 10
    freq_symbol 指定切割每一行的字符串 没有 frequency_symbol 的默认为1
    anno_symbol = "###" 如果启用注释, ###号后的字符都会进行删除
    """
    if file_is_empty(file_path):
        return {}

    # 自动获取文件编码
    if not encoding:
        encoding = file_encoding(file_path)

    freq_dict = {}
    with open(file_path, 'r', encoding=encoding) as f_obj:
        for line in f_obj.readlines():
            # 清理注释符号 ###
            if anno_symbol:
                line = line.rsplit(anno_symbol, 1)[0].strip()
            # 清理空字符串
            if not line.strip():
                continue
            # 去除不可见字符
            line = remove_unprintable_chars(line)
            # 如果规则存在频率选项 path [<-->10]
            split = [s.strip() for s in line.rsplit(freq_symbol, 1) if s.strip()]
            string = split[0]
            freq = int(split[1]) if len(split) > 1 and str(split[1]).isdigit() else default_freq
            # 如果字典已经存在就追加频率,否则直接赋值  # 判断字典是否包含键,可以使用in，__contains__()
            freq_dict[string] = freq_dict[string] + freq if string in freq_dict.keys() else freq
    return freq_dict


def read_files_to_freq_dict(file_list, encoding=None, frequency_symbol='<-->', annotation_symbol="###"):
    """
    读取文件列表内所有文件的内容并返回结果字典 {"路径”:频率}
    文件的每一行格式类似 path frequency_symbol 10
    frequency_symbol 指定切割每一行的字符串 没有 frequency_symbol 的默认为1
    annotation_symbol = "###" 如果启用注释,对###号开头的行,和频率字符串后面的###号都会进行删除
    """
    freq_dict = {}
    for file_path in file_list:
        raw_dict = read_file_to_freq_dict(file_path, encoding=encoding,
                                          freq_symbol=frequency_symbol,
                                          anno_symbol=annotation_symbol)

        # 合并到结果字典 # 使用 set(dict_a) | set(dict_b) 来获取 dict_a 和 dict_b 的所有键
        freq_dict.update({key: freq_dict.get(key, 0) + raw_dict.get(key, 0) for key in set(freq_dict) | set(raw_dict)})
    return freq_dict
