import ipaddress


def convert_range_to_cidr(ip_ranges):
    """
    转换 IP范围 格式到 IP cidr  测试通过
    :param ip_range:
    :return:
    """
    ip_ranges = [ip_ranges] if isinstance(ip_ranges, str) else ip_ranges

    cidr_blocks = []
    for ip_range in ip_ranges:
        if "-" not in ip_range:
            cidr_blocks.append(ip_range)
            continue

        # 将IP范围拆分为起始IP和结束IP
        start_ip, end_ip = ip_range.split('-')

        # 判断IP是否C段相同
        start_c_segment = '.'.join(start_ip.split('.')[:3])
        end_c_segment = '.'.join(end_ip.split('.')[:3])
        if not start_c_segment == end_c_segment:
            print(f"IP范围不在同一个C段 {ip_range} 跳过处理...")
            continue

        # 判断是否是单个IP
        if start_ip.strip() == end_ip.strip():
            cidr_block = f"{start_ip}/32"
            cidr_blocks.append(str(cidr_block))
            continue

        # 将起始IP和结束IP转换为IPv4Address对象
        start_ip = ipaddress.IPv4Address(start_ip.strip())
        end_ip = ipaddress.IPv4Address(end_ip.strip())
        # 将起始IP和结束IP转换为整数形式
        start_int = int(start_ip)
        end_int = int(end_ip)
        # 计算网络前缀长度
        xor_result = start_int ^ end_int
        prefix_length = 32 - len(bin(xor_result)) + 2
        # 创建CIDR IP地址块
        cidr_block = ipaddress.ip_network(f"{start_ip}/{prefix_length}", strict=False)
        cidr_blocks.append(str(cidr_block))
    return cidr_blocks


def convert_ip_to_range(ip_list):
    # 将IP转换为精细的IP范围和IP

    if isinstance(ip_list, str):
        return ip_list

    # 将IP地址字符串转换为IPv4Address对象
    ips = [ipaddress.IPv4Address(ip.strip()) for ip in ip_list]
    # 对IP地址进行排序
    sorted_ips = sorted(ips)

    merged_ranges = []
    while sorted_ips:
        start_ip = sorted_ips[0]
        end_ip = start_ip
        # 找到连续的IP地址段
        for ip in sorted_ips[1:]:
            if ip == end_ip + 1:
                end_ip = ip
            else:
                break

        # 创建合并后的IP范围字符串
        ip_range = f"{start_ip}-{end_ip}" if start_ip != end_ip else f"{end_ip}"
        sorted_ips = sorted_ips[len(ip_range.split('-')):]
        merged_ranges.append(ip_range)
    return merged_ranges


def convert_ip_to_range_fuzz(ip_lists):
    def split_ips_2_c_seg(ip_list):
        # 将IP列表按C段分离  输出二维列表，每个子元素是一个C段
        c_ranges = {}
        for ip in ip_list:
            # 提取前三段IP地址作为C段
            c_segment = '.'.join(ip.split('.')[:3])
            # 将IP添加到对应的C段列表中
            if c_segment in c_ranges:
                c_ranges[c_segment].append(ip)
            else:
                c_ranges[c_segment] = [ip]
        return list(c_ranges.values())

    # 将IP列表转换为模糊的IP段，注意,只建议操作C段值 不然会出现类似结果  1.1.1.1-192.168.88.88

    # 转换 IP 列表为IP C段列表
    c_ip_list = split_ips_2_c_seg(ip_lists)

    ip_range_list = []

    for c_ips in c_ip_list:
        if len(c_ips) == 1:
            ip_range_list.append(c_ips[0])
            continue

        # 将IP列表转换为IPv4Address对象列表
        ip_addresses = [ipaddress.IPv4Address(ip.strip()) for ip in c_ips]
        # 对IP地址进行排序
        sorted_ips = sorted(ip_addresses)
        # 获取最小和最大IP地址
        min_ip = sorted_ips[0]
        max_ip = sorted_ips[-1]
        # 构建IP范围地址字符串
        ip_range = f"{min_ip}-{max_ip}"
        ip_range_list.append(ip_range)
    return ip_range_list


if __name__ == '__main__':
    # ips = "192.168.88.1 192.168.88.2 192.168.88.88 1.1.1.1 192.168.88.1"
    # # 输入多个IP地址，以空格分隔
    ip_list = "192.168.88.1 192.168.88.2 192.168.88.88 1.1.1.1 2.2.2.2 3.3.3.3 3.3.3.4".split()
    ip_to_range = convert_ip_to_range(ip_list)
    ip_to_range_fuzz = convert_ip_to_range_fuzz(ip_list)
    range_to_cidr = convert_range_to_cidr(ip_to_range)
    range_to_cidr_fuzz = convert_range_to_cidr(ip_to_range_fuzz)

    # 发现2.2.2.2的IP被吃掉了
    print(ip_to_range)  # 错误 ['1.1.1.1', '3.3.3.3-3.3.3.4', '192.168.88.1-192.168.88.2', '192.168.88.88']
    print(ip_to_range_fuzz)
    print(range_to_cidr)  # 错误 ['1.1.1.1', '3.3.3.0/29', '192.168.88.0/30', '192.168.88.88']
    print(range_to_cidr_fuzz)
