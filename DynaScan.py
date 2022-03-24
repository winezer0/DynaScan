#!/usr/bin/env python
# encoding: utf-8
import re
import sys

sys.dont_write_bytecode = True  # 设置不生成pyc文件

from libs.utils_dict.BaseKeyReplace import replace_list_has_key_str
from libs.utils_dict.BaseRuleParser import rule_list_base_render

from libs.HttpRequests import requests_plus
from libs.ToolUtils import get_relative_file_name, three_tuple_index_value_equal, store_specify_ext, delete_specify_ext, \
    two_tuple_list_value_equal, read_file_to_dict_with_frequency, get_key_list_with_frequency, read_many_file_to_all, combine_folder_list_and_files_list, \
    get_domain_words, get_path_words, remove_list_none_render_value, url_path_chinese_encode, url_path_url_encode, combine_one_target_and_path_list, get_segments, \
    combine_target_list_and_path_list, auto_analyse_hit_result_and_write_file, replace_multi_slashes, read_list_file_to_all, url_remove_end_symbol, url_path_lowercase
from libs.ToolUtils import remove_dict_none_value_key  # 去除字典中空值的键值对
from libs.ToolUtils import get_host_port  # 从URL中自动获取域名信息相关列表和路径信息相关列表
from setting import *  # setting.py中的变量,包括config字典
from libs.InputParse import ParserCmd  # 用于解析用户输入参数的模块
from libs.LoggerPrinter import set_logger
from concurrent.futures import ThreadPoolExecutor, as_completed


# 进行多线程的URL访问测试
def multi_threaded_requests_url(url_path_list, threads_count=10, proxies={}, cookies=None, headers=None, timeout=2, stream=False, verify=False, allow_redirects=True,
                                dynamic_host_header=True, dynamic_refer_header=True, retry_times=3, logger=None, encode='utf-8', encode_all_path=True):
    """
    # 对URL列表进行访问测试,输出返回响应结果
    # 创建一个最大容纳数量为threads_count的线程池,然后进行访问操作
    # 返回响应元组组成的结果列表
    """
    url_access_result_list = []

    # 此处使用消息队列作为线程池锁，避免在第一个任务异常发生后到主线程获知中间仍然有任务被发送执行

    with ThreadPoolExecutor(max_workers=threads_count) as pool:
        all_task = []
        for url in url_path_list:
            task = pool.submit(requests_plus, method=config.http_method, url=url, proxies=proxies, cookies=cookies, headers=headers, timeout=timeout, stream=stream,
                               verify=verify, allow_redirects=allow_redirects, dynamic_host_header=dynamic_host_header, dynamic_refer_header=dynamic_refer_header,
                               retry_times=retry_times, logger=logger, encode=encode, encode_all_path=encode_all_path)
            all_task.append(task)

        # 保存所有访问进程返回的结果
        for future in as_completed(all_task):
            url_access_result_list.append(future.result())
            # future.result()格式为元组
            # url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head = future.result()
            # 取消线程结果输出,在请求内部进行输出
            # logger.debug("[+] 线程 {} 返回结果:{}".format(future, future.result()))
    return url_access_result_list


# 处理测试URL访问结果,返回一个用于对比的此时结果字典
def handle_test_result_dict(test_path_result_dict={}, filter_moudle_default_value_dict={}, logger=None):
    dynamic_exclude_dict = {}
    for target in test_path_result_dict.keys():
        # 针对每个target进行处理,实际情况下应该只有一个target,因为处理函数在循环内部调用。
        logger.debug("[*] 当前目标 {} 测试URL结果列表:{}".format(target, test_path_result_dict[target]))

        # 测试URL结果列表:
        # [('http://127.0.0.1:8080/wfG7VrH.PQm', 404, 'Error response', 469, 469, 'Blank-Value'),
        # ('http://127.0.0.1:8080/1ccVUkW.vWR/X8cYiAe.zuK', 404, 'Error response', 469, 469, 'Blank-Value'),
        # ('http://127.0.0.1:8080/lmWE8cY.qr6/VSKFgL0.V2b/Syca58P.Cue', 404, 'Error response', 469, 469, 'Blank-Value')]

        # 结果元组对应变量名序列
        # result = (url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head)
        result_moudle_name_list = ["url", "resp_status", "resp_content_length", "resp_text_size", "resp_text_title", "resp_text_hash", "resp_bytes_head"]

        # 需要被筛选的项目对应变量名序列
        # filter_moudle_name_list = filter_moudle_default_value_dict.keys()

        # 确定各个URL的对比参数
        # {"target":{"resp_content_length":"xxx","resp_text_size":"xxx","resp_bytes_head":"xxx","resp_text_title":"xxx"}}
        # dynamic_exclusion_dict = {} 存储所有目标的对比参数
        # dynamic_exclude_dict[target] = {} 存储单个目标的对比参数
        dynamic_exclude_dict[target] = {}
        for module_name in filter_moudle_default_value_dict.keys():
            # ＃当所有测试路径的响应resp_text_title相同,并且不在module_none_value_list内 时，这个resp_content_length就能拿来作为不存在路径的参照
            module_index = result_moudle_name_list.index(module_name)  # module在结果列表内对应的反向序列
            module_none_value_list = filter_moudle_default_value_dict[module_name]
            dynamic_exclude_dict = filter_dynamic(module_name, module_index, module_none_value_list,
                                                  test_path_result_dict, dynamic_exclude_dict, target, logger)
    # dynamic_exclusion_dictionary{'https://baike.baidu.com': {'resp_text_size': 4555}, 'http://www.baidu.com': {}}
    # 去除空值的字典中的
    remove_dict_none_value_key(dynamic_exclude_dict)
    return dynamic_exclude_dict


# 把判断筛选结果的函数组合到一起
def filter_dynamic(module_name, module_index, module_none_value_list, test_path_result_dict, dynamic_exclude_dict, target, logger):
    if three_tuple_index_value_equal(test_path_result_dict[target], module_index):
        if test_path_result_dict[target][0][module_index] not in module_none_value_list:
            logger.info("[+] 当前目标 {} 可以通过 {} 筛选，不存在路径对应值应该为:[{}]".format(target, module_name, test_path_result_dict[target][1][module_index]))
            dynamic_exclude_dict[target][module_name] = test_path_result_dict[target][1][module_index]
    return dynamic_exclude_dict


