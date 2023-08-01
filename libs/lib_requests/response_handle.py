#!/usr/bin/env python
# encoding: utf-8
import re
import sys
from urllib.parse import quote

from libs.lib_log_print.logger_printer import output, LOG_DEBUG, LOG_ERROR
from libs.lib_requests.requests_const import *
from libs.lib_requests.requests_const import HTTP_RESP_REDIRECT, RESP_REDIRECT_ORIGIN, RESP_REDIRECT_ERROR, \
    RESP_CONTENT_BLANK, RESP_CONTENT_LARGE, RESP_CONTENT_ERROR, HTTP_RESP_CONTENT_CRC, RESP_CONTENT_CRC_BLANK, \
    RESP_CONTENT_CRC_LARGE, RESP_CONTENT_CRC_ERROR, HTTP_RESP_TITLE, RESP_TITLE_BLANK, RESP_TITLE_LARGE, \
    RESP_TITLE_ERROR, HTTP_RESP_SIZE, RESP_SIZE_BLANK, RESP_SIZE_LARGE, RESP_SIZE_ERROR, HTTP_RESP_CONTENT_OPT, \
    RESP_CONTENT_IGNORE
from libs.lib_requests.requests_utils import content_encode, replace_content
from libs.lib_collect_opera.dict_operate import sorted_data_dict, calc_dict_info_hash


def show_requests_error(url_info, common_error_list, module_name, error_info):
    # 把常规错误的关键字加入列表common_error_list内,列表为空时都作为非常规错误处理
    if any(key in str(error_info) for key in common_error_list):
        output(f"[-] 当前目标 {url_info} COMMON ERROR ON Acquire [{module_name}]: [{error_info}]", level=LOG_DEBUG)
    else:
        output(f"[-] 当前目标 {url_info} OTHERS ERROR ON Acquire [{module_name}]: [{error_info}]", level=LOG_ERROR)


def handle_common_error(req_url, error, ignore_encode_error):
    if "ConnectTimeoutError" in str(error):
        # 目标无法访问处理
        resp_status = RESP_STATUS_ERROR
        output(f"[-] 当前目标 {req_url} 连接超时,返回错误状态!!!", level=LOG_ERROR)
    elif "codec can't encode" in str(error):
        # 数据编码错误处理
        if ignore_encode_error:
            # 不需要重试的结果 设置resp_status标记为1,
            resp_status = RESP_STATUS_IGNORE
            output(f"[-] 当前目标 {req_url} 中文数据编码错误, 忽略本次错误...", level=LOG_DEBUG)
        else:
            # 需要手动访问重试的结果
            resp_status = RESP_STATUS_ERROR
            output(f"[-] 当前目标 {req_url} 中文数据编码错误, 返回错误状态!!!", level=LOG_ERROR)
    elif "No host supplied" in str(error):
        # 目标格式不正确处理
        resp_status = RESP_STATUS_IGNORE
        output(f"[-] 当前目标 {req_url} 格式输入错误,忽略本次结果!!!", level=LOG_ERROR)
    else:
        resp_status = None
    return resp_status


def analysis_resp_header(req_url, resp_headers, resp_headers_need):
    # 获取响应头相关的内容, resp_hash_headers|resp_headers_opt|resp_length
    resp_hash_headers = get_resp_headers_hash(resp_headers, req_url)
    resp_headers_opt = get_resp_headers_opt(resp_headers, req_url, resp_headers_need)
    resp_length = get_resp_header_len(resp_headers, req_url)
    return resp_headers_opt, resp_hash_headers, resp_length


def analysis_resp_body(req_url, encode_content, resp_content_need):
    # 2、获取响应HASH数据
    resp_hash_content = get_resp_body_content_hash(encode_content, req_url)
    # 3、获取响应title
    resp_text_title = get_resp_body_content_title(encode_content, req_url)
    # 4、获取响应实际大小
    resp_text_size = get_resp_body_content_size(encode_content, req_url)
    # 5、提取响应内容
    resp_content_opt = get_resp_body_content_opt(encode_content, req_url, resp_content_need)
    return resp_content_opt, resp_hash_content, resp_text_title, resp_text_size


