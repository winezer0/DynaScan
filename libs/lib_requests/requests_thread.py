#!/usr/bin/env python
# encoding: utf-8
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from libs.lib_log_print.logger_printer import output, LOG_DEBUG
from libs.lib_requests.requests_httpx import httpx_plus
from libs.lib_requests.requests_plus import requests_plus

# 输入的字典格式时
TASK_URL = "httpx_plus"
TASK_DATA = "req_data"
TASK_HEADERS = "req_headers"
TASK_SIGN = "const_sign"
TASK_FORMAT = {TASK_URL: 0, TASK_DATA: 0, TASK_HEADERS: 0, TASK_SIGN: 0}  # 必须按照这个格式赋值


# 回调函数
def callback_func(future):
    # 当需要在 多线程 请求 内部进行操作时,需要自定义回调函数
    # try:
    #     result = future.result()  # 获取任务的执行结果
    #     print(f"[*] Callback function: Task result: {result}")
    # except Exception as e:
    #     print(f"[!] Callback function: Task raised an exception: {e}")
    pass


def parse_task_info(task_info, const_sign, req_data, req_headers):
    if isinstance(task_info, str):
        # 输入的时URL列表时
        req_url = task_info
    elif isinstance(task_info, tuple):
        # 输入的是(httpx_plus,const_sign,req_data, req_headers)元组列表时,必须按照这个顺序
        if len(task_info) > 4:
            raise ValueError(f"Task Parameter Numbers Error")
        req_url, tmp_sign, tmp_data, tmp_headers = task_info + (None,) * (4 - len(task_info))
        const_sign = tmp_sign or const_sign
        req_data = tmp_data or req_data
        req_headers = tmp_headers or req_headers
    elif isinstance(task_info, dict):
        invalid_params = set(task_info.keys()) - frozenset(list(TASK_FORMAT.keys()))
        if invalid_params:
            raise ValueError(f"Task Parameter Invalid: {', '.join(invalid_params)}")
        req_url = task_info.get(TASK_URL)
        req_data = task_info.get(TASK_DATA, None) or req_data
        req_headers = task_info.get(TASK_HEADERS, None) or req_headers
        const_sign = task_info.get(TASK_SIGN, None) or const_sign
    else:
        raise "Task Parameter Type Error"
    return req_url, const_sign, req_data, req_headers


def multi_thread_requests(task_list,
                          threads_count=100,
                          thread_sleep=0,
                          req_method="GET",
                          req_headers=None,  # 可选
                          req_data=None,  # 可选
                          req_proxies=None,
                          req_timeout=5,
                          verify_ssl=False,
                          req_allow_redirects=False,
                          req_stream=False,
                          retry_times=3,
                          const_sign=None,  # 可选
                          add_host_header=True,
                          add_refer_header=True,
                          ignore_encode_error=False,
                          resp_headers_need=True,
                          resp_content_need=False,
                          active_retry_dict=None,
                          ):
    # 存储所有响应结果
    with ThreadPoolExecutor(max_workers=threads_count) as pool:
        all_task = []
        for task_index, task_info in enumerate(task_list):
            req_url, const_sign, req_data, req_headers = parse_task_info(task_info, const_sign, req_data, req_headers)
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
                               ignore_encode_error=ignore_encode_error,
                               resp_headers_need=resp_headers_need,
                               resp_content_need=resp_content_need,
                               active_retry_dict=active_retry_dict,
                               )
            # 添加回调函数 回调函数将在任务完成后被调用，并接收 Future 对象作为参数，从而可以获取任务的执行结果。
            task.add_done_callback(callback_func)
            # time.sleep(thread_sleep)
            all_task.append(task)
            output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {const_sign or req_url}", level=LOG_DEBUG)
        all_access_result = [future.result() for future in as_completed(all_task)]
        # all_access_result = [task.result() for task in all_task]
        return all_access_result


def async_httpx(task_list,
                thread_count=100,
                thread_sleep=0,  # 限制失败
                req_method="GET",
                req_headers=None,  # 可选
                req_data=None,  # 可选
                req_proxies=None,
                req_timeout=5,
                verify_ssl=False,
                req_allow_redirects=False,
                req_stream=False,
                retry_times=3,
                const_sign=None,  # 可选
                add_host_header=True,
                add_refer_header=True,
                ignore_encode_error=False,
                resp_headers_need=True,
                resp_content_need=False,
                active_retry_dict=None,
                ):
    loop = asyncio.get_event_loop()

    # 创建多个任务
    tasks = []
    # for task_index, task_info in enumerate(task_list):
    for task_index, task_info in enumerate(task_list):
        req_url, const_sign, req_data, req_headers = parse_task_info(task_info, const_sign, req_data, req_headers)
        task = loop.create_task(httpx_plus(req_url=req_url,
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
                                           ignore_encode_error=ignore_encode_error,
                                           resp_headers_need=resp_headers_need,
                                           resp_content_need=resp_content_need,
                                           active_retry_dict=active_retry_dict,
                                           thread_count=thread_count,
                                           ))
        # 添加回调函数 回调函数将在任务完成后被调用，并接收 Future 对象作为参数，从而可以获取任务的执行结果。
        task.add_done_callback(callback_func)
        tasks.append(task)
        output(f"[*] 当前进度 {task_index + 1}/{len(task_list)} {const_sign or req_url}", level=LOG_DEBUG)
    # loop.run_until_complete(asyncio.wait(tasks)) 会等待 tasks 中的所有协程运行完成。
    loop.run_until_complete(asyncio.wait(tasks))
    all_access_result = [task.result() for task in tasks]
    return all_access_result
