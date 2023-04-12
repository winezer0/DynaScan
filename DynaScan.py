#!/usr/bin/env python
# encoding: utf-8
import argparse

from pyfiglet import Figlet

from libs.gen_path import gen_base_scan_path_list, product_urls_and_paths, path_list_handle, target_url_handle, \
    url_list_handle
from libs.lib_log_print.logger_printer import set_logger, output
from libs.lib_requests.check_protocol import check_proto_and_access
from libs.lib_requests.requests_const import *
from libs.lib_requests.requests_thread import multi_thread_requests_url, multi_thread_requests_url_sign
from libs.lib_requests.requests_tools import get_random_str, analysis_dict_same_keys, access_result_handle
from libs.lib_rule_dict.base_key_replace import replace_list_has_key_str
from libs.lib_rule_dict.util_depend_var import set_dependent_var_dict
from libs.lib_url_analysis.url_tools import get_host_port, get_base_url
from libs.util_file import read_file_to_list, file_encoding, write_lines
from libs.util_file import write_hit_result_to_frequency_file
from libs.util_func import url_to_raw_rule_classify
from setting import *  # setting.py中的变量

sys.dont_write_bytecode = True  # 设置不生成pyc文件


# 解析输入参数
def parse_input():
    # RawDescriptionHelpFormatter 支持输出换行符
    argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=True)

    # description 程序描述信息
    argument_parser.description = Figlet().renderText("DynaScan")

    argument_parser.add_argument("-u", "--target", default=GB_TARGET,
                                 help=f"Specify the target URL or target File, Default is [{GB_TARGET}]")

    argument_parser.add_argument("-x", dest="proxies", default=GB_PROXIES,
                                 help=f"Specifies http|https|socks5 proxies, Default is [{GB_PROXIES}]")

    argument_parser.add_argument("-t", "--threads_count", default=GB_THREADS_COUNT, type=int,
                                 help=f"Specifies request threads, Default is [{GB_THREADS_COUNT}]")

    argument_parser.add_argument("-s", dest="dict_suffix", default=GB_DICT_SUFFIX, nargs='+',
                                 help=f"Specifies Dict File Suffix List, Default is [{GB_DICT_SUFFIX}]")

    argument_parser.add_argument("-d", "--debug_flag", default=GB_DEBUG_FLAG, action="store_true",
                                 help=f"Specifies Display Debug Info, Default is [{GB_DEBUG_FLAG}]", )

    example = """
             \rExamples:
             \r  python3 {shell_name} -u target.txt
             \r  python3 {shell_name} -u https://www.baidu.com
             \r  python3 {shell_name} -u https://www.baidu.com -t 100
             \r  python3 {shell_name} -u https://www.baidu.com -s txt lst 
             \r  python3 {shell_name} -u https://www.baidu.com -p socks5://127.0.0.1:1080
             \r    
             \r  其他控制细节参数请通过setting.py进行配置
             \r    
             \r  T00L Version: {version}
             \r  """

    argument_parser.epilog = example.format(shell_name=argument_parser.prog, version=GB_VERSION)

    return argument_parser