# 处理拆分结果列表 并写入文件
def handle_real_result_dict(real_path_result_dict={}, logger=None, exclude_status=[], exclude_regexp='', dynamic_exclude_dict={}, exclude_dynamic_switch=True, filter_moudle_default_value_dict={}):
    # 保存所有被写入的结果列表,用于统计等
    all_write_result = []
    # 所有目标测试结果列表不为空
    if real_path_result_dict:
        # 对访问测试字典的数据进行提取,获取相关的数据
        for target in real_path_result_dict.keys():
            logger.debug("[*] 当前目标 {} 测试结果列表:{}".format(target, real_path_result_dict[target]))

            # 以目标host:port.replace(":",_)作为作为域名相关的结果文件名
            host_port_str = get_host_port(target).replace(":", "_")
            result_dir_str = str(result_dir_path).replace("\\", "/")

            if WRITE_RESULT_DIFF_SWITCH:
                if FILE_RUN_TIME_SWITCH:
                    result_path = "{}/{}_module_{}.csv".format(result_dir_str, host_port_str, RUN_TIME)
                else:
                    result_path = "{}/{}_module.csv".format(result_dir_str, host_port_str)
                logger.info("[*] 当前目标 {} 结果区分保存,结果路径: {}".format(target, result_path))
            else:
                if FILE_RUN_TIME_SWITCH:
                    result_path = "{}/module_{}.csv".format(result_dir_str, RUN_TIME)
                else:
                    result_path = "{}/module.csv".format(result_dir_str)
                logger.info("[*] 当前目标 {} 结果统一保存,结果路径: {}".format(target, result_path))

            # 构造常规的结果文件
            result_file_path = result_path.replace('module', 'result')
            result_file_path_open = open(result_file_path, "a+", encoding="utf-8")

            # 构造被过滤的结果文件名
            ignore_file_path = result_path.replace('module', 'ignore')
            ignore_file_path_open = open(ignore_file_path, "a+", encoding="utf-8")

            # 构造需要手动重试的结果文件名
            manual_file_path = result_path.replace('module', 'manual')
            manual_file_path_open = open(manual_file_path, "a+", encoding="utf-8")

            # 构造需要发生错误的结果文件名,(编码错误,)
            error_file_path = result_path.replace('module', 'error')
            error_file_path_open = open(error_file_path, "a+", encoding="utf-8")

            # 组合列表,用于快速关闭所有的文件
            list_file_path_open = [result_file_path_open, ignore_file_path_open, manual_file_path_open, error_file_path_open]

            for tuple in real_path_result_dict[target]:
                # 定义结果元组导出格式 #修改结果格式,需要修改格式串的数量
                tuple_result_format = "%s," * len(tuple) + "\n"
                # 结果元组对应顺序 # result = (url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_head, resp_bytes_head)
                url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head = tuple

                # 元组支持直接调用index返回对应结果 , resp_status = tuple[1]
                if resp_status == -1:
                    # 状态码为-1,说明没有成功获取到响应码,并且不是编码错误，需要手动重试
                    logger.debug("[-] 当前目标 {} resp_status {} 小于 0,因此本请求结果需要重试".format(url, resp_status))
                    manual_file_path_open.write(tuple_result_format % tuple)
                elif resp_status == 1:
                    # 状态码为-1,,说明没有成功获取到响应码,但是是编码错误，并且开启了编码功能，不需要手动重试
                    logger.debug("[-] 当前目标 {} resp_status {} 等于 1,因此本请求结果发生编码相关错误".format(url, resp_status))
                    error_file_path_open.write(tuple_result_format % tuple)
                elif resp_status in exclude_status:
                    # 状态码为在排除列表内,就输出到忽略文件夹
                    logger.debug("[-] 当前目标 {} resp_status {} 在 排除列表 {} 内,因此本请求结果忽略".format(url, resp_status, exclude_status))
                    ignore_file_path_open.write(tuple_result_format % tuple)
                elif resp_text_title not in filter_moudle_default_value_dict["resp_text_title"] and re.match(
                        exclude_regexp, resp_text_title, re.IGNORECASE):
                    # 标题内容被排除正则匹配,就输出到忽略文件夹
                    logger.error("[-] 当前目标 {} resp_text_title {} 被排除正则匹配,因此本请求结果忽略".format(url, resp_text_title, exclude_regexp))
                    ignore_file_path_open.write(tuple_result_format % tuple)
                elif exclude_dynamic_switch and dynamic_exclude_dict.__contains__(target):
                    # 需要被匹配的变量名字符串列表,用于根据key来动态生成变量
                    # match_list = ["resp_content_length", "resp_text_size", "resp_text_title", "resp_text_hash","resp_bytes_head"]
                    # 如果字典里包含这个目标作为的键,那就说明存在可以动态筛选的项目
                    for filter_key in dynamic_exclude_dict[target].keys():
                        filter_key_value = dynamic_exclude_dict[target][filter_key]  # 获取动态过滤字典中当前”变量名字符串“的对应的”值“
                        # 尝试使用动态字符串转变量名
                        dynamic_var_name = vars()[filter_key]
                        if dynamic_var_name == filter_key_value:
                            logger.debug("[-] 当前目标 {} {} {} == {} 因此本请求结果忽略".format(url, filter_key, dynamic_var_name, filter_key_value))
                            ignore_file_path_open.write(tuple_result_format % tuple)
                            break
                    else:
                        # 状态码都没有匹配过滤到,就输出到正常结果文件中
                        # for 循环执行完毕但是没有匹配到任何东西,就会执行else内容
                        # 如果 for 循环中有 break 字段等导致 for 循环没有正常执行完毕，那么 else 中的内容也不会执行。
                        logger.info("[+] 结果 {} 没有被动态检测情景过滤,即将被写入".format(tuple_result_format.strip()) % tuple)
                        result_file_path_open.write(tuple_result_format % tuple)
                        all_write_result.append(tuple)

                else:
                    # 状态码都没有匹配过滤到,就输出到正常结果文件中
                    logger.info("[+] 结果 {} 没有被任何情景过滤,即将被写入".format(tuple_result_format.strip()) % tuple)
                    result_file_path_open.write(tuple_result_format % tuple)
                    all_write_result.append(tuple)

            for file_open in list_file_path_open:
                file_open.close()
    else:
        logger.error("[*] 所有目标测试结果列表为空,请注意...")

    return all_write_result


