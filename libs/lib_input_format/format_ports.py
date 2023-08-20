#!/usr/bin/env python
# encoding: utf-8
from urllib.parse import urlparse


def remove_80_443(url):
    parsed_url = urlparse(url)
    if parsed_url.port in [80, 443]:
        return f"{parsed_url.scheme}://{parsed_url.hostname}"
    return url


def parse_ports(ports):
    # 解析输入的端口字符串列表
    ports = ports if isinstance(ports, list) else [ports]

    # 进行格式解析 第一次解析 分割逗号和空格
    tmp = []
    for port in ports:
        if isinstance(port, int):
            tmp.append(port)
        elif "," in str(port):
            tmp.extend(str(port).split(","))
        elif " " in str(port):
            tmp.extend(str(port).split(" "))
        else:
            tmp.append(port)

    # 解析格式解析 第三次解析
    result = []
    for port in tmp:
        if '-' in str(port):
            port_start = int(port.split("-")[0].strip())
            port_end = int(port.split("-")[1].strip())
            if port_end < port_start:
                result.extend([gen_port for gen_port in range(port_end, port_start + 1)])
            else:
                result.extend([gen_port for gen_port in range(port_start, port_end + 1)])
        elif isinstance(port, int) or str(port).isdigit():
            result.append(port)
        else:
            print(f"[!] 端口格式输入错误: {port}")

    # 进行数据去重
    result = [str(port) for port in result]
    result = list(dict.fromkeys(result))
    return result
