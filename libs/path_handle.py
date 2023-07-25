#!/usr/bin/env python
# encoding: utf-8

from libs.lib_args.input_const import *
from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_ERROR
from libs.lib_url_analysis.url_handle import specify_ext_store, specify_ext_delete, replace_multi_slashes, \
    remove_url_end_symbol, url_path_lowercase, url_path_chinese_encode, url_path_url_encode
from libs.lib_url_analysis.url_parser import combine_urls_and_paths
from libs.lib_url_analysis.url_tools import urls_to_url_paths
from libs.utils import product_folders_and_files


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
