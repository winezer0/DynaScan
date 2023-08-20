#!/usr/bin/env python
# encoding: utf-8
import os

from libs.lib_file_operate.file_read import read_file_to_list
from libs.lib_file_operate.file_utils import file_is_exist


def load_targets(targets):
    if targets is None:
        return []

    # 读取用户输入 的 字符串(列表) 或者文件 (列表)
    result = []
    targets = targets if isinstance(targets, list) else [targets]
    for target in targets:
        if os.path.isfile(target):
            result = read_file_to_list(file_path=target, de_strip=True, de_weight=True, de_unprintable=True)
        else:
            result.append(target)
    # 输入数据去重
    result = list(dict.fromkeys(result))
    return result
