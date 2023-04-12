import json
import re
import xml.etree.ElementTree as ET
from email import parser as mimeparse
from email import policy
from urllib import parse as url_encode_parse
from urllib.parse import urlparse, parse_qs

import xmltodict  # type: ignore

# Python解析HTTP请求报文 https://blog.csdn.net/zy010101/article/details/127207055
from libs.lib_log_print.logger_printer import output

"""整体HTTP初步解析"""
ENTER = "\n"
CLRF = "\r\n"


# 基本依赖email分割 http报文(不包括body获取) 返回：http起始行，headers, body
def http_pkg_split_by_email_simple_with_sep(sep, http_pkg):
    """
    http报文分割函数
    参数：http报文字符串，分割字符
    返回：http起始行，headers, body
    """
    tmp = http_pkg.split(sep=sep, maxsplit=1)
    start_line = tmp[0]
    others = tmp[1]  # 去除http报文起始行之后，剩余的内容应完全遵从MIME数据格式
    # 指定policy为HTTP，使得遵循 RFC 2822以及当前的各种 MIME RFC（RFC 5322, RFC 2047)
    p = mimeparse.Parser(policy=policy.HTTP)
    msg = p.parsestr(text=others, headersonly=False)  # 解析header和body

    headers = {}
    for k, v in msg.items():
        headers[k] = str(v)

    tmp_ = others.split(f"{sep}{sep}", 1)
    if len(tmp_) >= 2:
        body = tmp_[-1]
    else:
        body = None
    return start_line, headers, body


# 基本依赖email解析 http报文(不包括body获取) 返回：http起始行，headers, body
def http_pkg_split_by_email_simple(http_pkg):
    """
    http报文初步解析函数
    参数：http报文字符串
    返回：http起始行，headers, body
    """
    if ENTER in http_pkg:  # 处理非CLRF分割的http报文
        res = http_pkg_split_by_email_simple_with_sep(ENTER, http_pkg)
    elif CLRF in http_pkg:
        res = http_pkg_split_by_email_simple_with_sep(CLRF, http_pkg)
    else:
        raise Exception("http报文格式错误")
    return res


# 基本依赖email解析 host, method, path, headers, body, content_type
def parse_http_pkg_by_email_simple(http_pkg):
    """
    从报文中解析出 host, method, path, headers, body, content_type
    参数： http_pkg:
    返回: host, method, path, headers, body, content_type
    """
    try:
        start_line, headers, body = http_pkg_split_by_email_simple(http_pkg=http_pkg)
        # 解析起始行
        method, path, http_version = start_line.split(" ")
        # 解析http body
        content_type = headers.get("Content-Type", "")
        # body = parse_diff_content_type_body_entirely(body, content_type)
        host = headers.get("Host", "")
    except:
        output("解析失败")
    finally:
        return host, method, path, headers, body, content_type


# 完全依赖email分割http报文(包括body部分获取) 返回：http起始行，headers, body
def http_pkg_split_by_email_entirely_with_sep(sep, http_pkg):
    """
    http报文分割函数
    参数：http报文字符串，分割字符
    返回：http起始行，headers, body
    """
    tmp = http_pkg.split(sep=sep, maxsplit=1)
    start_line = tmp[0]
    others = tmp[1]  # 去除http报文起始行之后，剩余的内容应完全遵从MIME数据格式
    # 指定policy为HTTP，使得遵循 RFC 2822以及当前的各种 MIME RFC（RFC 5322, RFC 2047)
    p = mimeparse.Parser(policy=policy.HTTP)
    msg = p.parsestr(text=others, headersonly=False)  # 解析header和body

    headers = {}
    for k, v in msg.items():
        headers[k] = str(v)
    body = msg.get_payload()
    return start_line, headers, body


# 完全依赖email分割http报文(包括body部分获取) 返回：http起始行，headers, body
def http_pkg_split_by_email_entirely(http_pkg):
    """
    http报文初步解析函数
    参数：http报文字符串
    返回：http起始行，headers, body
    """
    if ENTER in http_pkg:  # 处理非CLRF分割的http报文
        res = http_pkg_split_by_email_entirely_with_sep(ENTER, http_pkg)
    elif CLRF in http_pkg:
        res = http_pkg_split_by_email_entirely_with_sep(CLRF, http_pkg)
    else:
        raise Exception("http报文格式错误")
    return res


# 完全依赖email解析 host, method, path, headers, body, content_type
def parse_http_pkg_by_email_entirely(http_pkg):
    try:
        start_line, headers, body = http_pkg_split_by_email_entirely(http_pkg=http_pkg)
        # 解析起始行
        method, path, http_version = start_line.split(" ")
        # 解析http body
        content_type = headers.get("Content-Type", "")
        # body = parse_diff_content_type_body_entirely(body, content_type)
        host = headers.get("Host", "")
    except:
        output("解析失败")
    finally:
        return host, method, path, headers, body, content_type


"""请求Body数据解析"""