def get_resp_body_content_opt(encode_content, req_url, resp_content_need):
    current_module = HTTP_RESP_CONTENT_OPT
    try:
        if current_module in [RESP_CONTENT_BLANK, RESP_CONTENT_ERROR, RESP_CONTENT_LARGE]:
            resp_content_opt = current_module
        else:
            # 根据用户输入获取指定的数据
            if isinstance(resp_content_need, bool) and resp_content_need:
                resp_content_opt = replace_content(encode_content)
            elif isinstance(resp_content_need, str):
                try:
                    re_find = re.findall(resp_content_need, encode_content, re.I)
                    resp_content_opt = ",".join(re_find)
                except re.error as regex_error:
                    # 正则表达式匹配错误
                    output(f"[!] 正则提取数据失败 ERROR:{regex_error}", level=LOG_ERROR)
                    resp_content_opt = RESP_CONTENT_ERROR
            else:
                resp_content_opt = RESP_CONTENT_IGNORE
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        resp_content_opt = RESP_CONTENT_ERROR
    return resp_content_opt


def get_resp_body_content_size(encode_content, req_url):
    current_module = HTTP_RESP_SIZE
    try:
        if current_module in [RESP_CONTENT_BLANK, RESP_CONTENT_ERROR]:
            resp_text_size = RESP_SIZE_BLANK
        elif current_module in [RESP_CONTENT_LARGE]:
            resp_text_size = RESP_SIZE_LARGE
        else:
            resp_text_size = len(encode_content)
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        resp_text_size = RESP_SIZE_ERROR
    return resp_text_size


def get_resp_body_content_title(encode_content, req_url):
    current_module = HTTP_RESP_TITLE
    try:
        if current_module in [RESP_CONTENT_BLANK, RESP_CONTENT_ERROR]:
            resp_text_title = RESP_TITLE_BLANK
        elif current_module in [RESP_CONTENT_LARGE]:
            resp_text_title = RESP_TITLE_LARGE
        else:
            resp_text_title = extract_title_by_re(encode_content)
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        resp_text_title = RESP_TITLE_ERROR
    return resp_text_title


def extract_title_by_re(encode_content):
    try:
        re_find = re.findall(r"<title.*?>(.+?)</title>", encode_content, re.I)
        resp_text_title = ",".join(re_find)
        resp_text_title.encode(sys.stdout.encoding)
    except re.error as regex_error:
        # 正则表达式匹配错误
        output(f"[!] 正则提取标题失败 ERROR:{regex_error}", level=LOG_ERROR)
        resp_text_title = RESP_TITLE_ERROR
    except UnicodeEncodeError as encode_error:
        resp_text_title = quote(resp_text_title.encode('utf-8'))
        output(f"[!] 使用URL编码当前标题 URL标题:{resp_text_title} Error:{encode_error}", level=LOG_ERROR)
    return resp_text_title


