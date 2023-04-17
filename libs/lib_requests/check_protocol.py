#!/usr/bin/env python
# encoding: utf-8

from libs.lib_log_print.logger_printer import output, LOG_INFO, LOG_ERROR
from libs.lib_requests.requests_const import *
from libs.lib_requests.requests_thread import multi_thread_requests_url_sign, multi_thread_requests_url


# 进行协议检查
def check_protocol(req_host, req_path, req_method, req_headers, req_proxies, req_timeout, verify_ssl):
    req_url_task_list = []
    for protocol in ["https", "http"]:
        req_url = f"{protocol}://{req_host}{req_path}"
        req_url_task_list.append((req_url, protocol))

    # 开始多线程请求
    access_result_dict_list = multi_thread_requests_url_sign(task_list=req_url_task_list,
                                                             threads_count=min(30, len(req_url)),
                                                             thread_sleep=0.1,
                                                             req_method=req_method,
                                                             req_headers=req_headers,
                                                             req_data=None,
                                                             req_proxies=req_proxies,
                                                             req_timeout=req_timeout,
                                                             verify_ssl=verify_ssl,
                                                             req_allow_redirects=True,
                                                             req_stream=False,
                                                             retry_times=0,
                                                             add_host_header=True,
                                                             add_refer_header=True,
                                                             ignore_encode_error=True
                                                             )

    # print(f"access_result_dict_list:{access_result_dict_list}")

    proto_result = {}
    for access_result_dict in access_result_dict_list:
        protocol = access_result_dict[HTTP_CONST_SIGN]
        proto_result[protocol] = access_result_dict[HTTP_RESP_STATUS]

    output(f"[*] PROTOCOL CHECK RESULT:{proto_result}")

    if proto_result["https"] <= 0 and proto_result["http"] <= 0:
        return None

    if proto_result["https"] <= 0 and proto_result["http"] > 0:
        return "http"

    if proto_result["https"] > 0 and proto_result["http"] <= 0:
        return "https"

    if proto_result["https"] > 0 and proto_result["http"] > 0:
        if str(proto_result["https"]).startswith("30"):
            return "http"
        else:
            return "https"


# 判断输入的URL列表是否添加协议头,及是否能够访问
def check_url_list_access(target_list,
                          thread_sleep=0.1,
                          url_access_test=True,
                          req_method=None,
                          req_headers=None,
                          req_proxies=None,
                          verify_ssl=False,
                          req_timeout=10,
                          req_allow_redirects=False,
                          retry_times=2):
    # 1、对所有没有协议头的目标添加协议头。
    # 2、结果去重
    # 3、URL排除
    # 4、对所有剩余的URL进行处理
    # 4.1 如果没有开启访问测试,就直接返回URL列表
    # 4.2 如果开启访问测试就继续访问
    # 4.3 对访问结果进行筛选

    # 存储最终可以访问的URL列表
    accessible_target = []
    # 存储最终的不可访问的URL列表
    inaccessible_target = []

    if not url_access_test:
        accessible_target = target_list
    else:
        output("[*] 批量访问筛选URL列表...", level=LOG_INFO)
        # 批量进行URL访问测试
        target_list = target_list
        access_result_dict_list = multi_thread_requests_url(task_list=target_list,
                                                            threads_count=min(30, len(target_list)),
                                                            thread_sleep=thread_sleep,
                                                            req_method=req_method,
                                                            req_headers=req_headers,
                                                            req_data=None,
                                                            req_proxies=req_proxies,
                                                            req_timeout=req_timeout,
                                                            verify_ssl=verify_ssl,
                                                            req_allow_redirects=req_allow_redirects,
                                                            req_stream=False,
                                                            retry_times=retry_times,
                                                            const_sign=None,
                                                            add_host_header=True,
                                                            add_refer_header=True,
                                                            ignore_encode_error=True,
                                                            )
        # 分析多线程检测结果
        for access_result_dict in access_result_dict_list:
            req_url = access_result_dict[HTTP_REQ_URL]
            resp_status = access_result_dict[HTTP_RESP_STATUS]
            if resp_status > 0:
                output(f"[*] 当前目标 {req_url} 将被添加 响应结果:{access_result_dict}", level=LOG_INFO)
                accessible_target.append(req_url)
            else:
                output(f"[*] 当前目标 {req_url} 将被忽略 响应结果:{access_result_dict}", level=LOG_ERROR)
                inaccessible_target.append(req_url)

    return accessible_target, inaccessible_target


def check_host_list_proto(target_list, req_method, req_path, req_headers, req_proxies, req_timeout, verify_ssl, default_proto):
    have_proto_head_host = []  # 存储有http头的目标
    none_proto_head_host = []  # 存储没有http头的目标
    # 目标熟悉判断
    for target in target_list:
        if target.startswith("http"):
            have_proto_head_host.append(target)
        else:
            none_proto_head_host.append(target)
    output(f"[*] 有协议头目标 {len(have_proto_head_host)}个 {have_proto_head_host}", level=LOG_INFO)
    output(f"[-] 无协议头目标 {len(none_proto_head_host)}个 {none_proto_head_host}", level=LOG_INFO)
    # 对none_proto_head_host里面的目标进行协议判断处理
    for target in none_proto_head_host:
        protocol = str(default_proto).lower()
        if protocol == "auto":
            protocol = check_protocol(req_host=target,
                                      req_method=req_method,
                                      req_path=req_path,
                                      req_headers=req_headers,
                                      req_proxies=req_proxies,
                                      req_timeout=req_timeout,
                                      verify_ssl=verify_ssl)
            if protocol:
                output(f"[+] 获取协议成功 [{target}]: [{protocol}]", level=LOG_INFO)
                have_proto_head_host.append(f"{protocol}://{target}")
            else:
                output(f"[-] 获取协议失败 [{target}] ,需手动检查重试!!!", level=LOG_ERROR)
        else:
            have_proto_head_host.append(f"{protocol}://{target}")
    return have_proto_head_host


if __name__ == "__main__":
    req_host = 'petstore.swagger.io'
    proto = check_protocol(req_host=req_host,
                           req_path="/",
                           req_method="get",
                           req_headers=None,
                           req_proxies=None,
                           req_timeout=5,
                           verify_ssl=False
                           )
    print(f"proto:{proto}")
