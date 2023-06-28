#!/usr/bin/env python
# encoding: utf-8

import re

from libs.lib_dyna_rule.dyna_rule_tools import list_to_re_str
from libs.lib_url_analysis.url_parser import get_root_dir_url, get_url_ext


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
        url_path = url_str.split(get_root_dir_url(url_str), 1)[-1]  # /config.inc.php
        # 循环替换因变量值为%%键%%
        # ['%%DOMAIN%%': ['www', 'www.baidu.com', 'baidu', 'baidu_com', 'baidu.com', 'www_baidu_com'], '%%PATH%%': []}]
        # 需要排除其中的空列表
        for reverse_replace_dict in reverse_replace_dict_list:
            for key, value in reverse_replace_dict.items():
                if value:
                    # 处理[空格和/]字符
                    value = [ele for ele in value if str(ele).strip() and str(ele).strip() != "/"]
                if value:
                    url_path = re.sub(list_to_re_str(value), key, url_path, count=0)

        # 提取URL中的后缀
        url_ext = get_url_ext(url_str)
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

