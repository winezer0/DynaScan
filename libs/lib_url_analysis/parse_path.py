#!/usr/bin/env python
# encoding: utf-8
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


