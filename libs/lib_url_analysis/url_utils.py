#!/usr/bin/env python
# encoding: utf-8

import itertools
from urllib.parse import urljoin, urlparse


def combine_dir_to_paths(words):
    # 将有序的目录列表重新组合为多层次的路径
    paths = []
    # 构建每一层目录的 URL
    current_url = "/"
    paths.append(current_url)
    for directory in words:
        current_url += directory + "/"
        paths.append(current_url)
    # print(f"full_paths: {full_paths}") # ['/', '/aaa/', '/aaa/bbb/']
    return paths


def combine_urls_and_paths(url_list, path_list, absolute=False):
    # 组合URl和路径
    url_path_tuples = list(itertools.product(url_list, path_list))
    url_path_list = []
    for url, path in url_path_tuples:
        if absolute:
            # 追加到根目录
            url_path_list.append(urljoin(url, f"/{str(path).lstrip('/')}"))
        else:
            # 追加到当前目录
            url_path_list.append(urljoin(url, f"./{str(path).lstrip('/')}"))
    # 去重URL
    url_path_list = list(set(url_path_list))
    return url_path_list


def get_url_ext(url, extension=None):
    # 获取URL的脚本语言后缀
    """
    # url = 'http://www.baidu.com' # 没有后缀,返回 None
    # url = 'http://www.baidu.com/xxx' # 没有后缀, 返回 None
    # url = 'http://www.baidu.com/xxx.xxx'  # 有后缀,返回 xxx
    """
    # 拆分长URL为多个URL目录
    parser_url = urlparse(url)
    path = [dirs for dirs in parser_url.path.split('/') if dirs.strip()]
    if len(path) >= 1:
        filename = path[-1].split('.')
        if len(filename) > 1:
            return filename[-1]
        else:
            return extension
    else:
        return extension
    return extension


def urls_to_url_paths(url_list):
    # 拆分URL和路径 可能是多个host
    url_path_dict = {}
    for url in url_list:
        parsed_url = urlparse(url)
        url_part = f"{parsed_url.scheme}://{parsed_url.netloc}"
        path_part = parsed_url.path
        # setdefault 方法检查字典中是否存在指定的键，如果不存在则将其添加到字典中
        url_path_dict.setdefault(url_part, []).append(path_part)
    return url_path_dict


def get_segment_urls(url):
    # 拆分长URL为多个URL目录
    parser_url = urlparse(urljoin(url, "./"))
    words = [dirs for dirs in parser_url.path.split('/') if dirs.strip()]
    # print(f"words:{words}") # words:['aaa', 'bbb']
    paths = combine_dir_to_paths(words)
    # print(f"paths:{paths}")  # paths:['/', '/aaa/', '/aaa/bbb/']
    urls = combine_urls_and_paths([urljoin(url, "/")], paths, absolute=False)
    # print(f"urls:{urls}") # urls:['https://www.baidu.com/aaa/bbb/', 'https://www.baidu.com/', 'https://www.baidu.com/aaa/']
    return urls