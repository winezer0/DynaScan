#!/usr/bin/env python
# encoding: utf-8

from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str
from libs.lib_dyna_rule.base_rule_parser import base_rule_render_list
from libs.lib_dyna_rule.dyna_rule_tools import cartesian_product_merging, frozen_tuple_list, \
    get_key_list_with_frequency
from libs.lib_dyna_rule.set_basic_var import set_base_var_dict_frequency
from libs.lib_file_operate.file_path import file_is_exist, get_dir_path_file_info_dict, get_sub_dirs
from libs.lib_file_operate.file_read import read_file_to_list, read_files_to_frequency_dict
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_ERROR, LOG_DEBUG
from libs.lib_url_analysis.url_handle import specify_ext_store, specify_ext_delete, replace_multi_slashes, \
    remove_url_end_symbol, url_path_lowercase, url_path_chinese_encode, url_path_url_encode
from libs.lib_url_analysis.url_tools import get_segment_urls_urlsplit
from setting_total import *


# 合并folders目录字典列表和files目录字典列表
def product_folders_and_files(folder_list, files_list):
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

    # 记录开始替换的时间
    start_time = time.time()

    # 格式化目录
    folder_list = format_paths(folder_list)
    # 格式化file
    files_list = format_paths(files_list)

    group_folder_files_list = cartesian_product_merging(folder_list, files_list)
    group_folder_files_list = frozen_tuple_list(group_folder_files_list, link_symbol="")
    end_time = time.time()
    run_time = end_time - start_time
    return group_folder_files_list, run_time


# 合并urls列表和paths列表
def product_urls_and_paths(urls, paths):
    def format_urls(url_list):
        """
        格式化目录和文件的路径，使其符合要求
        """
        formatted_paths = []
        for url in url_list:
            if url.endswith('/'):
                url = url.rstrip('/')
            formatted_paths.append(url)
        formatted_paths = list(set(formatted_paths))
        return formatted_paths

    # 格式化目录
    urls = format_urls(urls)
    paths = format_urls(paths)

    url_add_path_list = cartesian_product_merging(urls, paths)
    url_add_path_list = frozen_tuple_list(url_add_path_list, link_symbol="")
    return url_add_path_list


# 对输入的目标URL进行扩展
def target_url_handle(url):
    url_list = []
    # 根据URL层级拆分为多个目标
    if GB_SPLIT_TARGET_PATH:
        url_list = get_segment_urls_urlsplit(url)
        output(f"[*] 扩展目标URL 当前元素 {len(url_list)}个", level=LOG_INFO)
    else:
        url_list.append(url)
    return url_list


# 拼接URL前的PATH过滤和格式化
def path_list_handle(path_list):
    # 对列表中的所有PATH添加指定前缀
    if GB_ADD_CUSTOM_PREFIX:
        path_list = product_urls_and_paths(GB_ADD_CUSTOM_PREFIX, path_list)
        output(f"[*] 自定义前缀 剩余元素 {len(path_list)}个", level=LOG_INFO)

    # 保留指定后缀的URL目标
    if GB_ONLY_SCAN_SPECIFY_EXT:
        path_list = specify_ext_store(path_list, GB_ONLY_SCAN_SPECIFY_EXT)
        output(f"[*] 保留指定后缀  剩余元素 {len(path_list)}个", level=LOG_ERROR)

    # 移除指定后缀列表的内容
    if GB_NO_SCAN_SPECIFY_EXT:
        path_list = specify_ext_delete(path_list, GB_NO_SCAN_SPECIFY_EXT)
        output(f"[*] 移除指定后缀 剩余元素 {len(path_list)}个", level=LOG_ERROR)

    # 是否开启结尾字符列表去除
    if GB_REMOVE_SOME_SYMBOL:
        path_list = remove_url_end_symbol(path_list, remove_symbol_list=GB_REMOVE_SOME_SYMBOL)
        output(f"[*] 删除结尾字符 剩余元素 {len(path_list)}个", level=LOG_INFO)

    # 是否开启REMOVE_MULTI_SLASHES,将多个////转换为一个/
    if GB_REMOVE_MULTI_SLASHES:
        path_list = replace_multi_slashes(path_list)
        output(f"[*] 转换多个[/]为单[/] 剩余URL:{len(path_list)}个", level=LOG_INFO)

    # 全部路径小写
    if GB_URL_PATH_LOWERCASE:
        path_list = url_path_lowercase(path_list)
        output(f"[*] 全部路径小写 剩余元素 {len(path_list)}个", level=LOG_INFO)

    # 批量解决字典中文乱码问题
    if GB_CHINESE_ENCODE:
        if GB_ONLY_ENCODE_CHINESE:
            # 将URL字典中的中文路径进行多种编码的URL编码
            path_list = url_path_chinese_encode(path_list, GB_CHINESE_ENCODE)
            output(f"[+] 中文编码完毕 剩余元素 {len(path_list)}个", level=LOG_INFO)
        else:
            # 将URL字典的所有元素都进行多种编码的URL编码
            path_list = url_path_url_encode(path_list, GB_CHINESE_ENCODE)
            output(f"[+] URL编码完毕 剩余元素 {len(path_list)}个", level=LOG_INFO)

    return path_list


# 扫描前的URL过滤和格式化
def url_list_handle(url_list, url_history_file):
    # URL列表限额
    if GB_MAX_URL_NUM and isinstance(GB_MAX_URL_NUM, int):
        url_list = url_list[:GB_MAX_URL_NUM]

    # 排除历史扫描记录
    if GB_EXCLUDE_HOST_HISTORY:
        if file_is_exist(url_history_file):
            accessed_url_list = read_file_to_list(file_path=url_history_file, de_strip=True, de_weight=True,
                                                  de_unprintable=False)
            url_list = list(set(url_list) - set(accessed_url_list))
            output(f"[*] 历史访问URL {len(accessed_url_list)}个", level=LOG_INFO)
        output(f"[*] 剔除历史URL 剩余URL:{len(url_list)}个", level=LOG_INFO)
    return url_list


