#!/usr/bin/env python
# encoding: utf-8

import re

from libs.lib_url_analysis.url_tools import get_base_url, get_url_ext_urlsplit


# URL转原始规则（做反向变量替换）
def url_to_raw_rule_classify(hit_url_list,
                             reverse_replace_dict_list,
                             hit_ext_file,
                             hit_direct_file,
                             hit_folder_file,
                             hit_files_file
                             ):
    hit_classify = {hit_ext_file: [],
                    hit_direct_file: [],
                    hit_folder_file: [],
                    hit_files_file: []}

    for url_str in hit_url_list:
        # 提取路径
        url_path = url_str.split(get_base_url(url_str), 1)[-1]  # /config.inc.php
        # 循环替换因变量值为%%键%%
        # ['%%DOMAIN%%': ['www', 'www.baidu.com', 'baidu', 'baidu_com', 'baidu.com', 'www_baidu_com'],
        # '%%PATH%%': []}]  # 需要排除其中的空列表
        for reverse_replace_dict in reverse_replace_dict_list:
            for key, value in reverse_replace_dict.items():
                value = [ele for ele in value if str(ele).strip() and str(ele).strip() != "/"]  # 处理[ /]字符
                if value:
                    url_path = re.sub(list_to_re_str(value), key, url_path, count=0)

        # 提取URL中的后缀
        url_ext = get_url_ext_urlsplit(url_str)
        # 如果URL中确实存在后缀
        if url_ext and url_ext.strip():
            hit_classify[hit_ext_file].append(url_ext)

        if url_path.strip('/'):
            hit_classify[hit_direct_file].append(url_path)

        folders_path = '/' + url_path.rsplit("/", 1)[0].rsplit("/", 1)[-1]
        if folders_path.strip('/'):
            hit_classify[hit_folder_file].append(folders_path)

        file_path = '/' + url_path.rsplit("/", 1)[-1]
        if file_path.strip('/'):
            hit_classify[hit_files_file].append(file_path)

    return hit_classify


# 将URL转换为原始规则
def list_to_re_str(replace_list, bracket=True):
    """
    将后缀字典列表转为一个正则替换规则字符串
    replace_list: 列表，如 ['.ccc', '.bbb']
    bracket: 是否给正则结果添加括号
    返回值: 一个正则表达式模式字符串，如 '(\\.ccc|\\.bbb)'
    """
    if replace_list:
        # 使用列表推导式和re.escape()自动转义为正则表达式中的文字字符
        regexp = '|'.join(re.escape(item) for item in replace_list)
    else:
        regexp = ""

    if bracket:
        replace_str = f'({regexp})'
    else:
        replace_str = f'{regexp}'

    return replace_str
