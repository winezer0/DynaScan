# 解析输入参数
import argparse
from pyfiglet import Figlet
from libs.lib_file_operate.file_path import get_sub_dirs
from libs.lib_log_print.logger_printer import output, LOG_ERROR, LOG_INFO
from libs.input_const import *
from libs.lib_requests.requests_const import HTTP_USER_AGENTS
from libs.lib_requests.requests_tools import random_useragent, random_x_forwarded_for


def parse_input(config_dict):
    # RawDescriptionHelpFormatter 支持输出换行符
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)

    # description 程序描述信息
    argument_parser.description = Figlet().renderText("DynaScan")
    # 指定扫描URL或文件
    argument_parser.add_argument("-u",
                                 f"--{vars_param_name(GB_TARGET)}",
                                 default=config_dict[GB_TARGET],
                                 nargs="+",
                                 help=f"Specify the target URLs or Target File, "
                                      f"Default is [{config_dict[GB_TARGET]}]",
                                 )

    # 指定调用的字典目录
    argument_parser.add_argument("-r",
                                 f"--{vars_param_name(GB_DICT_RULE_SCAN)}",
                                 default=config_dict[GB_DICT_RULE_SCAN],
                                 nargs="+",
                                 choices=get_sub_dirs(config_dict[GB_DICT_RULE_PATH]),
                                 help=f"Specifies Scan the rule dirs list, "
                                      f"Default is [{config_dict[GB_DICT_RULE_SCAN]}], "
                                      f"Support Choices [{get_sub_dirs(config_dict[GB_DICT_RULE_PATH])}]",
                                 )
    # 指定最小提取频率
    argument_parser.add_argument("-f",
                                 f"--{vars_param_name(GB_FREQUENCY_MIN)}",
                                 default=config_dict[GB_FREQUENCY_MIN],
                                 type=int,
                                 help=f"Specifies the pair rule file level or prefix, "
                                      f"Default is [{config_dict[GB_FREQUENCY_MIN]}]",
                                 )
    # 指定频率分割符号
    argument_parser.add_argument("-fs",
                                 f"--{vars_param_name(GB_FREQUENCY_SYMBOL)}",
                                 default=config_dict[GB_FREQUENCY_SYMBOL],
                                 help=f"Specifies Name Pass Link Symbol in history file, "
                                      f"Default is [{config_dict[GB_FREQUENCY_SYMBOL]}]",
                                 )
    # 指定请求代理服务
    argument_parser.add_argument("-x",
                                 f"--{vars_param_name(GB_PROXIES)}",
                                 default=config_dict[GB_PROXIES],
                                 help=f"Specifies http|https|socks5 proxies, "
                                      f"Default is [{config_dict[GB_PROXIES]}]",
                                 )
    # 指定请求线程数量
    argument_parser.add_argument("-t",
                                 f"--{vars_param_name(GB_THREADS_COUNT)}",
                                 default=config_dict[GB_THREADS_COUNT],
                                 type=int,
                                 help=f"Specifies request threads, "
                                      f"Default is [{config_dict[GB_THREADS_COUNT]}]",
                                 )
    # 开启调试功能
    argument_parser.add_argument("-d",
                                 f"--{vars_param_name(GB_DEBUG_FLAG)}",
                                 default=config_dict[GB_DEBUG_FLAG],
                                 action="store_true",
                                 help=f"Specifies Display Debug Info, "
                                      f"Default is [{config_dict[GB_DEBUG_FLAG]}]",
                                 )

    # 开启随机UA
    argument_parser.add_argument("-ru",
                                 f"--{vars_param_name(GB_RANDOM_REQ_UA)}",
                                 default=config_dict[GB_RANDOM_REQ_UA],
                                 action="store_true",
                                 help=f"Specifies Start Random useragent, "
                                      f"Default is [{config_dict[GB_RANDOM_REQ_UA]}]",
                                 )
    # 开启随机XFF
    argument_parser.add_argument("-rx",
                                 f"--{vars_param_name(GB_RANDOM_REQ_XFF)}",
                                 default=config_dict[GB_RANDOM_REQ_XFF],
                                 action="store_true",
                                 help=f"Specifies Start Random XFF Header, "
                                      f"Default is [{config_dict[GB_RANDOM_REQ_XFF]}]",
                                 )
    # 关闭流模式扫描
    argument_parser.add_argument("-ss",
                                 f"--{vars_param_name(GB_STREAM_MODE)}",
                                 default=config_dict[GB_STREAM_MODE],
                                 action="store_false",
                                 help=f"Shutdown Request Stream Mode, "
                                      f"Default is [{config_dict[GB_STREAM_MODE]}]",
                                 )
    # 关闭历史扫描URL过滤
    argument_parser.add_argument("-se",
                                 f"--{vars_param_name(GB_EXCLUDE_HISTORY)}",
                                 default=config_dict[GB_EXCLUDE_HISTORY],
                                 action="store_false",
                                 help=f"Shutdown Exclude Request History, "
                                      f"Default is [{config_dict[GB_EXCLUDE_HISTORY]}]",
                                 )
    # 手动指定排除扫描的URLs文件
    argument_parser.add_argument("-eu",
                                 f"--{vars_param_name(GB_EXCLUDE_URLS)}",
                                 default=config_dict[GB_EXCLUDE_URLS],
                                 help=f"Specify the Exclude Custom URLs File, "
                                      f"Default is [{config_dict[GB_EXCLUDE_URLS]}]",
                                 )
    # 关闭 URL目标可访问性判断
    argument_parser.add_argument("-ua",
                                 f"--{vars_param_name(GB_URL_ACCESS_TEST)}",
                                 default=config_dict[GB_URL_ACCESS_TEST],
                                 action="store_false",
                                 help=f"Shutdown URL Access Test, "
                                      f"Default is [{config_dict[GB_URL_ACCESS_TEST]}]",
                                 )
    # 开启 目标URL拆分
    argument_parser.add_argument("-sp",
                                 f"--{vars_param_name(GB_SPLIT_TARGET_PATH)}",
                                 default=config_dict[GB_SPLIT_TARGET_PATH],
                                 action="store_true",
                                 help=f"Start Split Target Path, "
                                      f"Default is [{config_dict[GB_SPLIT_TARGET_PATH]}]",
                                 )
    # 排除匹配指定的状态码的响应结果
    argument_parser.add_argument("-es",
                                 f"--{vars_param_name(GB_EXCLUDE_STATUS)}",
                                 default=config_dict[GB_EXCLUDE_STATUS],
                                 nargs='+',
                                 type=int,
                                 help=f"Specified Response Status List Which Exclude, "
                                      f"Default is {config_dict[GB_EXCLUDE_STATUS]}",
                                 )
    # 排除匹配指定正则的响应结果
    argument_parser.add_argument("-er",
                                 f"--{vars_param_name(GB_EXCLUDE_REGEXP)}",
                                 default=config_dict[GB_EXCLUDE_REGEXP],
                                 help=f"Specified RE String When response matches the Str Excluded, "
                                      f"Default is [{config_dict[GB_EXCLUDE_REGEXP]}]",
                                 )

    # 指定字典后缀名列表
    argument_parser.add_argument("-ds",
                                 f"--{vars_param_name(GB_DICT_SUFFIX)}",
                                 default=config_dict[GB_DICT_SUFFIX],
                                 nargs='+',
                                 help=f"Specifies Dict File Suffix List, "
                                      f"Default is [{config_dict[GB_DICT_SUFFIX]}]",
                                 )
    # 指定保留指定后缀的文件
    argument_parser.add_argument("-so",
                                 f"--{vars_param_name(GB_ONLY_SCAN_SPECIFY_EXT)}",
                                 default=config_dict[GB_ONLY_SCAN_SPECIFY_EXT],
                                 nargs='+',
                                 help=f"Only Scan Specifies Suffix List Url, "
                                      f"Default is [{config_dict[GB_ONLY_SCAN_SPECIFY_EXT]}]",
                                 )
    # 指定排除指定后缀的文件
    argument_parser.add_argument("-sn",
                                 f"--{vars_param_name(GB_NO_SCAN_SPECIFY_EXT)}",
                                 default=config_dict[GB_NO_SCAN_SPECIFY_EXT],
                                 nargs='+',
                                 help=f"No Scan Specifies Suffix List Url, "
                                      f"Default is [{config_dict[GB_NO_SCAN_SPECIFY_EXT]}]",
                                 )
    # 为生成的每条字典添加特定前缀
    argument_parser.add_argument("-cp",
                                 f"--{vars_param_name(GB_CUSTOM_URL_PREFIX)}",
                                 default=config_dict[GB_CUSTOM_URL_PREFIX],
                                 nargs='+',
                                 help=f"Add Custom Prefix List for Each Path, "
                                      f"Default is [{config_dict[GB_CUSTOM_URL_PREFIX]}]",
                                 )
    # 去除以特定字符结尾的URL
    argument_parser.add_argument("-rs",
                                 f"--{vars_param_name(GB_REMOVE_END_SYMBOLS)}",
                                 default=config_dict[GB_REMOVE_END_SYMBOLS],
                                 nargs='+',
                                 help=f"Remove Url When Url endswith the Char List, "
                                      f"Default is [{config_dict[GB_REMOVE_END_SYMBOLS]}]",
                                 )
    # 指定默认请求方法
    argument_parser.add_argument("-rm",
                                 f"--{vars_param_name(GB_REQ_METHOD)}",
                                 default=config_dict[GB_REQ_METHOD],
                                 help=f"Specifies request method, "
                                      f"Default is [{config_dict[GB_REQ_METHOD]}]",
                                 )
    # 指定请求超时时间
    argument_parser.add_argument("-tt",
                                 f"--{vars_param_name(GB_TIMEOUT)}",
                                 default=config_dict[GB_TIMEOUT], type=int,
                                 help=f"Specifies request timeout, "
                                      f"Default is [{config_dict[GB_TIMEOUT]}]",
                                 )
    # 指定自动错误重试次数
    argument_parser.add_argument("-rt",
                                 f"--{vars_param_name(GB_RETRY_TIMES)}",
                                 default=config_dict[GB_RETRY_TIMES],
                                 type=int,
                                 help=f"Specifies request retry times, "
                                      f"Default is [{config_dict[GB_RETRY_TIMES]}]",
                                 )

    example = """Examples:
             \r  批量扫描 target.txt
             \r  python3 {shell_name} -u target.txt
             \r  指定扫描 baidu.com
             \r  python3 {shell_name} -u https://www.baidu.com
             \r  进行备份文件字典扫描,筛选频率10以上的字典:
             \r  python3 {shell_name} -u https://www.xxx.com -r backup -f 10
             \r  进行Spring Boot文件字典扫描,筛选频率1以上的字典:
             \r  python3 {shell_name} -u https://www.xxx.com -r backup -f 1
             \r  进行所有文件字典扫描,设置Socks5请求代理:
             \r  python3 {shell_name} -u https://www.baidu.com -p socks5://127.0.0.1:1080
             \r    
             \r  其他控制细节参数可通过setting.py进行配置
             \r  
             \r  T00L Version: {version}
             \r  """

    argument_parser.epilog = example.format(shell_name=argument_parser.prog, version=config_dict[GB_VERSION])
    args = argument_parser.parse_args()
    return args


