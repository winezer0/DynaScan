#!/usr/bin/env python
# encoding: utf-8
import os.path

from libs.lib_args.input_const import *
from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str
from libs.lib_dyna_rule.base_rule_parser import base_rule_render_list
from libs.lib_dyna_rule.dyna_rule_tools import get_key_list_with_freq
from libs.lib_file_operate.file_path import get_dirs_file_info_dict
from libs.lib_file_operate.rw_freq_file import read_files_to_freq_dict
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_ERROR
from libs.lib_url_analysis.url_handle import specify_ext_store, specify_ext_delete, replace_multi_slashes, \
    remove_url_end_symbol, url_path_lowercase, url_path_chinese_encode, url_path_url_encode
from libs.lib_url_analysis.url_parser import combine_urls_and_paths
from libs.lib_url_analysis.url_tools import urls_to_url_paths
from libs.util_func import product_folders_and_files


def read_dir_and_parse_rule_with_freq(read_dir_path, ext_list, freq_symbol, anno_symbol, freq_min, replace_dict):
    # 按频率读取目录下的所有字典文件,并进行动态解析

    # 读取前判断文件路径是否存在
    if not os.path.exists(read_dir_path):
        return []

    # 获取目录下所有文件名
    files_info = get_dirs_file_info_dict(dir_path=read_dir_path, ext_list=ext_list)

    # 读取前判断文件路径是否存在
    if not files_info:
        return []

    # 读取目录下所有文件内容到频率字典
    path_freq_dict = read_files_to_freq_dict(list(files_info.keys()), freq_symbol=freq_symbol, anno_symbol=anno_symbol)
    # 筛选频率字典
    path_freq_list = get_key_list_with_freq(path_freq_dict, freq_min)

    # 对 列表 中的规则进行 进行 动态解析
    path_freq_list, _, _ = base_rule_render_list(path_freq_list)

    # 对每个元素进行规则替换
    path_freq_list, _, _ = replace_list_has_key_str(path_freq_list, replace_dict)

    return path_freq_list


def combine_urls_and_path_dict(base_urls, paths_dict):
    # 组合URL列表和URL路径dict # 区分不同的基本URL,并拼接不同的路径字典
    url_list = []
    for keys, paths in paths_dict.items():
        if keys == STR_BASE_ROOT:
            url_list = combine_urls_and_paths(base_urls, paths, absolute=True)
            url_list.extend(url_list)
        else:
            url_list = combine_urls_and_paths(base_urls, paths, absolute=False)
            url_list.extend(url_list)
    url_list = list(set(url_list))
    return url_list


def url_and_paths_dict_handle(url_list, config_dict):
    # 对最后生成的URL进行处理
    new_url_list = []
    url_paths_dict = urls_to_url_paths(url_list)
    for url, paths in url_paths_dict.items():
        # 进行path处理
        paths = path_list_handle(paths, config_dict)
        # url_paths_dict[url] = paths
        # 组合新的url
        combine_urls = combine_urls_and_paths([url], paths)
        new_url_list.extend(combine_urls)

    # URL列表去重
    new_url_list = list(set(new_url_list))
    return new_url_list


def path_list_handle(path_list, config_dict):
    # 对列表中的所有PATH添加指定前缀
    if config_dict[GB_CUSTOM_URL_PREFIX]:
        path_list = product_folders_and_files(config_dict[GB_CUSTOM_URL_PREFIX], path_list)
        output(f"[*] 自定义前缀 剩余元素 {len(path_list)}个", level=LOG_INFO)

    # 保留指定后缀的URL目标
    if config_dict[GB_ONLY_SCAN_SPECIFY_EXT]:
        path_list = specify_ext_store(path_list, config_dict[GB_ONLY_SCAN_SPECIFY_EXT])
        output(f"[*] 保留指定后缀 剩余元素 {len(path_list)}个", level=LOG_ERROR)

    # 移除指定后缀列表的内容
    if config_dict[GB_NO_SCAN_SPECIFY_EXT]:
        path_list = specify_ext_delete(path_list, config_dict[GB_NO_SCAN_SPECIFY_EXT])
        output(f"[*] 移除指定后缀 剩余元素 {len(path_list)}个", level=LOG_ERROR)

    # 是否开启结尾字符列表去除
    if config_dict[GB_REMOVE_END_SYMBOLS]:
        path_list = remove_url_end_symbol(path_list, remove_symbol_list=config_dict[GB_REMOVE_END_SYMBOLS])
        output(f"[*] 删除结尾字符 剩余元素 {len(path_list)}个", level=LOG_INFO)

    # 是否开启REMOVE_MULTI_SLASHES,将多个////转换为一个/
    if config_dict[GB_REMOVE_MULTI_SLASHES]:
        path_list = replace_multi_slashes(path_list)
        output(f"[*] 转换多个[/]为单[/] 剩余URL:{len(path_list)}个", level=LOG_INFO)

    # 全部路径小写
    if config_dict[GB_URL_PATH_LOWERCASE]:
        path_list = url_path_lowercase(path_list)
        output(f"[*] 全部路径小写 剩余元素 {len(path_list)}个", level=LOG_INFO)

    # 批量解决字典中文乱码问题
    if config_dict[GB_CHINESE_ENCODE]:
        if config_dict[GB_ONLY_ENCODE_CHINESE]:
            # 将URL字典中的中文路径进行多种编码的URL编码
            path_list = url_path_chinese_encode(path_list, config_dict[GB_CHINESE_ENCODE])
            output(f"[+] 中文编码完毕 剩余元素 {len(path_list)}个", level=LOG_INFO)
        else:
            # 将URL字典的所有元素都进行多种编码的URL编码
            path_list = url_path_url_encode(path_list, config_dict[GB_CHINESE_ENCODE])
            output(f"[+] URL编码完毕 剩余元素 {len(path_list)}个", level=LOG_INFO)

    return path_list
