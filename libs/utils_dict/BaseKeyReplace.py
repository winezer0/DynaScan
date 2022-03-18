#!/usr/bin/env python
# encoding: utf-8
import queue
import re
import time


# 判断列表的元素是否有在字符串内
def list_in_str(list=[], string=""):
    flag = False
    if list:
        for i in list:
            if i in string:
                flag = True
                break
    return flag


# 替换列表中包含关键字的字符串,返回一个列表文件
def replace_list_has_key_str(replace_list=[], replace_dict={}):
    # 替换列表中包含关键字的字符串,返回一个列表文件
    # 记录开始替换的时间
    start_time = time.time()

    # 对每次替换进行一次计数
    replace_count = 0

    # 保存替换完毕后的结果文件
    result_list = []

    # 提前取出键值对,也许可以加快运行速度
    replace_dict_key = list(replace_dict.keys())

    for index in range(0, len(replace_dict_key)):

        # 提前取出索引对应的值,也许可以加快运行速度
        replace_key = replace_dict_key[index]
        # print("replace_key", replace_key)

        # 保存初次替换后还需要继续替换的字符串
        tmp_replace_list = []

        for replace_str in replace_list:
            # 如果字符串中有需要替换的键,就考虑进行替换
            if list_in_str(replace_dict_key[index:], replace_str):
                # 如果字符串中有需要替换的键,就进行替换
                if replace_key in replace_str:
                    for value in replace_dict[replace_key]:
                        replace_count = replace_count + 1
                        new_replace_str = replace_str.replace(replace_key, value)
                        # 替换后再看元素中有没有需要替换的键,
                        if list_in_str(replace_dict_key[index + 1:], new_replace_str):
                            tmp_replace_list.append(new_replace_str)
                        else:
                            result_list.append(new_replace_str)
                else:
                    tmp_replace_list.append(replace_str)
            else:
                # 没有需要替换的关键字,直接保存该项目
                result_list.append(replace_str)
        else:
            replace_list = tmp_replace_list

    result_list = list(set(result_list))
    end_time = time.time()
    run_time = end_time - start_time
    return result_list, replace_count, run_time



if __name__ == '__main__':
    replace_dict = {'%EXT%': ['aspx', 'php', 'jsp'],
                    '%BAK%': ['zip', 'rar', 'tar.gz'],
                    '%XXX%': ['XXX', 'YYY', 'ZZZ']}

    replace_str = "11111111.%EXT%.%BAK%.%XXX%"
    replace_str2 = "2222222222.%EXT%.%BAK%.%XXX%"
    replace_str_list = [replace_str, replace_str2]
    result_list, replace_count, run_time = replace_list_has_key_str(replace_str_list, replace_dict)
    print(len(result_list), replace_count, run_time)
    print(result_list)
