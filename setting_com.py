#!/usr/bin/env python
# encoding: utf-8
from pathlib import Path
import time
from libs.lib_args.input_const import *
from libs.lib_file_operate.file_utils import auto_make_dir


def init_common(config):
    """
    初始化本程序的通用参数
    :param config:
    :return:
    """
    ##################################################################
    # 获取setting.py脚本所在路径作为的基本路径
    config[GB_BASE_DIR] = Path(__file__).parent.resolve()
    ##################################################################
    # 程序开始运行时间
    config[GB_RUN_TIME] = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    ##################################################################
    # 版本号配置
    config[GB_VERSION] = "Ver 0.6.1 2023-07-28 17:30"
    ##################################################################
    # 是否显示DEBUG级别信息,默认False
    config[GB_DEBUG_FLAG] = False
    ##################################################################
    # 设置日志输出文件路径 #目录不存在会自动创建
    config[GB_LOG_INFO_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_info.log").as_posix()
    config[GB_LOG_DEBUG_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_debug.log").as_posix()
    config[GB_LOG_ERROR_FILE] = config[GB_BASE_DIR].joinpath("runtime", "runtime_error.log").as_posix()
    ##################################################################


def init_custom(config):
    ##################################################################
    # 记录不可访问的目标 # 没啥用
    config[GB_ACCESS_NO_FILE] = config[GB_BASE_DIR].joinpath("runtime", "access_no.log").as_posix()
    # 记录可以访问的目标 # 没啥用
    config[GB_ACCESS_OK_FILE] = config[GB_BASE_DIR].joinpath("runtime", "access_ok.log").as_posix()

    # 缓存检测动态排除字典
    config[GB_DYNA_DICT_CACHE] = config[GB_BASE_DIR].joinpath("runtime", "{mark}.cache.json").as_posix()
    ##################################################################
    #  扫描URL的排除过滤,建议开启
    config[GB_EXCLUDE_HISTORY] = True
    # 记录扫描已完成的URL 针对每个目标生成不同的记录文件
    config[GB_HISTORY_FORMAT] = config[GB_BASE_DIR].joinpath("runtime", "{mark}.history.log").as_posix()
    # 自定义排除的历史URLs,用于联动其他工具
    config[GB_EXCLUDE_URLS] = config[GB_BASE_DIR].joinpath("exclude_urls.txt").as_posix()
    ##################################################################
    # 设置输出结果文件目录
    config[GB_RESULT_DIR] = config[GB_BASE_DIR].joinpath("result")
    auto_make_dir(config[GB_RESULT_DIR])
    ##################################################################
    # 在配置文件中配置默认目标参数  支持文件 或 URL
    config[GB_TARGET] = "target.txt"
    ##################################################################
    # 每个目标的最大扫描URL阈值[数字] 辅助调试 或 其他用途
    config[GB_MAX_URL_NUM] = None
    ##################################################################
    # 停止扫描阈值[数字] # 如果每个目标的非正常响应超过这个阈值, 就停止任务
    config[GB_MAX_ERROR_NUM] = None
    ##################################################################
    # 对输入的URL路径进行分解 # 示例：https://XXX/item/DD/ 会被分解为 https://XXX/item/DD/,https://XXX/item/,https://XXX/
    config[GB_SPLIT_TARGET] = True
    ##################################################################
    # 是否开启命中结果动态排除开关，排除相同的命中结果。适用于网站路由是正则的情况 /index.xxx = /index
    config[GB_HIT_INFO_EXCLUDE] = True
    # 是否保存命中结果到HIT_XXX文件
    config[GB_SAVE_HIT_RESULT] = True
    # 命中结果文件追加模式
    config[GB_HIT_OVER_CALC] = True
    # True,计算频率后覆盖写入、后期写入时内存占用大,磁盘占用小,读取效率高
    # False 直接追加命中记录、后期写入时内存占用小,磁盘占用大,读取效率低
    # 存储命中的路径
    config[GB_HIT_PATH_FILE] = config[GB_BASE_DIR].joinpath("dict_hit", 'HIT_DIRECT.hit')
    # 存储命中的目录名
    config[GB_HIT_DIR_FILE] = config[GB_BASE_DIR].joinpath("dict_hit", 'HIT_FOLDER.hit')
    # 存储命中的文件名
    config[GB_HIT_FILE_FILE] = config[GB_BASE_DIR].joinpath("dict_hit", 'HIT_FILE.hit')
    # 存储命中的后缀
    config[GB_HIT_EXT_FILE] = config[GB_BASE_DIR].joinpath("dict_hit", 'HIT_EXT.hit')
    ##################################################################
