#!/usr/bin/env python
# encoding: utf-8

# 解析输入参数
import argparse

from libs.lib_args.input_basic import extract_heads
from libs.lib_file_operate.file_path import get_sub_dirs
from libs.lib_log_print.logger_printer import *
from libs.lib_args.input_const import *
from libs.lib_requests.requests_const import HTTP_USER_AGENTS
from libs.lib_requests.requests_utils import random_ua, random_xff


def args_parser(config_dict):
    # RawDescriptionHelpFormatter 支持输出换行符
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)

    # description 程序描述信息
    argument_parser.description = """基于规则的动态备份文件扫描工具"""

    # 动态实现重复参数设置代码  # 可提取到函数外正常使用
    # 规则示例: { "param": "", "dest": "","name": "", "default": "", "nargs": "","action": "",  "choices": "", "type": "","help": ""}
    allowed_rules = get_sub_dirs(config_dict[GB_DICT_RULE_PATH]).values()

    args_options = [
        # 指定扫描URL或文件
        {"param": GB_TARGET, "nargs": "+", "help": f"指定URLs或URLs文件列表"},

        # 指定调用的字典目录
        {"param": GB_DICT_RULE_SCAN, "nargs": "+", "help": f"指定规则目录列表, 可选:{allowed_rules}", "choices": allowed_rules},

        # 指定最小提取频率
        {"param": GB_FREQUENCY_MIN, "type": int, "help": "指定最小规则频率, 小于该频率的规则不会被调用."},

        # 指定频率分割符号
        {"param": GB_FREQUENCY_SYMBOL, "help": "频率字符串连接符"},

        # 指定请求代理服务
        {"param": GB_PROXIES, "help": "HTTP代理 支持:http|https|socks5"},

        # 指定请求线程数量
        {"param": GB_THREADS_COUNT, "type": int, "help": "请求线程数"},

        # 开启调试功能
        {"param": GB_DEBUG_FLAG, "action": "store_true", "help": "开启调试功能"},

        # 开启随机UA
        {"param": GB_RANDOM_UA, "action": "store_true", "help": "开启随机UserAgent"},

        # 开启随机XFF
        {"param": GB_RANDOM_XFF, "action": "store_true", "help": "开启随机XFF头"},

        # 关闭流模式扫描
        {"param": GB_STREAM_MODE, "action": "store_false", "help": "关闭流模式扫描"},

        # 关闭历史扫描URL过滤
        {"param": GB_EXCLUDE_HISTORY, "action": "store_false", "help": "关闭历史扫描URL过滤"},

        # 手动指定排除扫描的URLs文件
        {"param": GB_EXCLUDE_URLS, "help": "手动指定需要排除扫描的URL文件"},

        # 关闭 URL目标可访问性判断
        {"param": GB_URL_ACCESS_TEST, "action": "store_false", "help": "关闭URL目标可访问性判断"},

        # 开启 目标URL拆分
        {"param": GB_SPLIT_TARGET, "action": "store_true", "help": "开启将目标URL拆分为多个子目录"},

        # 排除匹配指定的状态码的响应结果
        {"param": GB_EXCLUDE_STATUS, "nargs": "+", "type": int, "help": "指定需要排除的响应状态码列表"},

        # 排除匹配指定正则 响应结果
        {"param": GB_EXCLUDE_REGEXP, "help": "排除匹配指定正则的响应结果"},

        # 指定字典后缀名列表
        {"param": GB_DICT_SUFFIX, "nargs": "+", "help": "指定字典文件的后缀列表"},

        # 指定仅扫描的URL后缀名列表
        {"param": GB_ONLY_SCAN_SPECIFY_EXT, "nargs": "+", "help": "仅扫描指定后缀的URL列表"},

        # 指定不扫描的URL后缀名列表
        {"param": GB_NO_SCAN_SPECIFY_EXT, "nargs": "+", "help": "指定不扫描的URL后缀名列表"},

        # 为生成的每条字典添加特定前缀
        {"param": GB_CUSTOM_URL_PREFIX, "nargs": "+", "help": "为生成的每条字典添加特定前缀"},

        # 去除以特定字符结尾的URL
        {"param": GB_REMOVE_END_SYMBOLS, "nargs": "+", "help": "去除以特定字符结尾的URL"},

        # 指定默认请求方法
        {"param": GB_REQ_METHOD, "help": "指定默认请求方法"},

        #  指定请求超时时间
        {"param": GB_TIME_OUT, "type": int, "help": "指定请求超时时间"},

        # 指定自动错误重试次数
        {"param": GB_RETRY_TIMES, "type": int, "help": "指定自动错误重试次数"},
    ]

    param_dict = {"help": "h"}  # 存储所有长-短 参数对应关系,用于自动处理重复的短参数名
    options_to_argument(args_options, argument_parser, config_dict, param_dict)

    # 其他输出信息
    shell_name = argument_parser.prog
    argument_parser.epilog = f"""Examples:
    
             \r  批量扫描 target.txt
             \r  python3 {shell_name} --{param_dict[GB_TARGET]} target.txt
             
             \r  进行备份文件字典扫描,筛选频率10以上的字典:
             \r  python3 {shell_name} --{param_dict[GB_TARGET]} https://www.xxx.com --{param_dict[GB_DICT_RULE_SCAN]} backup -f 10
             
             \r  进行所有文件字典扫描,设置Socks5请求代理:
             \r  python3 {shell_name} --{param_dict[GB_TARGET]} https://www.baidu.com --{param_dict[GB_PROXIES]} socks5://127.0.0.1:1080
             \r
             \r  其他默认控制细节参数可通过setting_***.py 或 命令行 进行配置
             \r
             \r  Version: {config_dict[GB_VERSION]}
             \r  """

    args = argument_parser.parse_args()
    return args