# 判断数据是否是JSON，并返回JSON解析的结构，
def data_is_json(data):
    """
    判断数据是否是JSON
    参数：数据data
    返回：一个bool值，如果是True，表示是JSON；如果是False，表示不是JSON。第二个值是JSON的情况下，返回JSON解析的结构，否则返回None
    """
    try:
        res = json.loads(data)
    except json.JSONDecodeError:
        return False, None
    else:
        return True, res


# 判断数据是否是xml，如果是并将其转为字典
def data_is_xml(data):
    """
    判断数据是否是xml，如果是并将其转为字典
    参数：数据data
    返回：一个bool值，如果是True，表示是xml；如果是False，表示不是xml
    """
    try:
        ET.fromstring(data)
    except ET.ParseError:
        return False, None
    else:
        # 是xml，并将其转为dict
        res = xmltodict.parse(data)
        return True, res


# 判断数据是否是urlencode，并返回解析后的字典
def data_is_urlencode(data):
    """
    判断数据是否是urlencode
    参数：数据data
    返回：一个bool值和一个字典，如果是True，表示是urlencode，并返回解析后的字典；如果是False，表示不是urlencode，并返回None
    """
    try:
        # 保留没有值的键，如果解析错误，引发ValueError异常
        res = url_encode_parse.parse_qs(qs=data, keep_blank_values=True, strict_parsing=True)
    except ValueError:
        return False, None
    else:
        return True, res


# 获取xml, json, urlencode解析后的结果
def parse_body_xml_json_urlencode(body, content_type=""):
    """
    获取xml, json, urlencode解析后的结果
    参数：body是http body, content_type应该取自http headers，默认为空字符串
    返回：解析后的结果可能是dict或者list
    """
    # 下面的代码借助了content_type来帮助判断，能加快解析速度。
    if "json" in content_type:
        res, data = data_is_json(body)
        if res:
            return data
        else:
            return None
    elif "xml" in content_type:
        res, data = data_is_xml(body)
        if res:
            return data
        else:
            return None
    elif "urlencode" in content_type:
        res, data = data_is_urlencode(body)
        if res:
            return data
        else:
            return None
    else:  # 无法从http headers中获取content_type或者content_type的类型不是以上几种
        res, data = data_is_json(body)
        if res:
            return data
        res, data = data_is_xml(body)
        if res:
            return data
        res, data = data_is_urlencode(body)
        if res:
            return data
        return None


# 解析multipart/form-data格式的数据
def parse_body_multipart(body, content_type=""):
    """
    解析multipart/form-data格式的数据
    参数：body是http body, content_type应该取自http headers，默认为空字符串
    返回：multipart/form-data格式的数据的解析结果
    BUG: AttributeError: 'str' object has no attribute 'items'
    """
    if "multipart/form-data" in content_type:
        res = []
        for b in body:
            for k, v in b.items():
                if k == "Content-Disposition":
                    info = url_encode_parse.parse_qs(qs=v)
                    break
            info["Content-Type"] = b.get_content_type()
            info["content"] = b.get_content()  # type: ignore
            res.append(info)
        return res
    else:
        return None


# http body解析函数 返回：解析后的结果表示为dict形式
def parse_diff_content_type_body_entirely(body, content_type=""):
    """
    http body解析函数
    参数：http body
    返回：解析后的结果表示为dict形式
    """
    if isinstance(body, str):  # xml,json,urlencode经过email模块解析之后都是str
        data = parse_body_xml_json_urlencode(body, content_type)
    elif isinstance(body, list):  # multipart/form-data解析之后是列表
        data = parse_body_multipart(body, content_type)
    else:
        data = None
    return data


# 通过字符串切割简单获取multipart格式的body参数键值对
def parse_body_multipart_simple(body, content_type):
    if "multipart/form-data" in content_type:
        # 获取multipart格式的body参数键值对
        params = {}
        boundary = content_type.split('; ')[1].split('=')[1].strip('"').strip("'")
        boundary = f'--{boundary}'
        # output(f"boundary:{boundary}")
        for part in body.strip().split(boundary):
            part = part.strip()
            # output(f"part:\n{part}")
            if part.strip().startswith('Content-Disposition'):
                _, name_str_and_value = part.split('; ')
                name_value = name_str_and_value.split('=')[1]
                split = name_value.replace("\r\n", "\n").split(f"\n\n", 1)
                name = split[0].strip('"')
                if len(split) == 2:
                    value = split[-1].strip('"')
                else:
                    value = ""
                params[name] = value
        return params
    else:
        return None


# http body解析函数 返回：解析后的结果表示为dict形式
def parse_diff_content_type_body_simple(body, content_type=""):
    """
    http body解析函数
    参数：http body
    返回：解析后的结果表示为dict形式
    """
    if "multipart/form-data" in content_type:
        data = parse_body_multipart_simple(body, content_type)
    else:
        data = parse_body_xml_json_urlencode(body, content_type)
    return data


"""解析请求路径中的参数"""


# 解析简单请求路径中的参数--新增
def parsed_query_params(request_path):
    parsed_url = urlparse(request_path)
    query_params = parse_qs(parsed_url.query)
    return query_params


# 解析简单请求体中的参数-新增
def parsed_body_params(body):
    # 解析请求体中的参数
    body_params = parse_qs(body)
    return body_params


