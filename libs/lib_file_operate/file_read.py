import os

from libs.lib_file_operate.file_coding import file_encoding


def remove_unprintable_chars(str_):
    """
    去除列表元素的\u200b等字符
    https://blog.csdn.net/lly1122334/article/details/107615950
    """
    if str_.isprintable():
        return str_
    else:
        new_path = ''.join(x for x in str_ if x.isprintable())
        return new_path


def read_file_to_list(file_path, encoding=None, de_strip=True, de_weight=False, de_unprintable=False):
    # 文本文件处理 读文件到列表
    result_list = []
    if os.path.exists(file_path):
        # 自动获取文件编码
        if not encoding:
            encoding = file_encoding(file_path)

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


def read_file_to_frequency_dict(file_path, encoding=None, frequency_symbol='<-->', annotation_symbol='#'):
    """
    读取一个文件内容并返回结果字典 {"路径”:频率}
    文件的每一行格式类似 path frequency_symbol 10
    frequency_symbol 指定切割每一行的字符串 没有 frequency_symbol 的默认为1
    annotation_symbol = '#' 如果启用注释,对#号开头的行,和频率字符串后面的#号都会进行删除
    """
    result_dict = {}
    if os.path.exists(file_path):
        # 自动获取文件编码
        if not encoding:
            encoding = file_encoding(file_path)

        with open(file_path, 'r', encoding=encoding) as f_obj:
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


def read_file_to_str(file_path, encoding=None, de_strip=False, de_unprintable=False):
    # 读取文件内容并返回字符串
    result_str = ""

    if os.path.exists(file_path):
        # 自动获取文件编码
        if not encoding:
            encoding = file_encoding(file_path)

        with open(file_path, 'r', encoding=encoding) as f_obj:
            result_str = f_obj.read()

            # 去除空字符结尾
            if de_strip:
                result_str = result_str.strip()

            # 去除不可见字符
            if de_unprintable:
                result_str = remove_unprintable_chars(result_str)

    return result_str


def read_file_to_dict(file_path, encoding=None, de_strip=True, de_unprintable=False, split_symbol=","):
    """
    简单读取文件到字典,以指定字符进行分隔
    :param file_path: 文件路径
    :param encoding: 文件编码
    :param de_strip: 去除两端空白字符
    :param de_unprintable: 去除不可见字符
    :param split_symbol: 键值对分割符号
    :return:
    """
    result_dict = {}
    if os.path.exists(file_path):
        # 自动获取文件编码
        if not encoding:
            encoding = file_encoding(file_path)
        with open(file_path, 'r', encoding=encoding) as f_obj:
            lines = f_obj.readlines()
            for line in lines:
                # 去除不可见字符
                if de_unprintable:
                    line = remove_unprintable_chars(line)

                # 分割csv
                key = line.split(split_symbol)[0]
                value = line.split(split_symbol)[-1]

                # strip空白字符
                if de_strip:
                    key = key.strip()
                    value = value.strip()

                result_dict[key] = value
    return result_dict


def read_files_to_list(file_list, encoding=None, de_strip=True, de_weight=False, de_unprintable=False):
    # 文本文件处理 读文件到列表
    result_list = []
    # 循环读取每个文件
    for file_path in file_list:
        file_content = read_file_to_list(file_path,
                                         encoding=encoding,
                                         de_strip=de_strip,
                                         de_weight=de_weight,
                                         de_unprintable=de_unprintable)
        result_list.extend(file_content)

    # 最终去重
    if result_list and de_weight:
        result_list = sorted(set(result_list), key=result_list.index)

    return result_list


def read_files_to_frequency_dict(file_list, encoding=None, frequency_symbol='<-->', annotation_symbol='#'):
    """
    读取文件列表内所有文件的内容并返回结果字典 {"路径”:频率}
    文件的每一行格式类似 path frequency_symbol 10
    frequency_symbol 指定切割每一行的字符串 没有 frequency_symbol 的默认为1
    annotation_symbol = '#' 如果启用注释,对#号开头的行,和频率字符串后面的#号都会进行删除
    """
    result_dict = {}
    for file_path in file_list:
        temp_dict = read_file_to_frequency_dict(file_path,
                                                encoding=encoding,
                                                frequency_symbol=frequency_symbol,
                                                annotation_symbol=annotation_symbol)

        # 合并到结果字典 # 使用 set(dict_a) | set(dict_b) 来获取 dict_a 和 dict_b 的所有键
        result_dict.update({key: result_dict.get(key, 0) + temp_dict.get(key, 0)
                            for key in set(result_dict) | set(temp_dict)})
    return result_dict
