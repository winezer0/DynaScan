#!/usr/bin/env python
# encoding: utf-8
import itertools
import os
from urllib.parse import urljoin, urlparse


def get_root_dir_url(url):
    # 从URL中提取根目录URL(末尾有/)
    # parsed_url = urlparse(url)
    # root_dir_url = parsed_url.scheme + "://" + parsed_url.netloc
    root_dir_url = urljoin(url, "/")  # 新方案
    return root_dir_url


def get_curr_dir_url(url):
    # 获取当前url的当前目录URL(末尾有/)
    curr_dir_url = urljoin(url, "./")
    return curr_dir_url


def split_path_to_words(path):
    # 切割path路径为多个单词
    words = []
    for dirs in path.split('/'):
        if dirs != '':
            words.append(dirs)
    # print(f"words: {words}")  # words: ['aaa', 'bbb']
    return words


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


def get_segment_urls(url):
    # 拆分长URL为多个URL目录
    parser_url = urlparse(get_curr_dir_url(url))
    words = split_path_to_words(parser_url.path)
    # print(f"words:{words}") # words:['aaa', 'bbb']
    paths = combine_dir_to_paths(words)
    # print(f"paths:{paths}")  # paths:['/', '/aaa/', '/aaa/bbb/']
    urls = combine_urls_and_paths([get_root_dir_url(url)], paths, absolute=False)
    # print(f"urls:{urls}") # urls:['https://www.baidu.com/aaa/bbb/', 'https://www.baidu.com/', 'https://www.baidu.com/aaa/']
    return urls


def get_url_ext(url, extension=None):
    # 获取URL的脚本语言后缀
    """
    # url = 'http://www.baidu.com' # 没有后缀,返回 None
    # url = 'http://www.baidu.com/xxx' # 没有后缀, 返回 None
    # url = 'http://www.baidu.com/xxx.xxx'  # 有后缀,返回 xxx
    """
    # 拆分长URL为多个URL目录
    parser_url = urlparse(url)
    path = split_path_to_words(parser_url.path)
    if len(path) >= 1:
        filename = path[-1].split('.')
        if len(filename) > 1:
            return filename[-1]
        else:
            return extension
    else:
        return extension
    return extension


def list_ele_in_str(list_=None, str_=None, default=True):
    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag


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


def parse_url_path_part(url):
    # 分割一个URL为基本URL和路径
    parsed_url = urlparse(url)
    url_part = f"{parsed_url.scheme}://{parsed_url.netloc}"
    path_part = parsed_url.path
    return url_part, path_part


def parse_url_file_part(url):
    # 提取URL中的文件名和扩展名
    # "https://www.baidu.com/aaa/bbb/index.php?a=1"  # ('index.php', 'index', '.php')
    # "https://www.baidu.com/aaa/bbb/index"  # ('index.php', 'index', '')
    # "https://www.baidu.com/aaa/bbb/"  # ('', '', '')
    # 解析 URL 获取路径部分
    parsed_url = urlparse(url)
    path = parsed_url.path

    # 提取文件名和扩展名
    file_name = os.path.basename(path)
    pure_name, file_ext = os.path.splitext(file_name)
    return file_name, pure_name


if __name__ == '__main__':
    surl = "https://www.baidu.com/aaa/index.php"
    # print(get_curr_dir_url(surl))  # https://www.baidu.com/aaa/
    # print(get_root_dir_url(surl))  # https://www.baidu.com