# 解析简单请求路径和请求体中的参数--新增 不支持解析json和multipart/form-data数据
def parsed_query_and_body_params(path, body):
    params = {}
    params.update(parsed_query_params(path))
    params.update(parsed_body_params(body))
    return params


"""更新不同类型请求体中的参数"""


# 替换重构JSON格式请求体
def update_param_value_json(req_body, param_key, param_value, new_param_value):
    json_data = json.loads(req_body)
    json_data[param_key] = new_param_value
    new_req_body = json.dumps(json_data)
    return new_req_body


# 替换重构普通格式的请求体
def update_param_value_normal(req_body, param_key, param_value, new_param_value):
    if req_body and len(str(req_body).strip()) > 0:
        req_body = req_body.replace(f'{param_key}={param_value}', f'{param_key}={new_param_value}')
    return req_body


# 替换重构multipart格式的请求体
def update_param_value_multipart(req_body, param_key, param_value, new_param_value):
    # new_req_body = req_body.replace("\r\n", "\n")
    # new_req_body = new_req_body.replace(f'''"{param_key}"\n\n{param_value}''', f'''"{param_key}"\n\n{new_param_value}''')

    # 使用正则替换
    pattern = re.compile(f'''["']{param_key}["']\\s*{param_value}''')
    new_req_body = re.sub(pattern, f'''"{param_key}"\n\n{new_param_value}''', req_body)
    return new_req_body


# 替换重构xml格式的请求体
def update_param_value_xml(req_body, param_key, param_value, new_param_value):
    # new_req_body = req_body.replace("\r\n", "\n").replace("\n", "")
    # new_req_body = new_req_body.replace(f'''<{param_key}>{param_value}</{param_key}>''',f'''<{param_key}>{new_param_value}</{param_key}>''',)
    #
    # 使用正则替换
    pattern = re.compile(f'''<{param_key}>\\s*{param_value}\\s*</{param_key}>''')
    new_req_body = re.sub(pattern, f'''<{param_key}>{new_param_value}</{param_key}>''', req_body)
    return new_req_body


def update_http_param_value(req_path, req_body, req_content_type, param_key, param_value, new_param_value):
    new_req_path = req_path.replace(f'{param_key}={param_value}', f'{param_key}={new_param_value}')

    # 标记参数在请求体的位置并替换
    if "json" in req_content_type:
        # output("开始更新Json body参数")
        new_req_body = update_param_value_json(param_key, param_value, new_param_value)
        # output("json", new_req_path, new_req_body)

    elif "xml" in req_content_type:
        output("开始更新xml body参数")
        new_req_body = update_param_value_xml(req_body, param_key, param_value, new_param_value)
        # output("xml", new_req_path, new_req_body)

    elif "multipart/form-data" in req_content_type:
        # output("开始更新multipart body参数")
        new_req_body = update_param_value_multipart(req_body, param_key, param_value, new_param_value)
        # output("multipart", new_req_path, new_req_body)
    else:
        # output("开始更新普通 body参数")
        new_req_body = update_param_value_normal(req_body, param_key, param_value, new_param_value)
        # output("normal", path, body)

    return new_req_path, new_req_body


if __name__ == "__main__":
    http_pkg = """POST /v2/pet/1/uploadImage HTTP/2
Host: petstore.swagger.io
Content-Length: 998
Sec-Ch-Ua: "(Not(A:Brand";v="8", "Chromium";v="99"
Accept: application/json
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarygZCWUWVOUSClxVIr
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36
Sec-Ch-Ua-Platform: "Linux"
Origin: https://petstore.swagger.io
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://petstore.swagger.io/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9

------WebKitFormBoundarygZCWUWVOUSClxVIr
Content-Disposition: form-data; name="additionalMetadata"

2
------WebKitFormBoundarygZCWUWVOUSClxVIr
Content-Disposition: form-data; name="file"; filename="test.png"
Content-Type: image/png

\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x01)\x00\x00\x00\xdb\x08\x02\x00\x00\x00\xbe\xd6\xf0s\x00\x00\x00\tpHYs\x00\x00\x0e\xc4\x00\x00\x0e\xc4\x01\x95+\x0e\x1b\x00\x00\x02yIDATx\x9c\xed\xd31\x01\x00 \x0c\xc00\xc0\xcb\xfc[\xc4\x05=H\x14\xf4\xe9\x9e\x99\x05<w\xea\x00\xf8\x94\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0\xe1=hx\x0f\x1a\xde\x83\x86\xf7\xa0q\x01\xdb\xc4\x02%u\xd0\xc3\x18\x00\x00\x00\x00IEND\xaeB`\x82
------WebKitFormBoundarygZCWUWVOUSClxVIr--
"""
    host, method, path, headers, body, content_type = parse_http_pkg_by_email_simple(http_pkg)
    output(method)  # POST
    output(path)  # /v2/pet/1/uploadImage
    output(body)
    # [{' name': ['"additionalMetadata"'], 'Content-Type': 'text/plain', 'content': '2'}, {' name': ['"file"'], ' filename': ['"test.png"'], 'Content-Type': 'image/png', 'content': b'\x89PNG\r\n\x1a
