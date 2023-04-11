#!/usr/bin/env python
# encoding: utf-8

from libs.lib_log_print.logger_printer import output
from libs.lib_requests.requests_const import *
from libs.lib_requests.requests_thread import multi_thread_requests_url_sign


# 进行协议检查
def check_protocol(req_host, req_path, req_method, req_headers, req_proxies, req_timeout, verify_ssl):
    req_url_sign_list = []
    for proto in ["https", "http"]:
        req_url = f"{proto}://{req_host}{req_path}"
        req_url_sign_list.append((req_url, proto))

    # 开始多线程请求
    access_result_dict_list = multi_thread_requests_url_sign(task_list=req_url_sign_list,
                                                             threads_count=len(req_url),
                                                             req_method=req_method,
                                                             req_headers=req_headers,
                                                             req_data=None,
                                                             req_proxies=req_proxies,
                                                             req_timeout=req_timeout,
                                                             verify_ssl=verify_ssl,
                                                             req_allow_redirects=True,
                                                             retry_times=0,
                                                             thread_sleep=0.1
                                                             )

    # print(f"access_result_dict_list:{access_result_dict_list}")

    proto_result = {}
    for access_result_dict in access_result_dict_list:
        proto = access_result_dict[CONST_SIGN]
        proto_result[proto] = access_result_dict[RESP_STATUS]

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
def check_proto_and_access(target_list,
                           default_proto_head=None,
                           url_access_test=True,
                           req_method="GET",
                           req_headers=None,
                           req_proxies=None,
                           verify_ssl=False,
                           req_timeout=10,
                           req_path="/",
                           req_allow_redirects=False,
                           retry_times=2,
                           thread_sleep=0.1):
    # 1、对所有没有协议头的目标添加协议头。
    # 2、结果去重
    # 3、URL排除
    # 4、对所有剩余的URL进行处理
    # 4.1 如果没有开启访问测试,就直接返回URL列表
    # 4.2 如果开启访问测试就继续访问
    # 4.3 对访问结果进行筛选

    have_proto_head_host = []  # 存储有http头的目标
    none_proto_head_host = []  # 存储没有http头的目标

    # 目标熟悉判断
    for target in target_list:
        if target.startswith("http"):
            have_proto_head_host.append(target)
        else:
            none_proto_head_host.append(target)
    output(f"[*] 有协议头目标 {len(have_proto_head_host)}个 {have_proto_head_host}", level="info")
    output(f"[-] 无协议头目标 {len(none_proto_head_host)}个 {none_proto_head_host}", level="info")

    # 对none_proto_head_host里面的目标进行协议判断处理
    for target in none_proto_head_host:
        protocol = default_proto_head.lower()
        if protocol == "auto":
            protocol = check_protocol(req_host=target,
                                      req_method=req_method,
                                      req_path=req_path,
                                      req_headers=req_headers,
                                      req_proxies=req_proxies,
                                      req_timeout=req_timeout,
                                      verify_ssl=verify_ssl)
            if protocol:
                output(f"[+] 获取协议成功 [{target}]: [{protocol}]", level="info")
                have_proto_head_host.append(f"{protocol}://{target}")
            else:
                output(f"[-] 获取协议失败 [{target}] ,需手动检查重试!!!", level="error")
        else:
            have_proto_head_host.append(f"{protocol}://{target}")

    # 存储最终可以访问的URL列表
    accessible_target = []
    # 存储最终的不可访问的URL列表
    inaccessible_target = []

    if not url_access_test:
        accessible_target = have_proto_head_host
    else:
        output("[*] 批量访问筛选URL列表...", level="info")
        # 批量进行URL访问测试
        task_list = [(url, url) for url in have_proto_head_host]
        access_result_dict_list = multi_thread_requests_url_sign(task_list=task_list,
                                                                 threads_count=10,
                                                                 req_method="GET",
                                                                 req_headers=req_headers,
                                                                 req_data=None,
                                                                 req_proxies=req_proxies,
                                                                 req_timeout=10,
                                                                 verify_ssl=verify_ssl,
                                                                 req_allow_redirects=req_allow_redirects,
                                                                 retry_times=retry_times,
                                                                 thread_sleep=thread_sleep)
        # 分析多线程检测结果
        for access_result_dict in access_result_dict_list:
            req_url = access_result_dict[REQ_URL]
            resp_status = access_result_dict[RESP_STATUS]
            if resp_status > 0:
                output(f"[*] 当前目标 {req_url} 将被添加 响应结果:{access_result_dict}", level="info")
                accessible_target.append(req_url)
            else:
                output(f"[*] 当前目标 {req_url} 将被忽略 响应结果:{access_result_dict}", level="error")
                inaccessible_target.append(req_url)

    return accessible_target, inaccessible_target


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