# 排除已经在访问列表中的项目
def removes_the_url_from_the_visited_list(have_proto_head_host, visited_target_list, logger):
    tmp_have_proto_head_host = []
    for target in have_proto_head_host:
        if target in visited_target_list:
            logger.error("[-] 当前目标 {} 已在访问记录内,不再进行访问测试,可通过删除记录文件或关闭功能开关解决".format(target))
        else:
            tmp_have_proto_head_host.append(target)
    else:
        have_proto_head_host = tmp_have_proto_head_host
    return have_proto_head_host


# 判断输入的URL列表是否添加协议头,及是否能够访问
def attempt_add_proto_and_access(list_all_target, logger):
    # 1、对所有没有协议头的目标添加协议头。
    # 2、结果去重
    # 3、URL排除
    # 4、对所有剩余的URL进行处理
    # 4.1 如果没有开启访问测试,就直接返回URL列表
    # 4.2 如果开启访问测试就继续访问
    # 4.3 对访问结果进行筛选

    logger.info("[*] 开始对所有目标进行URL格式判断,并进行HTTP访问性判断...")
    have_proto_head_host = []  # 先存储有http头的目标,后续将URL追加进去
    none_proto_head_host = []  # 存储没有http头的目标

    # 目标熟悉判断
    for target in list_all_target:
        if target.startswith("http://") or target.startswith("https://"):
            have_proto_head_host.append(target)
        else:
            none_proto_head_host.append(target)
    logger.info("[*] 目标列表中带有协议头的目标 {}个: {}".format(len(have_proto_head_host), have_proto_head_host))
    logger.info("[*] 目标列表中没有协议头的目标 {}个: {}".format(len(none_proto_head_host), none_proto_head_host))

    # 对none_proto_head_host里面的目标进行格式处理
    if none_proto_head_host:
        need_access_url_list = []
        for target in none_proto_head_host:
            have_proto_head_host.append("http://{}".format(target))
            have_proto_head_host.append("https://{}".format(target))

    # 对所有URL目标进行去重处理
    have_proto_head_host = list(set(have_proto_head_host))
    logger.info("[*] 所有目标格式化后剩余目标 {}个: {}".format(len(have_proto_head_host), have_proto_head_host))

    # 排除URL目标中已访问过的URL
    if EXCLUDE_VISITED_TARGET_SWITCH:
        logger.info("[*] 已开启已访问URL筛选,当前正在筛选格式化后的目标列表...")
        have_proto_head_host = removes_the_url_from_the_visited_list(have_proto_head_host, VISITED_TARGET_LIST, logger)
        logger.info("[*] 所有目标进行已访问URL筛选剩余目标 {}个: {}".format(len(have_proto_head_host), have_proto_head_host))

    # 存储最终的URL列表
    new_list_all_target = []
    if not ACCESS_ADD_PROTO_HEAD:
        # 不对URL进行访问追加,而是直接进行追加。
        logger.info("[*] 协议头访问识别模式开关: {},添加http与https目标 {}个: 列表 {}".format(ACCESS_ADD_PROTO_HEAD, len(have_proto_head_host), have_proto_head_host))
        new_list_all_target.extend(have_proto_head_host)
    else:
        # 对URL进行访问测试,通过访问测试的项目才追加到最终目标内
        logger.info("[*] 协议头访问识别模式开关: {},即将进行URL访问检测,目标 {}个: 列表 {}".format(ACCESS_ADD_PROTO_HEAD, len(have_proto_head_host), have_proto_head_host))
        target_proto_result_list = multi_threaded_requests_url(have_proto_head_host, threads_count=config.threads_count, proxies=config.proxies, cookies=COOKIES,
                                                               headers=HEADERS, timeout=5, stream=HTTP_STREAM, verify=ALLOW_SSL_VERIFY, allow_redirects=ALLOW_REDIRECTS,
                                                               dynamic_host_header=DYNAMIC_HOST_HEADER, dynamic_refer_header=DYNAMIC_REFER_HEADER,
                                                               retry_times=RETRY_TIMES, logger=logger, encode_all_path=ENCODE_ALL_PATH)
        if not SMART_ADD_PROTO_HEAD:
            # 简单的判断模式,URL能够访问就加入列表
            logger.info("[*] 当前使用响应状态码模式,对访问结果进行筛选,简单判断最终协议头...")
            for tuple in target_proto_result_list:
                url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head = tuple
                if resp_status > 0:
                    logger.info("[*] 当前目标 {} 即将被添加 响应结果 {} ".format(url, tuple))
                    new_list_all_target.append(url)
                else:
                    logger.error("[*] 当前目标 {} 即将被忽略 响应结果 {} ".format(url, tuple))
        else:
            # 复杂的判断模式
            logger.info("[*] 当前使用响应结果比较模式,对访问结果进行筛选,严格判断最终协议头...")
            # 先拆分结果列表的URL,相同HOST的分为一个组
            muilt_target_proto_result_dict = {}  # 多目标协议结果字典{"host":[(结果1),(结果2),(不应该有结果3)]}
            for tuple in target_proto_result_list:
                url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head = tuple
                host_port = url.split("://", 1)[-1]
                if host_port in muilt_target_proto_result_dict.keys():
                    muilt_target_proto_result_dict[host_port].append(tuple)
                else:
                    muilt_target_proto_result_dict[host_port] = [tuple]
            logger.info("[*] 响应结果字典:{}".format(muilt_target_proto_result_dict))

            # 对拆分的结果进行遍历比较
            for target, target_proto_result_list in muilt_target_proto_result_dict.items():
                # 如果只有一个结果就说明被排除了一个,此时直接加入最终列表,
                if len(target_proto_result_list) == 1:
                    url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head = target_proto_result_list[0]
                    if resp_status > 0:
                        logger.info("[*] 当前目标 {} 仅剩余1个URL访问结果,响应状态码为 {} ,本次将添加URL {}".format(target, resp_status, url))
                        new_list_all_target.append(url)
                # 如果目标存在两个结果,说明http和https都没有被排除,
                elif len(target_proto_result_list) >= 2:
                    # 是否除了URL,其他所有的返回内容都相同,如果是的话,仅返回http协议即可
                    if two_tuple_list_value_equal(target_proto_result_list):
                        # 两个协议的访问结果相同
                        # tuple = target_proto_result_list[0]
                        # tuple_result_format = "%s," * len(tuple) + "\n"
                        # url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head = tuple
                        url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head = target_proto_result_list[0]
                        if resp_status > 0:
                            logger.info("[*] 当前目标 {} 使用两个协议进行访问测试时结果相同,响应状态码为 {} ,本次将添加 http://{}".format(target, resp_status, target))
                            new_list_all_target.append(url)
                        else:
                            logger.error("[-] 当前目标 {} 使用两个协议进行访问测试时结果相同,但响应状态码 {} ,本次目标将被过滤...".format(target, resp_status))
                    else:
                        # 两个协议的访问结果不相同
                        for tuple in target_proto_result_list:
                            url, resp_status, resp_content_length, resp_text_size, resp_text_title, resp_text_hash, resp_bytes_head = tuple
                            if resp_status > 0:
                                logger.info("[*] 当前目标 {} 使用两个协议进行访问测试时结果不相同,URL {} 状态码为 {} ,将被添加...".format(target, url, resp_status))
                                new_list_all_target.append(url)
                            else:
                                logger.error("[-] 当前目标 {} 使用两个协议进行访问测试时结果不相同,URL {} 状态码为 {} ,将被过滤...".format(target, url, resp_status))
    return new_list_all_target


