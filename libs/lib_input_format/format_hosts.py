#!/usr/bin/env python
# encoding: utf-8
import re
from urllib.parse import urlparse

from libs.lib_input_format.format_ipv4 import is_ipv4, is_ip_cidr, is_ip_range_l, is_ip_range_s, parse_ip_cidr, \
    parse_ip_range_l, parse_ip_range_s


def is_http_url(string):
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return re.match(pattern, string) is not None


def is_valid_url(target):
    parsed_url = urlparse(target)
    return parsed_url.scheme != '' and parsed_url.netloc != ''


def is_host_port(string):
    pattern = r'^[a-zA-Z0-9.-]+:\d+$'
    return re.match(pattern, string) is not None


def is_domain(string):
    domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(domain_pattern, string) is not None


def extract_host_from_url(url):
    # 提取URL中的HOST部分,不包含端口号
    parsed_url = urlparse(url)
    # parsed_url.hostname 返回的结果不包含端口号。只返回URL中的主机名部分。
    host = parsed_url.hostname
    return host


def extract_host_from_host(host):
    # 提取host中的HOST部分,不包含端口号
    # parsed_url.hostname 返回的结果不包含端口号。只返回URL中的主机名部分。
    if ":" in host:
        host = str(host).split(":", 1)[0]
    return host


def classify_hosts(hosts, parse_cidr=True):
    # 将目标分类为  IP, Domain, HOST_PORT, PROTO_HOST_PORT
    list_ipv4 = []  # 存储 纯IP
    list_domain = []  # 存储 纯域名
    list_host_port = []  # 存储IP:Port|域名:Port
    list_proto_host_port = []  # 存储 URL
    # list_error = []
    for host in hosts:
        if is_http_url(host):
            list_proto_host_port.append(host)
        elif is_host_port(host):
            list_host_port.append(host)
        elif is_ipv4(host):
            list_ipv4.append(host)
        elif is_domain(host):
            list_domain.append(host)
        elif is_ip_cidr(host):
            if parse_cidr:
                list_ipv4.extend(parse_ip_cidr(host))
            else:
                list_ipv4.append(host)
        elif is_ip_range_s(host):
            list_ipv4.extend(parse_ip_range_s(host))
        elif is_ip_range_l(host):
            list_ipv4.extend(parse_ip_range_l(host))
        else:
            # list_error.append(target)
            print(f"[-] 发现错误格式的输入数据:{host}")

    # 去重输入目标
    list_proto_host_port = list(dict.fromkeys(list_proto_host_port))
    list_host_port = list(dict.fromkeys(list_host_port))
    list_domain = list(dict.fromkeys(list_domain))
    list_ipv4 = list(dict.fromkeys(list_ipv4))
    return list_proto_host_port, list_host_port, list_ipv4, list_domain


