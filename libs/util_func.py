#!/usr/bin/env python
# encoding: utf-8

import re
from urllib.parse import unquote
from libs.lib_dyna_rule.dyna_rule_tools import list_to_re_str
from libs.lib_collect_opera.collect_operation import cartesian_product_merging, frozen_tuple_list
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_ERROR
from libs.lib_url_analysis.url_parser import get_root_dir_url, get_url_ext


# 进行URL检查
def analysis_ends_url(current_url_list):
    for url in current_url_list:
        if "%%" in url or "%25%25" in unquote(url):
            output(f"[!] URL [{url}] 中存在 [%%] 可能是错误情景", level=LOG_ERROR)
    else:
        output(f"[*] 最终生成的URL检查通过", level=LOG_INFO)


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


# 合并folders目录字典列表和files目录字典列表
def product_folders_and_files(folder_list, files_list):
    # 合并folders目录字典列表和files目录字典列表
    def format_paths(path_list):
        """
        格式化目录和文件的路径，使其符合要求
        """
        formatted_paths = []
        for path in path_list:
            path = path.strip("/")
            if not path.startswith('/'):
                path = '/' + path
            if path.endswith('/'):
                path = path.rstrip('/')
            formatted_paths.append(path)
        formatted_paths = list(set(formatted_paths))
        return formatted_paths

    # 格式化目录
    folder_list = format_paths(folder_list)
    # 格式化file
    files_list = format_paths(files_list)

    group_folder_files_list = cartesian_product_merging(folder_list, files_list)
    group_folder_files_list = frozen_tuple_list(group_folder_files_list, link_symbol="")
    return group_folder_files_list