def args_dict_handle(args):
    # 记录已经更新过的数据
    update_dict = {}
    # 格式化输入的Proxy参数 如果输入了代理参数就会变为字符串
    if args.proxies and isinstance(args.proxies, str):
        if "socks" in args.proxies or "http" in args.proxies:
            args.proxies = {
                'http': args.proxies.replace('https://', 'http://'),
                'https': args.proxies.replace('https://', 'http://')
            }
            update_dict["proxies"] = args.proxies
        else:
            output(f"[!] 输入的代理地址[{args.proxies}]不正确,正确格式:Proto://IP:PORT", level=LOG_ERROR)
    return update_dict


def config_dict_handle(config_dict):
    # 记录已经更新过的数据
    update_dict = {}
    # 格式化输入的规则目录
    if not config_dict[GB_DICT_RULE_SCAN]:
        config_dict[GB_DICT_RULE_SCAN] = get_sub_dirs(config_dict[GB_DICT_RULE_PATH]).values()
        update_dict[GB_DICT_RULE_SCAN] = config_dict[GB_DICT_RULE_SCAN]

    # HTTP 头设置
    update_headers = {}

    if config_dict[GB_RANDOM_UA]:
        update_headers['User-Agent'] = random_ua()

    if config_dict[GB_RANDOM_XFF]:
        tmp = config_dict[GB_RANDOM_XFF]
        update_headers['X-Forwarded-For'] = tmp if isinstance(tmp, str) else random_xff()

    if update_headers:
        # setdefault方法可用于设置字典中的键值对，如果键不存在，则添加该键。以下是一个简化的示例：
        config_dict.setdefault(GB_REQ_HEADERS, {}).update(update_headers)
        update_dict.setdefault(GB_REQ_HEADERS, {}).update(update_headers)
    return update_dict


def options_to_argument(args_options, argument_parser, config_dict, param_dict):
    """
    将参数字典转换为参数选项
    :param args_options:
    :param argument_parser:
    :param config_dict:
    :param param_dict: 全局变量<-->短参数对应关系字典
    :return:
    """
    support_list = ["param", "dest", "name", "default", "nargs", "action", "choices", "type", "help"]
    for option in args_options:
        # 跳过空字典
        if not option:
            continue

        try:
            # 使用 issubset() 方法判断字典的所有键是否都是列表 support_list 的子集
            if not set(option.keys()).issubset(support_list):
                not_allowed_keys = set(option.keys()) - set(support_list)
                output(f"[!] 参数选项:[{option}]存在非预期参数[{not_allowed_keys}]!!!", level=LOG_ERROR)
            else:
                gb_param = option["param"]
                tmp_dest = vars_to_param(gb_param) if "dest" not in option.keys() else option["dest"]
                tmp_name = extract_heads(tmp_dest, param_dict) if "name" not in option.keys() else option["name"]
                tmp_default = config_dict[gb_param] if "default" not in option.keys() else option["default"]
                tmp_nargs = None if "nargs" not in option.keys() else option["nargs"]
                tmp_action = None if "action" not in option.keys() else option["action"]
                tmp_help = f"Specify the {vars_to_param(gb_param)}" if "help" not in option.keys() else option["help"]
                tmp_type = None if "type" not in option.keys() else option["type"]
                tmp_choices = None if "choices" not in option.keys() else option["choices"]

                # 存储长短参数对应关系
                param_dict[gb_param] = tmp_name

                if tmp_action:
                    argument_parser.add_argument(f"-{tmp_name.strip('-')}",
                                                 f"--{tmp_dest.strip('-')}",
                                                 default=tmp_default,
                                                 action=tmp_action,
                                                 # type=tmp_type,  # type 互斥 action
                                                 # nargs=tmp_nargs,  # type 互斥 action
                                                 # choices=tmp_choices,
                                                 help=f"{tmp_help}. Default Is [{tmp_default}]. Action Is {tmp_action}.",
                                                 )
                else:
                    # 当设置nargs参数时, 不能设置action, 需要分别设置
                    argument_parser.add_argument(f"-{tmp_name.strip('-')}",
                                                 f"--{tmp_dest.strip('-')}",
                                                 default=tmp_default,
                                                 nargs=tmp_nargs,
                                                 type=tmp_type,
                                                 choices=tmp_choices,
                                                 help=f"{tmp_help}. Default Is [{tmp_default}].",
                                                 )
        except Exception as error:
            output(f"[!] 参数选项 {option} 解析发生错误, ERROR:{error}", level=LOG_ERROR)
            exit()


def vars_to_param(var_name):
    # 实现全局变量到参数名的自动转换,和 config_dict_add_args中的修改过程相反
    # 基于变量的值实现，要求 变量="变量", 如:GB_PROXIES="GB_PROXIES"
    # param_name = str(var_name).replace("GB_", "").lower()
    # 基于变量名的更通用的实现, 要求变量是全局变量.
    param_name = str(globals()[var_name]).replace("GB_", "").lower()
    return param_name