# 主要的函数逻辑,注意本函数内的变量不是全局变量
def controller():
    # 程序开始运行时间
    program_start_time = time.time()

    # 解析命令行参数
    args = ParserCmd().init()

    # 对于默认为None和Flase的参数需要进行忽略,这种情况下,所有参数的默认输入值必须设置为（None和Flase）,这两种值的情况下就会调用默认值
    remove_dict_none_value_key(args)

    # 将用户输入的参数传递到config(全局字典变量) #解析命令行功能时会覆盖setting.py中的配置文件参数
    config.update(args)

    # 需要进一步手动处理的参数
    if config.__contains__("proxy") and config.proxy:
        config.proxies = {'http': config.proxy.replace('https://', 'http://'),
                          'https': config.proxy.replace('http://', 'https://')}

    # 根据用户输入的debug参数设置日志打印器属性 # 为主要是为了接受config.debug参数来配置输出颜色.
    logger = set_logger(info_log_file_path, err_log_file_path, dbg_log_file_path, config.debug)

    # 输出所有参数
    logger.info("[*] 所有输入参数信息: {}".format(config))
    logger.info("==================================================")

    # 读取用户输入的URL和目标文件参数
    list_all_target = []
    if "target" in config and config.target:
        list_all_target.append(config.target)
    elif "target_file" in config and file_is_exist(config.target_file):
        list_all_target.extend(read_file_to_list_de_weight(config.target_file))

    # 对输入的目标数量进行判断和处理
    if len(list_all_target) == 0:
        logger.error("[-] 未输入任何有效目标,即将退出程序...")
        sys.exit()
    else:
        logger.info("[*] 所有初步输入目标 {}个: {}".format(len(list_all_target), list_all_target))
        # 尝试对输入的目标进行初次过滤、添加协议头、访问测试等处理
        # 临时注释,加快调试时间
        list_all_target = attempt_add_proto_and_access(list_all_target, logger)
        list_all_target = list(set(list_all_target))
        logger.info("[+] 所有有效输入目标 {}个: {}".format(len(list_all_target), list_all_target))
    logger.info("==================================================")
    # 初次字典规则替换渲染开始时间
    render_1_start_time = time.time()
    logger.info("[*] 读取所有类型字典文件,并进行频率筛选、规则渲染、基本遍历替换...")

    ##############################################################
    # 1.1、获取基本字典目录下的所有文件名 # base_dir = './dict/base_var'
    list_dir_base_file = get_relative_file_name(dir_base_var, dict_file_suffix)
    logger.info("[*] 路径 {} 下存在基本变量规则字典: {}".format(dir_base_var, list_dir_base_file))

    # 1.2、读取BASE目录中的命中文件（ hit_ext.lst）把这个文件的内容加到所有基本变量以内
    frequency_list_hit = []
    if APPEND_HIT_EXT and file_is_exist(HIT_EXT_PATH):
        # 读取命中扩展字典文件
        frequency_dict_hit = read_file_to_dict_with_frequency(HIT_EXT_PATH, separator=SEPARATOR, additional=ADDITIONAL)
        logger.debug("[*] BASE目录中历史命中记录文件 {} 内容读取结果: {} 条 详情: {}".format(HIT_EXT_PATH, len(frequency_dict_hit), frequency_dict_hit))
        # 提取符合频率的键
        frequency_list_hit = get_key_list_with_frequency(frequency_dict_hit, frequency=FREQUENCY_MIN_HIT)
        logger.debug("[*] BASE目录中历史命中记录文件 {} 频率[{}]时筛选结果: {} 条,详情: {}".format(HIT_EXT_PATH, FREQUENCY_MIN_HIT, len(frequency_list_hit), frequency_list_hit))
        # 当开启命中扩展追加时,就不需要将命中后缀作为一个单独的替换关键字。
        hit_ext_name = HIT_EXT_PATH.rsplit('/', 1)[-1]
        if hit_ext_name in list_dir_base_file: list_dir_base_file.remove(hit_ext_name)
    logger.info("==================================================")
    # 1.3 读取所有基本替换变量字典并加入到基本变量替换字典文件
    for file_name in list_dir_base_file:
        # 从文件名中删除字典后缀,两边加上%%作为基本替换字典的键
        var_str = '%{}%'.format(file_name.rsplit(dict_file_suffix, 1)[0])
        # 读取字典内容时,进行频率筛选，返回超过频率阈值的行
        frequency_dict_ = read_file_to_dict_with_frequency(dir_base_var + '/' + file_name, separator=SEPARATOR, annotation=ANNOTATION, additional=ADDITIONAL)
        logger.debug("[*] BASE目录中常规替换字典文件 {} 内容读取结果: {} 条 详情: {}".format(dir_base_var + '/' + file_name, len(frequency_dict_), frequency_dict_))
        frequency_list_ = get_key_list_with_frequency(frequency_dict_, frequency=FREQUENCY_MIN_BASE)
        logger.debug("[*] BASE目录中常规替换字典文件 {} 频率[{}]时筛选结果: {} 条 详情: {}".format(dir_base_var + '/' + file_name, FREQUENCY_MIN_BASE, len(frequency_list_), frequency_list_))

        # 将命中扩展追加到所有基本键值对中
        if APPEND_HIT_EXT and frequency_list_hit: frequency_list_.extend(frequency_list_hit)
        if frequency_list_: BASE_VAR_REPLACE_DICT[var_str] = frequency_list_
        logger.info("[*] 基本替换变量 {} 有效替换元素 {} 个 详情: {}".format(var_str, len(frequency_list_), frequency_list_))
    logger.info("==================================================")
    # 将基本变量关键字加入全局替换关键字列表,用于最后检测请求URL是否没有替换成功
    ALL_REPLACE_KEY.extend(BASE_VAR_REPLACE_DICT.keys())

    # 去除基本替换字典中没有值的键 # 一般只有因变量字典会遇到这种情况
    remove_dict_none_value_key(BASE_VAR_REPLACE_DICT)
    logger.info("[*] 基本替换字典详情-已去除空值键: {}".format(BASE_VAR_REPLACE_DICT))
    logger.info("==================================================")

    # 对基本变量替换字典进行规则解析 # 每一行字典解析顺序-规则解析,基本变量替换,因变量替换
    logger.info("[*] 开始对基本替换字典元素进行 {XX=XXX:XXXXX}$ 规则解析渲染...")
    for key, rule_list in BASE_VAR_REPLACE_DICT.items():
        result_list, render_count, run_time = rule_list_base_render(rule_list, logger)
        BASE_VAR_REPLACE_DICT[key] = result_list
        logger.info("[*] 基本替换字典渲染后 {} 对应的替换列表元素 {} 个,本次解析规则 {} 次, 耗时 {} 秒".format(
            key, len(result_list),
            render_count, run_time))
    logger.info("==================================================")

    # 2、读取直接追加字典 # dir_path = './dict/direct_path'
    direct_path_frequency_list_ = []
    if DIRECT_DICT_MODE:
        logger.info("[+] 已开启 DIRECT 目录下的字典文件读取...")
        module = '直接追加路径'
        if SPECIFY_DIRECT_DICT:
            # 读取 DIRECT 目录的指定名称的字典文件
            logger.error("[+] 已开启 DIRECT 目录下的指定字典文件读取 {}".format(SPECIFY_DIRECT_DICT))
            direct_path_frequency_list_ = read_list_file_to_all(module, dir_direct_path, SPECIFY_DIRECT_DICT, BASE_VAR_REPLACE_DICT, SEPARATOR, ANNOTATION, ADDITIONAL, FREQUENCY_MIN_COMBIN, logger)
        else:
            # 读取 DIRECT 目录的所有字典文件
            direct_path_frequency_list_ = read_many_file_to_all(module, dir_direct_path, dict_file_suffix, BASE_VAR_REPLACE_DICT, SEPARATOR, ANNOTATION, ADDITIONAL, FREQUENCY_MIN_COMBIN, logger)
        logger.info("==================================================")
    else:
        logger.error("[-] 已关闭 DIRECT 目录下的字典文件读取...")
        logger.info("==================================================")

    # 2、分别读取 COMBIN-XXX目录下的字典,并进行合并处理
    combin_folder_files_list = []
    if COMBIN_DICT_MODE:
        logger.info("[+] 已开启 COMBIN 目录下的字典文件读取...")

        # 3、读取笛卡尔积组合字典-目录,并进行规则解析+基本变量替换
        module = '笛卡尔积组合-目录'
        if SPECIFY_COMBIN_FOLDER_DICT:
            logger.error("[+] 已开启 COMBIN-FOLDER 目录下的指定字典文件读取 {}".format(SPECIFY_COMBIN_FOLDER_DICT))
            combin_folder_frequency_list_ = read_list_file_to_all(module, dir_combin_folder, SPECIFY_COMBIN_FOLDER_DICT, BASE_VAR_REPLACE_DICT, SEPARATOR, ANNOTATION, ADDITIONAL, FREQUENCY_MIN_COMBIN, logger)
        else:
            combin_folder_frequency_list_ = read_many_file_to_all(module, dir_combin_folder, dict_file_suffix, BASE_VAR_REPLACE_DICT, SEPARATOR, ANNOTATION, ADDITIONAL, FREQUENCY_MIN_COMBIN, logger)
        logger.info("==================================================")

        # 4、读取笛卡尔积组合字典-文件,并进行规则解析+基本变量替换
        module = '笛卡尔积组合-文件'
        if SPECIFY_COMBIN_FILES_DICT:
            logger.error("[+] 已开启 COMBIN-FILES 目录下的指定字典文件读取 {}".format(SPECIFY_COMBIN_FILES_DICT))
            combin_files_frequency_list_ = read_list_file_to_all(module, dir_combin_files, dict_file_suffix, BASE_VAR_REPLACE_DICT, SEPARATOR, ANNOTATION, ADDITIONAL, FREQUENCY_MIN_COMBIN, logger)
        else:
            combin_files_frequency_list_ = read_many_file_to_all(module, dir_combin_files, dict_file_suffix, BASE_VAR_REPLACE_DICT, SEPARATOR, ANNOTATION, ADDITIONAL, FREQUENCY_MIN_COMBIN, logger)
        logger.info("==================================================")

        # 5、合并笛卡尔积组合-目录和笛卡尔积组合-文件的结果
        combin_folder_files_list, run_time = combine_folder_list_and_files_list(combin_folder_frequency_list_, combin_files_frequency_list_)
        logger.info(
            "[*] 笛卡尔积组合-目录(元素{}个) * 文件(元素{}个) 组合结果: 当前元素 {} 个, 耗时 {} s".format(len(combin_folder_frequency_list_), len(combin_files_frequency_list_), len(combin_folder_files_list), run_time))
        logger.info("==================================================")
    else:
        logger.error("[-] 已关闭 COMBIN-FOLDER 和 COMBIN-FILES 目录下的字典文件读取,本次不存在任何结果...")
        logger.info("==================================================")

    # 6、合并笛卡尔积组合字典和直接访问字典
    list_all_fuzz_path = []
    list_all_fuzz_path.extend(direct_path_frequency_list_)
    list_all_fuzz_path.extend(combin_folder_files_list)
    list_all_fuzz_path = list(set(list_all_fuzz_path))
    if list_all_fuzz_path:
        logger.info("[*] 合并直接路径列表(元素{}个) 及 笛卡尔积组合列表(元素{}个): 当前元素 {} 个".format(len(direct_path_frequency_list_), len(combin_folder_files_list), len(list_all_fuzz_path)))
        logger.debug("[*] 合并后所有路径元素内容: {} ".format(list_all_fuzz_path))
    else:
        # 如果没有任何字典,直接跳出循环
        logger.error("[!] 注意：最终组合字典列表路径元素为 {} 个, 将退出程序".format(len(list_all_fuzz_path)))
        sys.exit()
    logger.info("==================================================")

    # 初次字典规则替换组合、渲染结束时间
    render_1_end_time = time.time()
    logger.info("[*] 读取所有类型字典文件,并进行频率筛选、规则渲染、基本遍历替换,过程耗时 {} s".format(render_1_end_time - render_1_start_time))
    logger.info("==================================================")

    # 对所有目标进行分析和二次渲染,然后拼接URL进行处理
    for target in list_all_target:
        # 输出当前扫描进度
        logger.info("[+] 当前目标 {} 扫描任务进度 {}/{}...".format(target, list_all_target.index(target) + 1, len(list_all_target)))
        logger.info("==================================================")

        # 排除已访问过的URL
        if EXCLUDE_VISITED_TARGET_SWITCH:
            if target in VISITED_TARGET_LIST:
                logger.error("[-] 当前目标 {} 已在访问记录文件内,不再进行访问,可通过删除记录文件或关闭功能开关解决".format(target))
                logger.info("==================================================")
                continue

        logger.info("[+] 当前目标 {} 开始进行因变量规则提取、替换...".format(target))
        # 基于URL解析出因变量,再和初步处理的list_all_fuzz_path再次组合替换生成新的URL字典列表
        domain_var_list = get_domain_words(target, ignore_ip_format=IGNORE_IP_FORMAT, sysbol_replace_dict=DOMAIN_SYSBOL_REPLACE_DICT, remove_not_path_symbol=REMOVE_NOT_PATH_SYMBOL,
                                           not_path_symbol=NOT_PATH_SYMBOL)
        path_var_list = get_path_words(target, sysbol_replace_dict=PATH_SYSBOL_REPLACE_DICT, remove_not_path_symbol=REMOVE_NOT_PATH_SYMBOL, not_path_symbol=NOT_PATH_SYMBOL)

        # 将因变量加入因变量替换字典
        DEPEND_VAR_REPLACE_DICT = {"%%DOMAIN%%": domain_var_list, "%%PATH%%": path_var_list}

        # 将动态变量关键字加入全局替换关键字列表,用于最后检测请求URL是否没有替换成功
        ALL_REPLACE_KEY.extend(DEPEND_VAR_REPLACE_DICT.keys())

        # 如果开启了自定义替换变量,就在每个因变量的值内添加自定义变量
        if APPEND_CUSTOM_VAR and CUSTOME_REPLACE_VAR:
            logger.info("[*] 当前目标 {} 因变量字典结果{} 需要追加自定义因变量 {}".format(target, DEPEND_VAR_REPLACE_DICT, CUSTOME_REPLACE_VAR))
            for key in DEPEND_VAR_REPLACE_DICT.keys():
                DEPEND_VAR_REPLACE_DICT[key].extend(CUSTOME_REPLACE_VAR)

        # 去除因变量字典中没有获取到值的键
        remove_dict_none_value_key(DEPEND_VAR_REPLACE_DICT)
        logger.info("[*] 当前目标 {} 解析URL获取到因变量字典: {}".format(target, DEPEND_VAR_REPLACE_DICT))
        # 对所有字典进行第2次因变量替换
        if not DEPEND_VAR_REPLACE_DICT:
            # 如果没有获取到因变量,直接跳过替换
            list_one_target_url_path = list_all_fuzz_path
            logger.error("[+] 当前目标 {} 没有解析出任何因变量,本次跳过因变量替换...".format(target))
        else:
            list_one_target_url_path, replace_count, run_time = replace_list_has_key_str(list_all_fuzz_path, DEPEND_VAR_REPLACE_DICT)
            logger.info("[+] 当前目标 {} 因变量替换结束,本次解析规则 {} 次, 耗时 {} 秒 ,当前元素 {} 个".format(target, replace_count, run_time, len(list_one_target_url_path)))
        logger.info("==================================================")

        # 剔除没有被成功替换的关键字变量的路径 #任何时候都会存在没有被替换的变量
        logger.info("[*] 目标 {} 开始剔除路径列表中存在变量的路径 原有字典 [{}]条...".format(target, len(list_one_target_url_path)))
        list_one_target_url_path = remove_list_none_render_value(list_one_target_url_path, ALL_REPLACE_KEY, logger=logger)
        logger.info("[*] 目标 {} 完成剔除路径列表中存在变量的路径 当前字典 [{}]条...".format(target, len(list_one_target_url_path)))
        logger.info("==================================================")

        # 批量解决字典中文乱码问题
        if ENCODE_ALL_PATH and ENCODE_CHINESE_ONLY:
            # 方案2  #将URL字典中的中文路径进行多种编码的URL编码
            list_one_target_url_path = url_path_chinese_encode(list_one_target_url_path, logger, ALL_BASE_ENCODE)
            logger.info("[+] 当前目标 {} 所有中文编码 完成,当前元素 {} 个".format(target, len(list_one_target_url_path)))
        elif ENCODE_ALL_PATH and not ENCODE_CHINESE_ONLY:
            # 方案1  #将URL字典的所有元素都进行多种编码的URL编码,筛选其中的不同结果加入列表
            list_one_target_url_path = url_path_url_encode(list_one_target_url_path, logger, ALL_BASE_ENCODE)
            logger.info("[+] 当前目标 {} 所有特殊字符进行URL编码 完成,当前元素 {} 个".format(target, len(list_one_target_url_path)))

        # 是否开启REMOVE_MULTI_SLASHES,将多个////转换为一个/
        if REMOVE_MULTI_SLASHES:
            list_one_target_url_path = replace_multi_slashes(list_one_target_url_path)
            logger.info("[*] 当前目标 {} 已开启多个[/]转为单[/]处理,当前元素 {}个".format(target, len(list_one_target_url_path)))
            logger.info("==================================================")

        # 是否开启结尾字符列表去除
        if REMOVE_END_SYMBOL_SWITCH:
            list_one_target_url_path = url_remove_end_symbol(list_one_target_url_path, remove_symbol_list=REMOVE_SYMBOL_LIST)
            logger.info(
                "[*] 当前目标 {} 已开启结尾字符 {} 删除,当前元素 {}个".format(target, REMOVE_SYMBOL_LIST, len(list_one_target_url_path)))
            logger.info("==================================================")

        if PATH_LOWERCASE_SWITCH:
            list_one_target_url_path = url_path_lowercase(list_one_target_url_path)
            logger.info("[*] 当前目标 {} 已开启全部路径小写,当前元素 {}个".format(target, len(list_one_target_url_path)))
            logger.info("==================================================")

        # 对列表中的所有PATH添加指定前缀
        if CUSTOM_PREFIX_SWITCH:
            list_one_target_url_path = combine_folder_list_and_files_list(CUSTOM_PREFIX_LIST, list_one_target_url_path)
            logger.info("[*] 当前目标 {} 已开启自定义前缀列表功能,当前元素 {}个".format(target, len(list_one_target_url_path)))
            logger.info("==================================================")

        # 开始进行URL测试,确定动态排除用的变量
        logger.info("[+] 当前目标 {} 开始访问随机测试路径 {} ...".format(target, TEST_PATH_LIST))
        # 记录测试开始时间
        test_executor_start_time = time.time()
        # 用于存储请求所有测试路径的结果 # 初始化测试返回结果保存数组
        test_path_result_dict = {target: []}
        # 组合URL和测试路径
        test_url_path_list = combine_one_target_and_path_list(target, TEST_PATH_LIST)

        # 访问测试路径列表,返回测试结果
        test_path_result_dict[target] = multi_threaded_requests_url(test_url_path_list, threads_count=config.threads_count, proxies=config.proxies, cookies=COOKIES,
                                                                    headers=HEADERS, timeout=HTTP_TIMEOUT, stream=HTTP_STREAM, verify=ALLOW_SSL_VERIFY,
                                                                    allow_redirects=ALLOW_REDIRECTS, dynamic_host_header=DYNAMIC_HOST_HEADER, dynamic_refer_header=DYNAMIC_REFER_HEADER,
                                                                    retry_times=RETRY_TIMES, logger=logger, encode_all_path=ENCODE_ALL_PATH)

        # 提取测试路径响应结果对比项
        # 确定各个URL的对比参数 #dynamic_exclusion_dictionary存储对比参数
        # {"target":{"resp_content_length":"xxx","resp_text_size":"xxx","resp_bytes_head":"xxx"}}
        dynamic_exclude_dict = handle_test_result_dict(test_path_result_dict, FILTER_MOUDLE_DEFAULT_VALUE_DICT, logger)
        logger.info("[+] 当前目标 {} 所有测试URL访问结果筛选完毕 动态结果排除字典内容 [{}]".format(target, dynamic_exclude_dict if dynamic_exclude_dict else "无"))

        # 针对每个目标的最终字典开始进行请求处理的结束时间
        test_executor_end_time = time.time()
        logger.info("[*] 当前目标 {} 的所有测试路径URL进程访问完毕,过程耗时[{}]...".format(target, test_executor_end_time - test_executor_start_time))
        logger.info("==================================================")

        # 是否对URL路径进行分解,分解模式下一个多目录层级的URL能够变成多个目标
        target_url_list = []
        # 是否开启多目标模式,多目标模式下一个目标会根据目标目录层级拆分为多个目标
        if MULTI_TARGET_PATH_MODE:
            target_url_list = get_segments(target)
            logger.info("[*] 当前目标 {} 正处于多目标模式,扩展生成目标URL {} 个 :{} ".format(target, len(target_url_list), target_url_list))
        else:
            target_url_list.append(target)
            logger.info("[*] 当前目标 {} 正处于单目标模式,扩展生成目标URL {} 个 :{} ".format(target, len(target_url_list), target_url_list))
        logger.info("==================================================")

        # 组合URL列表和动态路径列表
        target_url_path_list = combine_target_list_and_path_list(target_url_list, list_one_target_url_path)
        logger.info("[*] 当前目标 {} 通过智能合并目标及规则字典最终生成URL数量:[{}]个".format(target, len(target_url_path_list)))
        logger.debug("[*] 当前目标 {} 通过智能合并目标及规则字典最终生成URL结果:{}".format(target, target_url_path_list))
        logger.info("==================================================")

        # 保留指定后缀的URL目标 # store_specify_ext(url_list_, ext_list_)
        if STORE_SPECIFY_EXT_SWITCH and STORE_SPECIFY_EXT_LIST:
            target_url_path_list = store_specify_ext(target_url_path_list, STORE_SPECIFY_EXT_LIST)
            logger.error("[*] 当前目标 {} 已开启保存指定后缀 {} 功能,最终提取URL数量:[{}]个".format(target, STORE_SPECIFY_EXT_LIST, len(target_url_path_list)))
            logger.info("==================================================")

        # 移除指定后缀列表的内容 # delete_specify_ext(url_list_, ext_list_)
        if DELETE_SPECIFY_EXT_SWITCH and DELETE_SPECIFY_EXT_LIST:
            target_url_path_list = delete_specify_ext(target_url_path_list, DELETE_SPECIFY_EXT_LIST)
            logger.error("[*] 当前目标 {} 已开启移除指定后缀 {} 功能,最终提取URL数量:[{}]个".format(target, DELETE_SPECIFY_EXT_LIST,
                                                                              len(target_url_path_list)))
            logger.info("==================================================")

        # 是否开启测试模式处理,只获取目标生成的100个URL进行测试
        if TEST_MODE_HANDLE:
            target_url_path_list = target_url_path_list[:100]
            logger.error("[*] 当前目标 {} 正处于测试模式,最终提取URL数量:[{}]个".format(target, len(target_url_path_list)))
            logger.info("==================================================")

        # 剔除没有被成功替换的关键字变量的目标URL # 应该没有不被替换成功的
        # logger.debug("[*] 目标 {} 开始剔除最终URL列表中替换关键字失败的请求URL 原有URL数量:[{}]个...".format(target, len(target_url_path_list)))
        # target_url_path_list = remove_list_none_render_value(target_url_path_list, ALL_REPLACE_KEY, logger=logger)
        # logger.info("[*] 目标 {} 最终URL列表剔除替换关键字失败请求URL 当前URL数量:[{}]个".format(target, len(target_url_path_list)))
        # logger.info("==================================================")

        # 剔除已经访问过的URL list3中包括所有不在list2中出现的list1中的元素
        logger.debug("[*] 当前目标 {} 开始剔除最终URL列表中被访问过的请求URL...".format(target))
        target_url_path_list = list(set(target_url_path_list) - set(ALL_ACCESSED_URL))
        logger.info("[*] 当前目标 {} 最终URL列表剔除被访问过的请求URL后,当前 URL数量:[{}]个".format(target, len(target_url_path_list)))
        logger.info("==================================================")

        logger.info("[*] 当前目标 {} 所有URL进程访问开始进行,请耐心等待请求结束(debug模式可查看请求详情)...".format(target))
        # 针对每个目标的最终字典开始进行请求处理的开始时间
        target_exec_start_time = time.time()
        # 用于存储请求所有结果文件的字典
        real_path_result_dict = {}
        # 存储URL请求函数的返回结果 real_path_result_dict = { "target":["http://x.x.x.x",] }
        real_path_result_dict[target] = []
        # 对URL列表进行访问测试,返回响应结果列表
        real_path_result_dict[target] = multi_threaded_requests_url(target_url_path_list, threads_count=config.threads_count, proxies=config.proxies, cookies=COOKIES,
                                                                    headers=HEADERS, timeout=HTTP_TIMEOUT, stream=HTTP_STREAM, verify=ALLOW_SSL_VERIFY,
                                                                    allow_redirects=ALLOW_REDIRECTS, dynamic_host_header=DYNAMIC_HOST_HEADER, dynamic_refer_header=DYNAMIC_REFER_HEADER,
                                                                    retry_times=RETRY_TIMES, logger=logger, encode_all_path=ENCODE_ALL_PATH)
        logger.info("==================================================")
        # 针对每个目标进行请求处理的结束时间
        target_exec_end_time = time.time()
        logger.info("[*] 当前目标 {} 所有URL进程访问完毕,过程耗时[{}]...".format(target, target_exec_end_time - target_exec_start_time))
        logger.info("==================================================")
        logger.info("[+] 当前目标 {} 开始处理所有URL访问测试结果 结果自动筛选分类中...".format(target))
        write_tuple_result = handle_real_result_dict(real_path_result_dict, logger, EXCLUDE_STATUS, EXCLUDE_REGEXP, dynamic_exclude_dict, EXCLUDE_DYNAMIC_SWITCH, FILTER_MOUDLE_DEFAULT_VALUE_DICT)
        logger.info("==================================================")
        if SAVE_HIT_RESULT:
            logger.info("[+] 当前目标 {} 已开启命中结果保存...".format(target))
            if write_tuple_result:
                logger.info("[+] 当前目标 {} 开始将命中的结果 {} 写入到命中文件中...".format(target, write_tuple_result))
                write_url_list = [tuple[0] for tuple in write_tuple_result]
                write_flag = auto_analyse_hit_result_and_write_file(write_url_list, BASE_VAR_REPLACE_DICT, DEPEND_VAR_REPLACE_DICT, HIT_EXT_PATH, HIT_DIRECT_PATH, HIT_FOLDER_PATH, HIT_FILES_PATH, logger,
                                                                    HIT_OVERWRITE_MODE)
                if not write_flag:
                    logger.error("[!] 当前目标 {} 命中结果写入时发生错误...".format(target))
            else:
                logger.error("[-] 当前目标 {} 在本次扫描中没有命中任何结果...".format(target))
        else:
            logger.error("[-] 当前目标 {} 已关闭命中结果保存功能...".format(target))
        logger.info("==================================================")
        with open(visited_target_file_path, 'a+', encoding='utf-8') as file_open:
            file_open.write(target + '\n')
            logger.info("[+] 当前目标 {} 已写入已访问URL记录文件 {}".format(target, visited_target_file_path))
            logger.info("==================================================")

    # 程序整体运行结束的时间
    program_end_time = time.time()
    logger.info("[+] 所有目标URL访问测试结果处理完毕,程序整体运行耗时[{}]...".format(program_end_time - program_start_time))
    logger.info("==================================================")


if __name__ == "__main__":
    controller()