# 生成动态排除字典
def gen_dynamic_exclude_dict(req_url):
    test_path_1 = get_random_str(length=8, has_symbols=False, has_dot=True, with_slash=True)

    test_path_2 = get_random_str(length=9, has_symbols=False, has_dot=False, with_slash=True)
    test_path_2 += get_random_str(length=10, has_symbols=False, has_dot=True, with_slash=True)

    test_path_3 = get_random_str(length=11, has_symbols=False, has_dot=False, with_slash=True)
    test_path_3 += get_random_str(length=12, has_symbols=False, has_dot=False, with_slash=True)
    test_path_3 += get_random_str(length=13, has_symbols=False, has_dot=True, with_slash=True)

    test_path_list = [test_path_1, test_path_2, test_path_3]

    # 组合URL和测试路径
    test_url_path_list = product_urls_and_paths([get_base_url(req_url)], test_path_list)

    # 执行测试任务
    output(f"[+] 随机访问测试 {test_url_path_list}", level="info")
    test_result_dict_list = multi_thread_requests_url(task_list=test_url_path_list,
                                                      threads_count=min(len(test_url_path_list), 30),
                                                      thread_sleep=GB_THREAD_SLEEP,
                                                      req_method=GB_REQ_METHOD,
                                                      req_headers=GB_HEADERS,
                                                      req_data=GB_REQ_BODY,
                                                      req_proxies=GB_PROXIES,
                                                      req_timeout=GB_TIMEOUT,
                                                      verify_ssl=GB_SSL_VERIFY,
                                                      req_allow_redirects=GB_ALLOW_REDIRECTS,
                                                      req_stream=GB_STREAM_MODE,
                                                      retry_times=GB_RETRY_TIMES,
                                                      const_sign=None,
                                                      add_host_header=GB_ADD_DYNAMIC_HOST,
                                                      add_refer_header=GB_ADD_DYNAMIC_REFER,
                                                      ignore_encode_error=GB_CHINESE_ENCODE
                                                      )

    output(f"随机测试响应 {test_result_dict_list}", level="debug")

    # 分析测试结果
    dynamic_exclude_dict = analysis_dict_same_keys(test_result_dict_list, FILTER_MODULE_DEFAULT_VALUE_DICT)
    output(f"[+] 动态排除字典 {req_url} -> {dynamic_exclude_dict}", level="info")
    return dynamic_exclude_dict


