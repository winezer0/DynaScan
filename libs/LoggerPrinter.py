#!/usr/bin/env python
# encoding: utf-8

import sys

from loguru import logger


def set_logger(info_log_file_path=None, err_log_file_path=None, dbg_log_file_path=None, debug=None):
    # 初始化日志记录器
    logger.remove()  # remove()清除之前的设置

    # logger_format_simple = "<level>{message}</level>"
    # logger_format_simple  输出时没有颜色,写入文件时相同# [*] 正在对目标列表进行初步访问测试 ['http://127.0.0.1:8080', 'http://127.0.0.1:8888']
    # logger_format_common = "[<green>{time:HH:mm:ss}</green>] <level>{message}</level>"
    # logger_format_common  输出时有颜色,写入文件时没有影响# [12:44:44] [*] 所有有效输入目标: ['https://www.baidu.com', 'https://baike.baidu.com']
    # logger_format_complex = "<green>{time:YYYY-MM-DD HH:mm:ss,SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    # logger_format_complex 输出时有多种颜色,写入文件时没有影响# 2022-03-08 12:43:28,341 | INFO     | __main__:main:637 - [+] 目标 https://baike.baidu.com 二次字典规则渲染开始...

    logger_format_write = "[{time:HH:mm:ss}] <level>{message}</level>"
    # logger_format_write 没有颜色 # [12:46:19] [*] 没有协议头的目标列表 ['http://127.0.0.1:8080', 'http://127.0.0.1:8888']

    # 选择写入到文件使用哪个格式
    logger_format_writer = logger_format_write

    # 设置显示INFO到桌面
    # logger.add(sys.stdout, format=logger_format1, level="INFO")

    # 设置显示DEBUG到桌面
    # logger.add(sys.stdout, format=logger_format1, level="DEBUG")

    # 设置显示INFO到文件
    logger.add(info_log_file_path, format=logger_format_writer, level="INFO", rotation="10 MB", enqueue=True,encoding="utf-8", errors="ignore")
    # 设置显示DEBUG到文件
    logger.add(dbg_log_file_path, format=logger_format_writer, rotation="10 MB", level="DEBUG", enqueue=True, encoding="utf-8",errors="ignore")
    # 设置显示ERROR到文件
    logger.add(err_log_file_path, format=logger_format_writer, rotation="10 MB", level="ERROR", enqueue=True, encoding="utf-8",errors="ignore")

    # 根据输入的debug参数指定窗口输出的日志信息级别,不执行语句会导致没有控制台页面输出
    logger_format_show_info= "[<blue>{time:HH:mm:ss}</blue>] <level>{message}</level>"
    logger_format_show_debug= "[<green>{time:HH:mm:ss}</green>] <level>{message}</level>"
    if debug:
        logger.add(sys.stdout, format=logger_format_show_debug, level="DEBUG")
    else:
        logger.add(sys.stdout, format=logger_format_show_info, level="INFO")
    return logger
