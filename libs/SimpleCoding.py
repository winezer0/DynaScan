#!/usr/bin/env python
# encoding: utf-8

# 简单的判断文件编码类型
# 说明：UTF兼容ISO8859-1和ASCII，GB18030兼容GBK，GBK兼容GB2312，GB2312兼容ASCII
CODES = ['UTF-8', 'GB18030', 'BIG5']
# UTF-8 BOM前缀字节
UTF_8_BOM = b'\xef\xbb\xbf'


def file_encoding(file_path: str):
    """
    获取文件编码类型

    :param file_path: 文件路径
    :return:
    """
    with open(file_path, 'rb') as f:
        return string_encoding(f.read())


def string_encoding(data: bytes):
    """
    获取字符编码类型

    :param data: 字节数据
    :return:
    """
    # 遍历编码类型
    for code in CODES:
        try:
            data.decode(encoding=code)
            if 'UTF-8' == code and data.startswith(UTF_8_BOM):
                return 'UTF-8-SIG'
            return code
        except UnicodeDecodeError:
            continue
    return 'unknown'

if __name__ == '__main__':
    import SimpleCoding
    import requests
    # 检测文件编码
    print(SimpleCoding.file_encoding('test1.txt'))
    print(SimpleCoding.file_encoding('test2.txt'))
    # 检测字符串编码
    print(SimpleCoding.string_encoding(requests.get('https://www.baidu.com').content))