# 扫描主体
def dyna_scan():
    # 读取用户输入的URL和目标文件参数
    target_list = []
    if os.path.isfile(GB_TARGET):
        target_list = read_file_to_list(file_path=GB_TARGET,
                                        encoding=file_encoding(GB_TARGET),
                                        de_strip=True,
                                        de_weight=True,
                                        de_unprintable=True)
    else:
        target_list.append(GB_TARGET)

    # 尝试对输入的目标进行初次过滤、添加协议头、访问测试等处理
    accessible_target, inaccessible_target = check_proto_and_access(target_list=target_list,
                                                                    thread_sleep=GB_THREAD_SLEEP,
                                                                    default_proto_head=GB_DEFAULT_PROTO_HEAD,
                                                                    url_access_test=GB_URL_ACCESS_TEST,
                                                                    req_path="/",
                                                                    req_method=GB_REQ_METHOD,
                                                                    req_headers=GB_HEADERS,
                                                                    req_proxies=GB_PROXIES,
                                                                    verify_ssl=GB_SSL_VERIFY,
                                                                    req_timeout=GB_TIMEOUT,
                                                                    req_allow_redirects=GB_ALLOW_REDIRECTS,
                                                                    retry_times=GB_RETRY_TIMES
                                                                    )

    # 记录可以访问的目标到文件
    write_lines(GB_ACCESSIBLE_RECORD, accessible_target, encoding="utf-8", new_line=True, mode="a+")
    # 记录不可访问的目标到文件
    write_lines(GB_INACCESSIBLE_RECORD, inaccessible_target, encoding="utf-8", new_line=True, mode="a+")

    target_list = list(set(accessible_target))

    output(f"[*] 当前整合URL 剩余目标 {len(target_list)}个", level="info")

    # 对输入的目标数量进行判断和处理
    if not target_list:
        output("[-] 未输入任何有效目标,退出程序...", level="error")
        return

    # 读取路径字典 进行频率筛选、规则渲染、基本变量替换
    output("[*] 读取路径字典 进行频率筛选、规则渲染、基本变量替换", level="info")
    base_scan_path_list = gen_base_scan_path_list()

    # 对路径字典进行过滤和格式化
    base_scan_path_list = path_list_handle(base_scan_path_list)
    output(f"[*] 字典处理完毕 剩余元素 {len(base_scan_path_list)}", level="info")

    # 对每个目标进行分析因变量分析和因变量替换渲染
    for target_index, target_url in enumerate(target_list):
        output(f"[+] 任务进度 {target_index + 1}/{len(target_list)} {target_url}", level="info")

        # 开始进行URL测试,确定动态排除用的变量
        curr_dynamic_exclude_dict = gen_dynamic_exclude_dict(target_url)

        # 扩展输入的URL列表
        current_url_list = target_url_handle(target_url)

        # 处理目标URL格式,最后的一个/不需要
        current_url_list = list(set([url[:-1] if url.endswith('/') else url for url in current_url_list]))

        # 合并urls列表和paths列表
        current_url_list = product_urls_and_paths(current_url_list, base_scan_path_list)
        output(f"[*] 合并urls列表和paths列表 {len(current_url_list)}个", level="info")

        # 基于URL解析因变量并进行替换
        current_dependent_dict = set_dependent_var_dict(target_url=target_url,
                                                        base_dependent_dict=GB_DEPENDENT_VAR_REPLACE_DICT,
                                                        ignore_ip_format=GB_IGNORE_IP_FORMAT,
                                                        symbol_replace_dict=GB_SYMBOL_REPLACE_DICT,
                                                        not_allowed_symbol=GB_NOT_ALLOW_SYMBOL)
        output(f"[*] 因变量字典 {current_dependent_dict}", level="info")
        # 进行因变量替换
        current_url_list, replace_count_, running_time = replace_list_has_key_str(will_replace_list=current_url_list,
                                                                                  replace_used_dict_=current_dependent_dict,
                                                                                  remove_not_render_str=True,
                                                                                  keep_no_repl_key_str=True)
        output(f"[*] 因变量替换 {len(current_url_list)}个", level="info")

        # 历史记录文件路径 基于主机HOST动态生成
        curr_host_port_no_symbol = get_host_port(target_url, replace_symbol=True)
        curr_host_history_file = GB_PER_HOST_HISTORY_FILE.format(host_port=curr_host_port_no_symbol)

        # 格式化和过滤当前的 current_url_list
        current_url_list = url_list_handle(current_url_list, curr_host_history_file)
        output(f"[*] 当前目标 {target_url} 所有URL访问开始进行...", level="info")

        # 组合爆破任务
        brute_task_list = [(url, url) for url in current_url_list]

        # 将任务列表拆分为多个任务列表 再逐步进行爆破,便于统一处理结果
        task_size = GB_THREADS_COUNT
        brute_task_list = [brute_task_list[i:i + task_size] for i in range(0, len(brute_task_list), task_size)]
        output(f"[*] 任务拆分 SIZE:[{task_size}] * NUM:[{len(brute_task_list)}]", level="info")

        # 直接被排除的请求记录
        ignore_file_path = os.path.join(GB_RESULT_DIR, f"{curr_host_port_no_symbol}.ignore.csv")
        # 构造常规的结果文件
        result_file_path = GB_RESULT_FILE_PATH
        if "auto" in result_file_path.lower():
            # 根据主机名生成结果文件名
            result_file_path = os.path.join(GB_RESULT_DIR, f"{curr_host_port_no_symbol}.result.csv")

        # 统计本目标的总访问错误次数
        access_fail_count = 0
        # 循环多线程请求操作
        for sub_task_index, sub_task_list in enumerate(brute_task_list):
            output(f"[*] 任务进度 {sub_task_index + 1}/{len(brute_task_list)}", level="info")
            result_dict_list = multi_thread_requests_url_sign(task_list=sub_task_list,
                                                              threads_count=GB_THREADS_COUNT,
                                                              thread_sleep=GB_THREAD_SLEEP,
                                                              req_method=GB_REQ_METHOD,
                                                              req_headers=GB_HEADERS,
                                                              req_data=GB_REQ_BODY,
                                                              req_proxies=GB_PROXIES,
                                                              req_timeout=GB_TIMEOUT,
                                                              verify_ssl=GB_SSL_VERIFY,
                                                              req_allow_redirects=GB_ALLOW_REDIRECTS,
                                                              req_stream=GB_STREAM_MODE,
                                                              retry_times=GB_RETRY_TIMES,
                                                              add_host_header=GB_ADD_DYNAMIC_HOST,
                                                              add_refer_header=GB_ADD_DYNAMIC_REFER,
                                                              ignore_encode_error=GB_CHINESE_ENCODE
                                                              )

            # 处理响应结果
            stop_run, HIT_URL_LIST = access_result_handle(result_dict_list=result_dict_list,
                                                          dynamic_exclude_dict=curr_dynamic_exclude_dict,
                                                          ignore_file=ignore_file_path,
                                                          result_file=result_file_path,
                                                          history_file=curr_host_history_file,
                                                          access_fail_count=access_fail_count,
                                                          exclude_status_list=GB_EXCLUDE_STATUS,
                                                          exclude_title_regexp=GB_EXCLUDE_REGEXP,
                                                          max_error_num=GB_MAX_ERROR_NUM,
                                                          hit_saving_field=CONST_SIGN
                                                          )

            # 写入命中结果
            if SAVE_HIT_RESULT and HIT_URL_LIST:
                print(f"HIT_URL_LIST:{HIT_URL_LIST}")
                hit_classify_dict = url_to_raw_rule_classify(hit_url_list=HIT_URL_LIST,
                                                             reverse_replace_dict_list=[current_dependent_dict],
                                                             hit_ext_file=GB_HIT_EXT_FILE,
                                                             hit_direct_file=GB_HIT_DIRECT_FILE,
                                                             hit_folder_file=GB_HIT_FOLDER_FILE,
                                                             hit_files_file=GB_HIT_FILES_FILE
                                                             )
                for file_name, path_list in hit_classify_dict.items():
                    write_hit_result_to_frequency_file(file_name=file_name,
                                                       path_list=path_list,
                                                       encoding='utf-8',
                                                       frequency_symbol=GB_FREQUENCY_SYMBOL,
                                                       annotation_symbol=GB_ANNOTATION_SYMBOL,
                                                       hit_over_write=GB_HIT_OVER_CALC)

            # 停止扫描任务
            if stop_run:
                output(f"[-] 错误次数超过阈值,停止扫描目标 {target_url}", level="info")
                break

        output(f"[+] 测试完毕 [{target_url}]", level="info")


if __name__ == "__main__":
    # 输入参数解析
    parser = parse_input()

    # 输出所有参数
    args = parser.parse_args()
    output(f"[*] 所有输入参数信息: {args}")
    time.sleep(0.1)

    # 使用字典解压将参数直接赋值给相应的全局变量
    for param_name, param_value in vars(args).items():
        globals_var_name = f"GB_{param_name.upper()}"
        try:
            globals()[globals_var_name] = param_value
            # output(f"[*] INPUT:{globals_var_name} -> {param_value}", level="debug")
        except Exception as error:
            output(f"[!] 输入参数信息: {param_name} {param_value} 未对应其全局变量!!!", level="error")
            exit()

    # 处理代理参数 如果输入了代理参数就会变为字符串
    if GB_PROXIES and isinstance(GB_PROXIES, str):
        if "socks" in GB_PROXIES or "http" in GB_PROXIES:
            GB_PROXIES = {'http': GB_PROXIES.replace('https://', 'http://'),
                          'https': GB_PROXIES.replace('http://', 'https://')}
        else:
            output(f"[!] 输入的代理地址[{GB_PROXIES}]不正确,正确格式:Protocol://IP:PORT", level="error")

    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    set_logger(GB_INFO_LOG_FILE, GB_ERR_LOG_FILE, GB_DBG_LOG_FILE, GB_DEBUG_FLAG)

    # 开始扫描
    dyna_scan()

    output(f"[+] 所有任务测试完毕", level="info")
