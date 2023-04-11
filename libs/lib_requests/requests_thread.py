#!/usr/bin/env python
# encoding: utf-8
import time

from libs.lib_log_print.logger_printer import output
from libs.lib_requests.requests_plus import requests_plus
from concurrent.futures import ThreadPoolExecutor, as_completed


# 进行多线程的URL访问测试
def multi_thread_requests_url(task_list,
                              threads_count,
                              req_method,
                              req_headers,
                              req_data,
                              req_proxies,
                              req_timeout,
                              verify_ssl,
                              req_allow_redirects,
                              retry_times,
                              thread_sleep):
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
                               retry_times=retry_times,
                               const_sign=None)
            time.sleep(thread_sleep)
            all_task.append(task)
            output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {req_url}", level="info")

        # 保存所有访问进程返回的结果
        for future in as_completed(all_task):
            access_resp_dict = future.result()
            access_result_dict_list.append(access_resp_dict)
    return access_result_dict_list


# 进行多线程的URL访问测试
def multi_thread_requests_url_sign(task_list,
                                   threads_count,
                                   req_method,
                                   req_headers,
                                   req_data,
                                   req_proxies,
                                   req_timeout,
                                   verify_ssl,
                                   req_allow_redirects,
                                   retry_times,
                                   thread_sleep):
    """
    # 对URL列表进行访问测试,输出返回响应结果
    # 创建一个最大容纳数量为threads_count的线程池,然后进行访问操作
    # 返回响应字典组成的结果列表
    """
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
                               retry_times=retry_times,
                               const_sign=const_sign)
            time.sleep(thread_sleep)
            all_task.append(task)
            output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {const_sign}", level="info")

        # 保存所有访问进程返回的结果
        for future in as_completed(all_task):
            access_resp_dict = future.result()
            access_result_dict_list.append(access_resp_dict)
    return access_result_dict_list


# 执行测试任务
def multi_thread_requests_url_body_sign(task_list,
                                        threads_count,
                                        task_method,
                                        task_headers,
                                        req_proxies,
                                        req_timeout,
                                        verify_ssl,
                                        retry_times,
                                        req_allow_redirects,
                                        thread_sleep):
    result_dict_list = []
    with ThreadPoolExecutor(max_workers=threads_count) as pool:
        for task_index, (new_url, new_body, const_sign) in enumerate(task_list):
            task = pool.submit(requests_plus,
                               req_url=new_url,
                               req_method=task_method,
                               req_headers=task_headers,
                               req_data=new_body,
                               req_proxies=req_proxies,
                               req_timeout=req_timeout,
                               verify_ssl=verify_ssl,
                               req_allow_redirects=req_allow_redirects,
                               retry_times=retry_times,
                               const_sign=const_sign)
            time.sleep(thread_sleep)
            result_dict_list.append(task)
            output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {const_sign}", level="info")
        result_dict_list = [task.result() for task in result_dict_list]
    return result_dict_list
