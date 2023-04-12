#!/usr/bin/env python
# encoding: utf-8
import re
from urllib.parse import quote


# 中文字符转ANY URL 如 gb2312、utf8
def chinese_char_to_encode(char_, coding="utf8", url_encode=True):
    """
    中文转任意编码  支持gb2312 utf8  unicode_escape  支持URL编码
    """
    # 进行编码
    char_ = char_.encode(coding)
    # 进行URL编码
    if url_encode:
        char_ = quote(char_)
    # 转为字符串
    char_ = str(char_).strip('b').replace('\'', '').replace('\\\\', '\\').replace('\\n', '')
    return char_


# 获取字符串中的中文
def extract_chinese_char(chinese_string):
    # 使用正则表达式匹配中文字符
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fa5]')
    chinese_char_list = chinese_char_pattern.findall(chinese_string)
    return chinese_char_list


# 生成 字符:编码结果 替换字典
def gen_chinese_replace_dict(char_list, coding="utf-8", url_encode=True):
    chinese_char_replace_dict = {}
    for chinese_char in char_list:
        replace_char = chinese_char_to_encode(chinese_char, coding=coding, url_encode=url_encode)
        chinese_char_replace_dict[chinese_char] = replace_char
    return chinese_char_replace_dict


# 替换列表中包含中文的字符串,返回一个字符串
def replace_string_by_replace_dict(old_string, replace_dict):
    for replace_key, replace_value in replace_dict.items():
        old_string = str(old_string).replace(replace_key, replace_value)
    return old_string


# 对字符串进行中文编码
def chinese_str_to_encode(string, coding, url_encode, de_strip, only_chinese=False):
    # 删除空白字符
    if de_strip:
        string = str(string).strip()
    # 检测是否存在中文字符
    char_list = extract_chinese_char(string)
    if char_list:
        # 生成替换字典
        chinese_char_replace_dict = gen_chinese_replace_dict(char_list=char_list, coding=coding, url_encode=url_encode)
        # 进行字符串替换
        string = replace_string_by_replace_dict(string, chinese_char_replace_dict)
    elif not only_chinese:
        # 对字符串进行URL编码
        string = chinese_char_to_encode(string, coding=coding, url_encode=url_encode)
    return string


# 对 字符串列表 进行中文编码和URL编码
def chinese_list_to_encode_by_char(string_list, 
coding_list=['utf-8'], 
url_encode=True, 
de_strip=True,
only_chinese=True):
    encode_str_list = []
    for string in string_list:
        for coding in coding_list:
            new_string = chinese_str_to_encode(string=string,
                                               coding=coding,
                                               url_encode=url_encode,
                                               de_strip=de_strip,
                                               only_chinese=only_chinese)
            # 不忽略没有编码的元组, 后面需要去重一次
            encode_str_list.append(new_string)
    return encode_str_list


# 对 元组列表 进行中文编码和URL编码
def chinese_encode_tuple_list_by_char(tuple_list, 
coding_list=["utf8"], 
url_encode=True, 
de_strip=True,
only_chinese=True):
    new_tuple_list = []
    for ele_1, ele_2 in tuple_list:
        for coding in coding_list:
            ele_1 = chinese_str_to_encode(string=ele_1,
                                          coding=coding,
                                          url_encode=url_encode,
                                          de_strip=de_strip,
                                          only_chinese=only_chinese)
            ele_2 = chinese_str_to_encode(string=ele_2,
                                          coding=coding,
                                          url_encode=url_encode,
                                          de_strip=de_strip,
                                          only_chinese=only_chinese)
            # 不忽略没有编码的元组, 后面需要去重一次
            new_tuple_list.append((ele_1, ele_2))
    return new_tuple_list


# 判断字符串是否包含中文
def has_chinese_char_by_re(text):
    pattern = re.compile('[\u4e00-\u9fa5]+')
    result = pattern.search(text)
    return result is not None


# 只适用于字符串中包含较少的中文字符的情况
def has_chinese_char_by_cycle(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False
