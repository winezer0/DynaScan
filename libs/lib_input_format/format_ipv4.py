#!/usr/bin/env python
# encoding: utf-8
import ipaddress
import re


def is_ipv4(string):
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    return re.match(ip_pattern, string) is not None


def is_ip_cidr_by_ipaddress(address):
    try:
        # strict 设置支持非严格网段
        ip_network = ipaddress.IPv4Network(address, strict=False)
        return True
    except ValueError:
        return False


def is_ip_cidr(address):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$'
    if re.match(pattern, address):
        return True
    else:
        return False


def is_ip_range_l(address):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}-(\d{1,3}\.){3}\d{1,3}$'
    if re.match(pattern, address):
        return True
    else:
        return False


def is_ip_range_s(address):
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.)\d{1,3}-(\d{1,3})$'
    match = re.match(pattern, address)
    if match:
        return True
    else:
        return False


def parse_ip_cidr(cidr):
    ip_list = []
    try:
        network = ipaddress.IPv4Network(cidr, strict=False)
        ip_list = [str(ip) for ip in network.hosts()]
    except ValueError as e:
        print(f"Invalid IP CIDR: {e}")
    return ip_list


def parse_ip_range_s(ip_range):
    ip_list = []
    pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.)(\d{1,3})-(\d{1,3})$'
    match = re.match(pattern, ip_range)
    if match:
        ip_prefix = match.group(1)
        start_ip = int(match.group(2))
        end_ip = int(match.group(3))

        for i in range(start_ip, end_ip + 1):
            ip_list.append(f"{ip_prefix}{i}")
    else:
        print(f"Invalid IP range format: {ip_range}")
    return ip_list


def parse_ip_range_l(ip_range):
    ip_list = []
    try:
        start_ip, end_ip = ip_range.split("-")
        start_ip = ipaddress.IPv4Address(start_ip.strip())
        end_ip = ipaddress.IPv4Address(end_ip.strip())
        for ip in range(int(start_ip), int(end_ip) + 1):
            ip_list.append(str(ipaddress.IPv4Address(ip)))
    except ValueError:
        print(f"Invalid IP range format:{ip_range}")
    return ip_list


def remove_private_ips(ip_list):
    public_ips = []
    for ip in ip_list:
        try:
            # 验证IP地址或CIDR网段是否有效
            ip_network = ipaddress.ip_network(ip, strict=False)
            # 排除私有IP地址
            if not ip_network.is_private:
                public_ips.append(str(ip_network))
        except ValueError:
            print(f"无效的IP地址或CIDR网段: {ip}")
    return public_ips


if __name__ == '__main__':
    if is_ip_range_s("1.1.1.1-2"):
        print(parse_ip_range_s("1.1.1.1-2"))

    if is_ip_range_l("1.1.1.1-1.1.2.2"):
        print(parse_ip_range_l("1.1.1.1-1.1.2.2"))

    if is_ip_cidr("1.1.1.1/28"):
        print(parse_ip_cidr("1.1.1.1/26"))