# 按频率读取目录下的所有字典文件,并进行动态解析
def read_path_files_and_rule_parse_frequency(dir_path,
                                             ext_list,
                                             frequency_symbol,
                                             annotation_symbol,
                                             frequency_min,
                                             replace_dict):
    # 获取目录下所有文件名
    path_files = get_dir_path_file_info_dict(dir_path=dir_path, ext_list=ext_list)

    # 读取目录下所有文件内容到频率字典
    path_frequency_dict = read_files_to_frequency_dict(list(path_files.values()),
                                                       frequency_symbol=frequency_symbol,
                                                       annotation_symbol=annotation_symbol)
    # 筛选频率字典
    path_frequency_list = get_key_list_with_frequency(path_frequency_dict, frequency_min)

    # 对 列表 中的规则进行 进行 动态解析
    path_frequency_list, _, _ = base_rule_render_list(path_frequency_list)

    # 对每个元素进行规则替换
    path_frequency_list, _, _ = replace_list_has_key_str(path_frequency_list, replace_dict)

    return path_frequency_list


# 生成基本扫描字典
def gen_base_scan_path_list(cur_rule_dir_list=None):
    # 0、在不指定扫描目录的情况下,默认扫描所有文件
    all_rule_dir_list = get_sub_dirs(GB_DICT_RULE_PATH)
    if cur_rule_dir_list:
        unexpected_dirs = [element for element in cur_rule_dir_list if element not in all_rule_dir_list]
        if len(unexpected_dirs) > 0:
            output(f"[!] 输入非预期目录:{unexpected_dirs}, 当前可选目录: {all_rule_dir_list}", level=LOG_ERROR)
            exit()
    else:
        cur_rule_dir_list = all_rule_dir_list
    output(f"[*] 当前指定加载目录:{cur_rule_dir_list}", level=LOG_DEBUG)

    # 1、获取基本变量替换字典
    base_var_replace_dict = set_base_var_dict_frequency(base_var_dir=GB_BASE_VAR_DIR,
                                                        ext_list=GB_DICT_SUFFIX,
                                                        base_replace_dict=GB_BASE_VAR_REPLACE_DICT,
                                                        frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                        annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                        frequency_min=GB_FREQUENCY_MIN
                                                        )
    output(f"[*] 获取基本变量完成:{base_var_replace_dict.keys()}", level=LOG_DEBUG)

    base_path_list = []
    for rule_dir in cur_rule_dir_list:
        direct_path = GB_DIRECT_PATH_STR.format(RULE_DIR=rule_dir)
        group_dirs = GB_GROUP_DIRS_STR.format(RULE_DIR=rule_dir)
        group_file = GB_GROUP_FILE_STR.format(RULE_DIR=rule_dir)
        # 2、读取直接追加字典 并进行规则解析、变量替换处理
        if GB_ADD_DIRECT_DICT:
            # module = '读取直接追加路径'
            direct_path_list = read_path_files_and_rule_parse_frequency(dir_path=direct_path,
                                                                        ext_list=GB_DICT_SUFFIX,
                                                                        frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                                        annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                                        frequency_min=GB_FREQUENCY_MIN,
                                                                        replace_dict=base_var_replace_dict)
            base_path_list.extend(direct_path_list)
            output(f"[+] 加载元素数量 {len(direct_path_list)} <--> {direct_path}", level=LOG_INFO)

        # 3、读取笛卡尔积路径 字典 并进行规则解析、变量替换处理
        if GB_ADD_GROUP_DICT:
            # 按频率 读取笛卡尔积路径 -> 目录 字典下的所有文件,并进行解析
            # module = '读取笛卡尔积路径 -> 目录'
            group_folder_list = read_path_files_and_rule_parse_frequency(dir_path=group_dirs,
                                                                         ext_list=GB_DICT_SUFFIX,
                                                                         frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                                         annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                                         frequency_min=GB_FREQUENCY_MIN,
                                                                         replace_dict=base_var_replace_dict)
            output(f"[+] 加载元素数量 {len(group_folder_list)} <--> {group_dirs}", level=LOG_INFO)

            # 按频率 读取笛卡尔积路径 -> 文件 字典下的所有文件,并进行解析
            # module = '读取笛卡尔积路径 -> 文件'
            group_files_list = read_path_files_and_rule_parse_frequency(dir_path=group_file,
                                                                        ext_list=GB_DICT_SUFFIX,
                                                                        frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                                        annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                                        frequency_min=GB_FREQUENCY_MIN,
                                                                        replace_dict=base_var_replace_dict)
            output(f"[+] 加载元素数量 {len(group_files_list)} <--> {group_file}", level=LOG_INFO)

            # 组合 group_folder_list group_files_list
            group_dict_list, _ = product_folders_and_files(group_folder_list, group_files_list)
            base_path_list.extend(group_dict_list)

    return base_path_list


if __name__ == '__main__':
    gen_base_scan_path_list(cur_rule_dir_list=GB_DICT_RULE_SCAN)
    # 获取目录下所有文件名
    dir_path = r"C:\Users\WINDOWS\GithubProject\DynaScan\dict_rule\backup\direct_path"
    path_files = get_dir_path_file_info_dict(dir_path=dir_path, ext_list=[".txt"])
    print(path_files)