def args_dict_handle(args):
    # # 格式化输入的Proxy参数 如果输入了代理参数就会变为字符串
    if args.proxies and isinstance(args.proxies, str):
        if "socks" in args.proxies or "http" in args.proxies:
            args.proxies = {'http': args.proxies.replace('https://', 'http://'),
                            'https': args.proxies.replace('https://', 'http://')}
        else:
            output(f"[!] 输入的代理地址[{args.proxies}]不正确,正确格式:Proto://IP:PORT", level=LOG_ERROR)
    return args


def vars_param_name(var_name):
    # 实现全局变量到参数名的自动转换,和 config_dict_add_args中的修改过程相反
    # 基于变量的值实现，要求 变量="变量", 如:GB_PROXIES="GB_PROXIES"
    # param_name = str(var_name).replace("GB_", "").lower()
    # 基于变量名的更通用的实现, 要求变量是全局变量.
    param_name = str(globals()[var_name]).replace("GB_", "").lower()
    return param_name


def config_dict_add_args(config_dict, args):
    # 使用字典解压将参数 直接赋值给相应的全局变量
    # 要求args参数命名要和字典的键 统一（完全相同或可以变为完全相同）
    for param_name, param_value in vars(args).items():
        var_name = f"GB_{param_name.upper()}"
        try:
            # globals()[var_name] = param_value # 赋值全局变量,仅本文件可用
            # output(f"[*] INPUT:{var_name} -> {param_value}", level=LOG_ERROR)
            config_dict[var_name] = param_value  # 赋值全局字典,所有文件可用
            if var_name not in config_dict.keys():
                output(f"[-] 非预期参数将被赋值: {var_name} <--> {param_value}", level=LOG_ERROR)
        except Exception as error:
            output(f"[!] 更新参数发生错误: {error}", level=LOG_ERROR)
            exit()
    return


def config_dict_handle(config_dict):
    # 格式化输入的规则目录
    if not config_dict[GB_DICT_RULE_SCAN]:
        config_dict[GB_DICT_RULE_SCAN] = get_sub_dirs(config_dict[GB_DICT_RULE_PATH])
        # output(f"[*] 未指定扫描规则,默认扫描所有规则{args.dict_rule_scan}", level=LOG_ERROR)

    # HTTP 头设置
    config_dict[GB_REQ_HEADERS] = {
        'User-Agent': random_useragent(HTTP_USER_AGENTS, config_dict[GB_RANDOM_REQ_UA]),
        'X_FORWARDED_FOR': random_x_forwarded_for(config_dict[GB_RANDOM_REQ_XFF]),
        'Accept-Encoding': ''
    }
    return config_dict


def show_config_dict(config_dict):
    # 输出 config 字典
    for index, param_name in enumerate(config_dict.keys()):
        param_val = config_dict[param_name]
        output(f"[*] Param_{index} {param_name} <--> {param_val}", level=LOG_INFO)

