import os

from libs.lib_file_operate.file_coding import file_encoding


def remove_unprintable_chars(str_):
    """去除列表元素的\u200b等字符 https://blog.csdn.net/lly1122334/article/details/107615950 """
    if str_.isprintable():
        return str_
    else:
        new_path = ''.join(x for x in str_ if x.isprintable())
        return new_path


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