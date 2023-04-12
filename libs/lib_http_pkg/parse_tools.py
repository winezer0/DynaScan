#!/usr/bin/env python
# encoding: utf-8


# 判断列表内的元素是否存在有包含在字符串内的
def list_ele_in_str(list_=None, str_=None, default=False):
    if list_ is None:
        list_ = []

    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag

