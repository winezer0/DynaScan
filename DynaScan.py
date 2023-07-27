#!/usr/bin/env python
# encoding: utf-8
import os

import setting_com
import setting_dict
import setting_http
from libs.lib_dyna_rule.base_key_replace import replace_list_has_key_str
from libs.lib_dyna_rule.set_basic_var import set_base_var_dict_with_freq
from libs.lib_dyna_rule.set_depend_var import set_dependent_var_dict
from libs.lib_file_operate.rw_json_file import load_json_to_dict, dump_dict_to_json
from libs.lib_requests.requests_const import FILTER_HTTP_VALUE_DICT, FILTER_DYNA_IGNORE_KEYS, HTTP_CONST_SIGN
from libs.lib_requests.requests_thread import multi_thread_requests
from libs.lib_requests.requests_utils import random_str, analysis_dict_same_keys, access_result_handle
from libs.lib_url_analysis.parse_path import get_curr_dir_url
from libs.lib_url_analysis.url_utils import combine_urls_and_paths, get_segment_urls
from libs.lib_url_analysis.parse_host import get_proto, get_host_port
from libs.path_handle import url_and_paths_dict_handle
from libs.lib_attribdict.config import CONFIG
from libs.lib_file_operate.file_utils import auto_make_dir, file_is_exist, exclude_history_files, file_is_empty
from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_write import write_lines
from libs.lib_file_operate.rw_freq_file import write_list_to_freq_file
from libs.lib_log_print.logger_printer import output, LOG_INFO, set_logger, LOG_ERROR, LOG_DEBUG
from libs.lib_args.input_const import *
from libs.lib_requests.check_protocol import check_host_list_proto, check_url_list_access
from libs.lib_args.input_parse import args_parser, args_dict_handle, config_dict_handle
from libs.lib_args.input_basic import config_dict_add_args
from libs.utils import analysis_ends_url, url_to_raw_rule_classify, read_dir_and_parse_rule_with_freq, \
    combine_urls_and_path_dict


# 读取用户输入的URL和目标文件参数
def init_target(config_dict):
    # 读取用户输入的URL和目标文件参数
    input_target = config_dict[GB_TARGET]
    if isinstance(input_target, str):
        input_target = [input_target]

    targets = []
    if isinstance(input_target, list):
        for target in input_target:
            if file_is_exist(target):
                lists = read_file_to_list(file_path=target, de_strip=True, de_weight=True, de_unprintable=True)
                targets.extend(lists)
            else:
                if not target.startswith(("http://", "https://")) and any(c in target for c in ['\\', '/', '.txt']):
                    # 字符串既不以 "http://" 或 "https://" 开头，且包含 '\'、'/' 或以 ".txt" 结尾
                    # 表示该字符串符合 Windows 或 Linux 的路径格式
                    output(f"[!] 目标文件路径不存在 {target}", level=LOG_ERROR)
                    exit()
                else:
                    targets.append(target)
    # 去重输入目标
    targets = list(dict.fromkeys(targets))

    # 尝试对输入的目标进行HOST头添加
    targets = check_host_list_proto(target_list=targets,
                                    req_method=config_dict[GB_REQ_METHOD],
                                    req_path="/",
                                    req_headers=config_dict[GB_REQ_HEADERS],
                                    req_proxies=config_dict[GB_PROXIES],
                                    req_timeout=config_dict[GB_TIME_OUT],
                                    verify_ssl=config_dict[GB_SSL_VERIFY],
                                    default_proto=config_dict[GB_DEFAULT_PROTO])

    # 尝试对输入的目标访问测试等处理
    if config_dict[GB_URL_ACCESS_TEST]:
        accessible_target, inaccessible_target = check_url_list_access(
            target_list=targets,
            thread_sleep=config_dict[GB_THREAD_SLEEP],
            req_method=config_dict[GB_REQ_METHOD],
            req_headers=config_dict[GB_REQ_HEADERS],
            req_proxies=config_dict[GB_PROXIES],
            verify_ssl=config_dict[GB_SSL_VERIFY],
            req_timeout=config_dict[GB_TIME_OUT],
            req_allow_redirects=config_dict[GB_ALLOW_REDIRECTS],
            retry_times=config_dict[GB_RETRY_TIMES])
        # 记录可以访问的目标到文件
        write_lines(config_dict[GB_ACCESS_OK_FILE], accessible_target, encoding="utf-8", new_line=True, mode="a+")
        # 记录不可访问的目标到文件
        write_lines(config_dict[GB_ACCESS_NO_FILE], inaccessible_target, encoding="utf-8", new_line=True, mode="a+")
        # 需要扫描的目标列表
        targets = list(set(accessible_target))

    output(f"[*] 当前整合URL 剩余目标 {len(targets)}个", level=LOG_INFO)
    return targets


# 生成基本扫描字典
def init_load_dict(config_dict):
    cur_rule_dir_list = config_dict[GB_DICT_RULE_SCAN]
    output(f"[*] 当前指定加载目录:{cur_rule_dir_list}", level=LOG_DEBUG)

    # # 1、获取所有的基本变量替换字典
    # base_replace_dict = set_base_var_dict_with_freq(
    #     base_var_dir=config_dict[GB_BASE_VAR_DIR],
    #     ext_list=config_dict[GB_DICT_SUFFIX],
    #     base_replace_dict=config_dict[GB_BASE_REPLACE_DICT],
    #     freq_symbol=config_dict[GB_FREQUENCY_SYMBOL],
    #     anno_symbol=config_dict[GB_ANNOTATION_SYMBOL],
    #     freq_min=config_dict[GB_FREQUENCY_MIN]
    # )
    # output(f"[*] 获取基本变量完成:{base_replace_dict.keys()}", level=LOG_DEBUG)

    # 读取扫描字典
    bse_path_dict = {
        STR_BASE_PATH: [],
        STR_BASE_ROOT: [],
    }

    # 循环读取每个文件夹下的规则字典
    for rule_dir in cur_rule_dir_list:
        # 1、获取基本变量替换字典 # 只获取目标文件下的依赖
        base_replace_dict = set_base_var_dict_with_freq(
            base_var_dir=config_dict[GB_BASE_VAR_DIR].joinpath(rule_dir),
            ext_list=config_dict[GB_DICT_SUFFIX],
            base_replace_dict=config_dict[GB_BASE_REPLACE_DICT],
            freq_symbol=config_dict[GB_FREQUENCY_SYMBOL],
            anno_symbol=config_dict[GB_ANNOTATION_SYMBOL],
            freq_min=config_dict[GB_FREQUENCY_MIN]
        )
        output(f"[*] 获取[{rule_dir}]目录基本变量完成:{base_replace_dict.keys()}", level=LOG_INFO)

        base_path_path = config_dict[GB_BASE_PATH_STR].format(RULE_DIR=rule_dir)
        base_root_path = config_dict[GB_BASE_ROOT_STR].format(RULE_DIR=rule_dir)

        # 2、读取直接追加到当前目录的字典
        if config_dict[GB_SCAN_BASE_PATH]:
            base_path_dict_list = read_dir_and_parse_rule_with_freq(
                read_dir_path=base_path_path,
                ext_list=config_dict[GB_DICT_SUFFIX],
                freq_symbol=config_dict[GB_FREQUENCY_SYMBOL],
                anno_symbol=config_dict[GB_ANNOTATION_SYMBOL],
                freq_min=config_dict[GB_FREQUENCY_MIN],
                replace_dict=base_replace_dict)
            output(f"[+] 加载元素数量 {len(base_path_dict_list)} <--> {base_path_path}", level=LOG_INFO)
            bse_path_dict[STR_BASE_PATH].extend(base_path_dict_list)

        # 3、读取追加到根目录下的字典
        if config_dict[GB_SCAN_BASE_ROOT]:
            base_root_dict_list = read_dir_and_parse_rule_with_freq(
                read_dir_path=base_root_path,
                ext_list=config_dict[GB_DICT_SUFFIX],
                freq_symbol=config_dict[GB_FREQUENCY_SYMBOL],
                anno_symbol=config_dict[GB_ANNOTATION_SYMBOL],
                freq_min=config_dict[GB_FREQUENCY_MIN],
                replace_dict=base_replace_dict)
            output(f"[+] 加载元素数量 {len(base_root_dict_list)} <--> {base_root_path}", level=LOG_INFO)
            bse_path_dict[STR_BASE_ROOT].extend(base_root_dict_list)
    return bse_path_dict


# 生成动态排除字典
def gen_dynamic_exclude_dict(target_url, config_dict):
    test_path_1 = random_str(length=8, num=True, char=True, capital=True, dot=True, slash=True)

    test_path_2 = random_str(length=9, num=True, char=True, capital=True, dot=False, slash=True)
    test_path_2 += random_str(length=10, num=True, char=True, capital=True, dot=True, slash=True)

    test_path_3 = random_str(length=11, num=True, char=True, capital=True, dot=False, slash=True)
    test_path_3 += random_str(length=12, num=True, char=True, capital=True, dot=False, slash=True)
    test_path_3 += random_str(length=13, num=True, char=True, capital=True, dot=True, slash=True)

    test_path_list = [test_path_1, test_path_2, test_path_3]

    # 组合URL和测试路径
    base_urls = [get_curr_dir_url(target_url)]  # 这里应该采用当前目录
    test_url_path_list = combine_urls_and_paths(base_urls, test_path_list)
    # 执行测试任务
    output(f"[+] 随机访问测试 {test_url_path_list}", level=LOG_DEBUG)
    test_result_dict_list = multi_thread_requests(
        task_list=test_url_path_list,
        threads_count=config_dict[GB_THREADS_COUNT],
        thread_sleep=config_dict[GB_THREAD_SLEEP],
        req_method=config_dict[GB_REQ_METHOD],
        req_headers=config_dict[GB_REQ_HEADERS],
        req_data=config_dict[GB_REQ_BODY],
        req_proxies=config_dict[GB_PROXIES],
        req_timeout=config_dict[GB_TIME_OUT],
        verify_ssl=config_dict[GB_SSL_VERIFY],
        req_allow_redirects=config_dict[GB_ALLOW_REDIRECTS],
        req_stream=config_dict[GB_STREAM_MODE],
        retry_times=config_dict[GB_RETRY_TIMES],
        const_sign=None,
        add_host_header=config_dict[GB_DYNA_REQ_HOST],
        add_refer_header=config_dict[GB_DYNA_REQ_REFER],
        ignore_encode_error=config_dict[GB_CHINESE_ENCODE]
    )

    output(f"随机测试响应 {test_result_dict_list}", level=LOG_DEBUG)

    # 分析测试结果
    dynamic_exclude_dict = analysis_dict_same_keys(test_result_dict_list,
                                                   FILTER_HTTP_VALUE_DICT,
                                                   FILTER_DYNA_IGNORE_KEYS)
    return dynamic_exclude_dict


# 扫描主体
def dyna_scan_controller(target_urls, paths_dict, config_dict):
    # 对每个目标进行分析因变量分析和因变量替换渲染
    for target_index, target_url in enumerate(target_urls):
        output(f"[+] 任务进度 {target_index + 1}/{len(target_urls)} {target_url}", level=LOG_INFO)

        # 历史记录文件路径 基于主机HOST动态生成
        curr_host_port_string = f"{get_proto(target_url)}_{get_host_port(target_url, True)}"
        curr_host_history_file = config_dict[GB_HISTORY_FORMAT].format(mark=curr_host_port_string)
        curr_host_dyna_cache = config_dict[GB_DYNA_DICT_CACHE].format(mark=curr_host_port_string)

        # 开始进行URL测试,确定动态排除用的变量
        if file_is_empty(curr_host_dyna_cache):
            curr_dynamic_exclude_dict = gen_dynamic_exclude_dict(target_url, config_dict)
            output(f"[+] 生成动态排除字典 {target_url} -> {curr_dynamic_exclude_dict}", level=LOG_INFO)
            dump_dict_to_json(curr_host_dyna_cache, curr_dynamic_exclude_dict)
        else:
            curr_dynamic_exclude_dict = load_json_to_dict(curr_host_dyna_cache)
            output(f"[*] 加载历史排除字典 {target_url} -> {curr_dynamic_exclude_dict}", level=LOG_INFO)

        # 根据URL层级拆分为多个目标
        current_url_list = get_segment_urls(target_url) if config_dict[GB_SPLIT_TARGET] else [target_url]
        output(f"[*] URL元素 {current_url_list}", level=LOG_INFO)

        # 分别合并urls列表和paths列表
        current_url_list = combine_urls_and_path_dict(current_url_list, paths_dict)
        output(f"[*] 合并urls列表和paths字典 {len(current_url_list)}个", level=LOG_INFO)

        # 基于URL解析因变量并进行替换
        current_dependent_dict = set_dependent_var_dict(target_url=target_url,
                                                        base_dependent_dict=config_dict[GB_DEPENDENT_REPLACE_DICT],
                                                        ignore_ip_format=config_dict[GB_IGNORE_IP_FORMAT],
                                                        symbol_replace_dict=config_dict[GB_SYMBOL_REPLACE_DICT],
                                                        not_allowed_symbol=config_dict[GB_NOT_ALLOW_SYMBOL])
        output(f"[*] 因变量字典 {current_dependent_dict}", level=LOG_INFO)
        # 进行因变量替换
        current_url_list, _, _ = replace_list_has_key_str(will_replace_list=current_url_list,
                                                          replace_used_dict_=current_dependent_dict,
                                                          remove_not_render_str=True,
                                                          keep_no_repl_key_str=True)
        output(f"[*] 因变量替换 {len(current_url_list)}个", level=LOG_INFO)

        # 对url的路径进行过滤和格式化
        current_url_list = url_and_paths_dict_handle(current_url_list, config_dict)

        # 分析URL是否正确
        analysis_ends_url(current_url_list)

        # URL列表限额
        if config_dict[GB_MAX_URL_NUM] and isinstance(config_dict[GB_MAX_URL_NUM], int):
            current_url_list = current_url_list[:config_dict[GB_MAX_URL_NUM]]

        # 过滤当前的 current_url_list
        if config_dict[GB_EXCLUDE_HISTORY]:
            # 排除自定义的历史URL文件
            current_url_list = exclude_history_files(current_url_list, config_dict[GB_EXCLUDE_URLS])
            # 排除自动生成的历史URL文件
            current_url_list = exclude_history_files(current_url_list, curr_host_history_file)
            output(f"[*] 排除历史文件后剩余元素数量: {len(current_url_list)}", level=LOG_INFO)

        output(f"[*] 当前目标 {target_url} 开始进行URL访问任务处理...", level=LOG_INFO)
        # 组合爆破任务
        brute_task_list = [(url, url) for url in current_url_list]

        # 将任务列表拆分为多个任务列表 再逐步进行爆破,便于统一处理结果
        task_size = config_dict[GB_TASK_CHUNK_SIZE]
        brute_task_list = [brute_task_list[i:i + task_size] for i in range(0, len(brute_task_list), task_size)]
        output(f"[*] 任务拆分 SIZE:[{task_size}] * NUM:[{len(brute_task_list)}]", level=LOG_INFO)

        # 直接被排除的请求记录
        ignore_file_path = config_dict[GB_RESULT_DIR].joinpath(f"{curr_host_port_string}.ignore.csv")
        # 根据主机名生成结果文件名
        result_file_path = config_dict[GB_RESULT_DIR].joinpath(f"{curr_host_port_string}.result.csv")

        # 统计本目标的总访问错误次数
        access_fail_count = 0

        # 记录已命中结果的特征信息,用于过滤已命中的结果
        hit_info_hash_list = [] if config_dict[GB_HIT_INFO_EXCLUDE] else None

        # 循环多线程请求操作
        for sub_task_index, sub_task_list in enumerate(brute_task_list):
            output(f"[*] 任务进度 {sub_task_index + 1}/{len(brute_task_list)}", level=LOG_INFO)
            result_dict_list = multi_thread_requests(task_list=sub_task_list,
                                                     threads_count=config_dict[GB_THREADS_COUNT],
                                                     thread_sleep=config_dict[GB_THREAD_SLEEP],
                                                     req_method=config_dict[GB_REQ_METHOD],
                                                     req_headers=config_dict[GB_REQ_HEADERS],
                                                     req_data=config_dict[GB_REQ_BODY],
                                                     req_proxies=config_dict[GB_PROXIES],
                                                     req_timeout=config_dict[GB_TIME_OUT],
                                                     verify_ssl=config_dict[GB_SSL_VERIFY],
                                                     req_allow_redirects=config_dict[GB_ALLOW_REDIRECTS],
                                                     req_stream=config_dict[GB_STREAM_MODE],
                                                     retry_times=config_dict[GB_RETRY_TIMES],
                                                     add_host_header=config_dict[GB_DYNA_REQ_HOST],
                                                     add_refer_header=config_dict[GB_DYNA_REQ_REFER],
                                                     ignore_encode_error=config_dict[GB_CHINESE_ENCODE]
                                                     )

            # 处理响应结果
            stop_run, hit_url_list = access_result_handle(result_dict_list=result_dict_list,
                                                          dynamic_exclude_dict=curr_dynamic_exclude_dict,
                                                          ignore_file=ignore_file_path,
                                                          result_file=result_file_path,
                                                          history_file=curr_host_history_file,
                                                          access_fail_count=access_fail_count,
                                                          exclude_status_list=config_dict[GB_EXCLUDE_STATUS],
                                                          exclude_title_regexp=config_dict[GB_EXCLUDE_REGEXP],
                                                          max_error_num=config_dict[GB_MAX_ERROR_NUM],
                                                          hit_saving_field=HTTP_CONST_SIGN,
                                                          hit_info_hashes=hit_info_hash_list,
                                                          )

            # 写入命中结果
            if config_dict[GB_SAVE_HIT_RESULT] and hit_url_list:
                # 分析命中的URL 并返回命中的path部分 path部分是字典 分类包括 后缀、路径、目录、文件
                hit_classify_dict = url_to_raw_rule_classify(hit_url_list=hit_url_list,
                                                             replace_dict_list=[current_dependent_dict],
                                                             hit_ext_file=config_dict[GB_HIT_EXT_FILE],
                                                             hit_direct_file=config_dict[GB_HIT_PATH_FILE],
                                                             hit_folder_file=config_dict[GB_HIT_DIR_FILE],
                                                             hit_files_file=config_dict[GB_HIT_FILE_FILE]
                                                             )
                # 将命中的路径分别写到不同的频率文件中
                for file_name, path_list in hit_classify_dict.items():
                    auto_make_dir(os.path.dirname(file_name))
                    write_list_to_freq_file(file_path=file_name,
                                            path_list=path_list,
                                            encoding='utf-8',
                                            freq_symbol=config_dict[GB_FREQUENCY_SYMBOL],
                                            anno_symbol=config_dict[GB_ANNOTATION_SYMBOL])
                output(f"[*] 记录命中结果规则: {len(hit_url_list)}", level=LOG_INFO)
            # 停止扫描任务
            if stop_run:
                output(f"[-] 错误次数超过阈值,停止扫描目标 {target_url}", level=LOG_INFO)
                break

        output(f"[+] 测试完毕 [{target_url}]", level=LOG_INFO)


if __name__ == '__main__':
    # 加载初始设置参数
    setting_com.init_common(CONFIG)
    setting_com.init_custom(CONFIG)
    setting_http.init_custom(CONFIG)
    setting_dict.init_custom(CONFIG)

    # 设置默认debug参数日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], True)

    # 输入参数解析
    args = args_parser(CONFIG)
    output(f"[*] 输入参数信息: {args}")

    # 处理输入参数
    updates = args_dict_handle(args)
    output(f"[*] 输入参数更新: {updates}")

    # 将输入参数加入到全局CONFIG
    config_dict_add_args(CONFIG, args)

    # 更新全局CONFIG
    updates = config_dict_handle(CONFIG)
    output(f"[*] 配置参数更新: {updates}")

    # 根据用户输入的debug参数设置日志打印器属性
    set_logger(CONFIG[GB_LOG_INFO_FILE], CONFIG[GB_LOG_ERROR_FILE], CONFIG[GB_LOG_DEBUG_FILE], CONFIG[GB_DEBUG_FLAG])

    # 输出所有参数信息
    output(f"[*] 最终配置信息: {CONFIG}", level=LOG_INFO)
    # show_config_dict(CONFIG)

    # 对输入的目标数量进行处理
    output(f"[*] 分析输入目标 [{CONFIG[GB_TARGET]}] 进行访问解析测试", level=LOG_INFO)
    target_list = init_target(CONFIG)
    if not len(target_list):
        output("[-] 未输入任何有效目标,即将退出程序...", level=LOG_ERROR)
        exit()

    # 读取路径字典 进行频率筛选、规则渲染、基本变量替换
    output(f"[*] 读取字典 [{CONFIG[GB_DICT_RULE_SCAN]}] 进行频率筛选、规则渲染、基本变量替换", level=LOG_INFO)
    path_dict = init_load_dict(CONFIG)
    if not len(path_dict):
        output("[-] 未输入任何有效字典,,即将退出程序...", level=LOG_ERROR)
        exit()

    # 开始扫描
    dyna_scan_controller(target_list, path_dict, CONFIG)

    output(f"[+] 所有任务测试完毕", level=LOG_INFO)