def extract_title_by_bs(html_markup):
    """
    获取标题
    :param html_markup: html标签
    :return: 标题
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_markup, 'lxml')

    title = soup.title
    if title:
        return title.text

    h1 = soup.h1
    if h1:
        return h1.text

    h2 = soup.h2
    if h2:
        return h2.text

    h3 = soup.h3
    if h2:
        return h3.text

    desc = soup.find('meta', attrs={'name': 'description'})
    if desc:
        return desc['content']

    word = soup.find('meta', attrs={'name': 'keywords'})
    if word:
        return word['content']

    text = soup.text
    if len(text) <= 200:
        return text.strip().replace('\r', '').replace('\n', '')
    return RESP_TITLE_BLANK


def get_resp_body_content_hash(encode_content, req_url):
    current_module = HTTP_RESP_CONTENT_CRC
    try:
        if current_module in [RESP_CONTENT_BLANK, RESP_CONTENT_ERROR]:
            resp_hash_content = RESP_CONTENT_CRC_BLANK
        elif current_module in [RESP_CONTENT_LARGE]:
            resp_hash_content = RESP_CONTENT_CRC_LARGE
        else:
            resp_hash_content = calc_dict_info_hash(encode_content, crc_mode=True)
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        resp_hash_content = RESP_CONTENT_CRC_ERROR
    return resp_hash_content


def get_resp_body_content(req_url, resp, resp_length, http_maximum_read, req_stream):
    current_module = "GET_RAW_RESP_CONTENT"
    try:
        # 1、正常获取到了响应头长度, 判断当前结果大小是否超出限制
        if isinstance(resp_length, int) and resp_length == 0:
            encode_content = RESP_CONTENT_BLANK
        elif isinstance(resp_length, int) and 0 < resp_length < http_maximum_read:
            # 大小没有超出限制, 可以进行正常读取
            encode_content = content_encode(resp.content)  # bytes类型
        else:
            # 大小超出限制|或者没有发现大小数据,只读取部分数据
            # 如果是流模式,使用raw读取 http_maximum_read
            if req_stream:
                bytes_content = resp.raw.read(http_maximum_read)
                encode_content = content_encode(bytes_content)
            else:
                encode_content = RESP_CONTENT_LARGE
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        encode_content = RESP_CONTENT_ERROR
    return encode_content


async def get_resp_body_content_httpx(req_url, resp, resp_length, http_maximum_read, req_stream):
    current_module = "GET_RAW_RESP_CONTENT"
    try:
        # 1、正常获取到了响应头长度, 判断当前结果大小是否超出限制
        if isinstance(resp_length, int) and resp_length == 0:
            encode_content = RESP_CONTENT_BLANK
        elif isinstance(resp_length, int) and 0 < resp_length < http_maximum_read:
            # 大小没有超出限制, 可以进行正常读取
            encode_content = content_encode(resp.content)  # bytes类型
        else:
            # 大小超出限制|或者没有发现大小数据,只读取部分数据
            # 如果是流模式,使用raw读取 http_maximum_read
            if req_stream:
                chunk_size = 1024
                total_bytes = bytes()
                async for chunk in resp.aiter_bytes(chunk_size=chunk_size):
                    total_bytes += chunk
                    # print(f"Received {len(chunk)} bytes")
                    if len(total_bytes) >= http_maximum_read:
                        break
                encode_content = content_encode(total_bytes)
            else:
                encode_content = RESP_CONTENT_LARGE
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        encode_content = RESP_CONTENT_ERROR
    return encode_content


def get_resp_redirect_url(req_url, resp):
    # 获取重定向后的URL信息
    current_module = HTTP_RESP_REDIRECT
    try:
        resp_redirect_url = RESP_REDIRECT_ORIGIN if req_url == str(resp.url) else str(resp.url)
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        resp_redirect_url = RESP_REDIRECT_ERROR
    return resp_redirect_url


def retry_action_check(actions_dict, response_dict):
    # 声明所有动作的优先级
    if actions_dict and response_dict:
        # priority = [HTTP_RESP_STATUS, HTTP_RESP_TITLE, HTTP_RESP_SIZE, HTTP_RESP_LENGTH, HTTP_RESP_REDIRECT, HTTP_RESP_HEADERS_CRC, HTTP_RESP_CONTENT_CRC, HTTP_RESP_HEADERS_OPT, HTTP_RESP_CONTENT_OPT]
        priority = list(response_dict.keys())
        # 根据priority列表中元素的索引进行排序 使用lambda函数来提供排序依据，
        sorted_actions = sorted(actions_dict.keys(), key=lambda x: priority.index(x))
        for ac_type in sorted_actions:
            if ac_type in response_dict.keys():
                if any(str(keyword) in str(response_dict[ac_type]) for keyword in actions_dict[ac_type]):
                    return True
    return False


def get_resp_header_len(resp_headers, req_url):
    current_module = HTTP_RESP_LENGTH
    try:
        if 'Content-Length' in resp_headers.keys():
            resp_length = int(str(resp_headers.get('Content-Length')))
        else:
            resp_length = RESP_LENGTH_BLANK
    except Exception as error:
        module_common_error_list = ["invalid literal for int()"]
        show_requests_error(req_url, module_common_error_list, current_module, error)
        resp_length = RESP_LENGTH_ERROR
    return resp_length


def get_resp_headers_opt(resp_headers, req_url, resp_headers_need):
    current_module = HTTP_RESP_HEADERS_OPT
    try:
        # 如果用户需要返回响应头,就进行返回
        if isinstance(resp_headers_need, bool) and resp_headers_need:
            resp_headers_opt = sorted_data_dict(resp_headers)
        elif isinstance(resp_headers_need, str):
            value = resp_headers.get(resp_headers_need)
            resp_headers_opt = str(value) if value else RESP_HEADERS_BLANK
        elif isinstance(resp_headers_need, list):
            # 获取自定义的响应头
            resp_headers_opt = sorted_data_dict({key: str(resp_headers.get(key)) for key in resp_headers_need})
        else:
            # 设置为忽略获取
            resp_headers_opt = RESP_HEADERS_IGNORE
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        resp_headers_opt = RESP_HEADERS_ERROR
    return resp_headers_opt


def get_resp_headers_hash(resp_headers, req_url):
    current_module = HTTP_RESP_HEADERS_CRC
    try:
        # 响应头 字符串 HASH
        if resp_headers:
            resp_hash_headers = calc_dict_info_hash(resp_headers)
        else:
            resp_hash_headers = RESP_HEADERS_CRC_BLANK
    except Exception as error:
        show_requests_error(req_url, [], current_module, error)
        resp_hash_headers = RESP_HEADERS_CRC_ERROR
    return resp_hash_headers
