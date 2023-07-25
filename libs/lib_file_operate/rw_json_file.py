#!/usr/bin/env python
# encoding: utf-8
import json

import json

from libs.lib_file_operate.file_utils import file_is_empty


def load_json_to_dict(file_path, mode="r", encoding="utf-8"):
    # 加载Json文件
    if file_is_empty(file_path):
        return {}
    with open(file_path, mode=mode,encoding=encoding) as json_file:
        data = json.load(json_file)
        return data


def dump_dict_to_json(file_path, data, mode="w",encoding="utf-8"):
    # 存储Dict文件
    with open(file_path, mode=mode, encoding=encoding) as json_file:
        json.dump(data, json_file)

