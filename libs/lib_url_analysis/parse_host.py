#!/usr/bin/env python
# encoding: utf-8
from urllib.parse import urlparse


def get_proto(url):
    # 从URL中获取HTTP协议
    scheme = urlparse(url).scheme
    return scheme


def get_host_port(url, replace_symbol=False):
    """
    从URL中获取HOST头部
    output(get_host_port('http://www.baidu.com.cn:8080/111/222/3.aspx?p=123')) #www.baidu.com.cn:8080
    """
    path_obj = urlparse(url)
    host_port = path_obj.netloc
    if replace_symbol:
        host_port = str(host_port).replace(":", "_")
    return host_port


def get_proto_host(url, replace_symbol=False):
    path_obj = urlparse(url)
    scheme = path_obj.scheme
    host_port = path_obj.netloc
    result = f"{scheme}://{host_port}"
    if replace_symbol:
        result = str(result).replace(":", "_").replace("/", "_")
    return result
