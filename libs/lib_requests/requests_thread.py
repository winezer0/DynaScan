#!/usr/bin/env python
# encoding: utf-8
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from libs.lib_log_print.logger_printer import output, LOG_DEBUG
from libs.lib_requests.requests_plus import requests_plus


# 进行多线程的URL访问测试
def multi_thread_requests_url(task_list,
                              threads_count,
                              thread_sleep,
                              # req_url,
                              req_method,
                              req_headers,
                              req_data,
                              req_proxies,
                              req_timeout,
                              verify_ssl,
                              req_allow_redirects,
                              req_stream,
                              retry_times,
                              const_sign,
                              add_host_header,
                              add_refer_header,
                              ignore_encode_error
                              ):
    """
    # 对URL列表进行访问测试,输出返回响应结果
    # 创建一个最大容纳数量为threads_count的线程池,然后进行访问操作
    # 返回响应字典组成的结果列表
    """
    access_result_dict_list = []

    with ThreadPoolExecutor(max_workers=threads_count) as pool:
        all_task = []
        for task_index, req_url in enumerate(task_list):
            task = pool.submit(requests_plus,
                               req_url=req_url,
                               req_method=req_method,
                               req_headers=req_headers,
                               req_data=req_data,
                               req_proxies=req_proxies,
                               req_timeout=req_timeout,
                               verify_ssl=verify_ssl,
                               req_allow_redirects=req_allow_redirects,
                               req_stream=req_stream,
                               retry_times=retry_times,
                               const_sign=const_sign,
                               add_host_header=add_host_header,
                               add_refer_header=add_refer_header,
                               ignore_encode_error=ignore_encode_error)
            time.sleep(thread_sleep)
            all_task.append(task)
            output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {req_url}", level=LOG_DEBUG)

        # 保存所有访问进程返回的结果
        for future in as_completed(all_task):
            access_resp_dict = future.result()
            access_result_dict_list.append(access_resp_dict)
    return access_result_dict_list


# 进行多线程的URL访问测试
def multi_thread_requests_url_sign(task_list,
                                   threads_count,
                                   thread_sleep,
                                   # req_url,
                                   req_method,
                                   req_headers,
                                   req_data,
                                   req_proxies,
                                   req_timeout,
                                   verify_ssl,
                                   req_allow_redirects,
                                   req_stream,
                                   retry_times,
                                   # const_sign,
                                   add_host_header,
                                   add_refer_header,
                                   ignore_encode_error
                                   ):
    # 存储所有响应结果
    access_result_dict_list = []
    with ThreadPoolExecutor(max_workers=threads_count) as pool:
        all_task = []
        for task_index, (req_url, const_sign) in enumerate(task_list):
            task = pool.submit(requests_plus,
                               req_url=req_url,
                               req_method=req_method,
                               req_headers=req_headers,
                               req_data=req_data,
                               req_proxies=req_proxies,
                               req_timeout=req_timeout,
                               verify_ssl=verify_ssl,
                               req_allow_redirects=req_allow_redirects,
                               req_stream=req_stream,
                               retry_times=retry_times,
                               const_sign=const_sign,
                               add_host_header=add_host_header,
                               add_refer_header=add_refer_header,
                               ignore_encode_error=ignore_encode_error)
            time.sleep(thread_sleep)
            all_task.append(task)
            output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {const_sign}", level=LOG_DEBUG)

        # 保存所有访问进程返回的结果
        for future in as_completed(all_task):
            access_resp_dict = future.result()
            access_result_dict_list.append(access_resp_dict)
    return access_result_dict_list


# 执行测试任务
def multi_thread_requests_url_body_sign(task_list,
                                        threads_count,
                                        thread_sleep,
                                        # req_url,
                                        req_method,
                                        req_headers,
                                        # req_data,
                                        req_proxies,
                                        req_timeout,
                                        verify_ssl,
                                        req_allow_redirects,
                                        req_stream,
                                        retry_times,
                                        # const_sign,
                                        add_host_header,
                                        add_refer_header,
                                        ignore_encode_error
                                        ):
    # 存储所有响应结果
    access_result_dict_list = []
    with ThreadPoolExecutor(max_workers=threads_count) as pool:
        for task_index, (req_url, req_data, const_sign) in enumerate(task_list):
            task = pool.submit(requests_plus,
                               req_url=req_url,
                               req_method=req_method,
                               req_headers=req_headers,
                               req_data=req_data,
                               req_proxies=req_proxies,
                               req_timeout=req_timeout,
                               verify_ssl=verify_ssl,
                               req_allow_redirects=req_allow_redirects,
                               req_stream=req_stream,
                               retry_times=retry_times,
                               const_sign=const_sign,
                               add_host_header=add_host_header,
                               add_refer_header=add_refer_header,
                               ignore_encode_error=ignore_encode_error)
            time.sleep(thread_sleep)
            access_result_dict_list.append(task)
            output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {const_sign}", level=LOG_DEBUG)
        access_result_dict_list = [task.result() for task in access_result_dict_list]
    return access_result_dict_list


# 执行测试任务
def multi_thread_requests_url_body_headers_sign(task_list,
                                                threads_count,
                                                thread_sleep,
                                                # req_url,
                                                req_method,
                                                # req_headers,
                                                # req_data,
                                                req_proxies,
                                                req_timeout,
                                                verify_ssl,
                                                req_allow_redirects,
                                                req_stream,
                                                retry_times,
                                                # const_sign,
                                                add_host_header,
                                                add_refer_header,
                                                ignore_encode_error
                                                ):
    # 存储所有响应结果
    access_result_dict_list = []
    with ThreadPoolExecutor(max_workers=threads_count) as pool:
        for task_index, (req_url, req_data, req_headers, const_sign) in enumerate(task_list):
            task = pool.submit(requests_plus,
                               req_url=req_url,
                               req_method=req_method,
                               req_headers=req_headers,
                               req_data=req_data,
                               req_proxies=req_proxies,
                               req_timeout=req_timeout,
                               verify_ssl=verify_ssl,
                               req_allow_redirects=req_allow_redirects,
                               req_stream=req_stream,
                               retry_times=retry_times,
                               const_sign=const_sign,
                               add_host_header=add_host_header,
                               add_refer_header=add_refer_header,
                               ignore_encode_error=ignore_encode_error)
            time.sleep(thread_sleep)
            access_result_dict_list.append(task)
            output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {const_sign}", level=LOG_DEBUG)
        access_result_dict_list = [task.result() for task in access_result_dict_list]
    return access_result_dict_list
