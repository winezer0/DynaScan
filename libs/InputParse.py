#!/usr/bin/env python
# encoding: utf-8
import sys
sys.dont_write_bytecode = True  # 设置不生成pyc文件

import argparse
# 获取版本号,并返回版本号字符串
from setting import version

# 获取版本号,并返回版本号字符串
def get_version():
    return '[*] 当前的工具版本号为: {} !!!'.format(version)


class ParserCmd(object):

    def __init__(self):
        super(ParserCmd, self).__init__()
        self.parser = self.my_parser()
        self.args = self.parser.parse_args().__dict__

    def my_parser(self):
        example = """Examples:
                          \r  python3 {shell_name} -u http://www.baidu.com
                          \r  python3 {shell_name} -f target.txt
                          \r  python3 {shell_name} -f target.txt -p http://127.0.0.1:8080
                          \r  
                          \r  其他控制细节参数请通过setting.py进行配置
                          \r  
                          \r  T00L Version: {version}
                          \r  
                          """

        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True,)
        parser.epilog = example.format(shell_name=parser.prog, version=version)
        parser.add_argument("-u", dest="target", type=str, default=None, help="指定扫描目标URL, Example: http://www.baidu.com")

        parser.add_argument("-f", dest="target_file", type=str, default=None, help="指定扫描目标URL文件, Example: target.txt")

        parser.add_argument("-p", dest="proxy", type=str, default=None, help="指定请求时使用的HTTPS或SOCKS5的代理, Example: http://127.0.0.1:8080 or socks5://127.0.0.1:1080")

        parser.add_argument("-t", dest="threads_count", type=int, default=None, help="指定多线程池的最大线程数")

        parser.add_argument("-d", dest="debug", default=False, action="store_true", help="显示程序运行时的所有调试信息,默认关闭")

        parser.add_argument("-v", "--version", action="version", version=get_version(), help="显示程序当前版本号")
        return parser

    @staticmethod
    def init():
        parser = ParserCmd()

        return parser.args


if __name__ == '__main__':
    args = ParserCmd().init()
    print(args)
