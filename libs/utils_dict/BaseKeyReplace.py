#!/usr/bin/env python
# encoding: utf-8
import itertools
import sys

from libs.LoggerPrinter import output

sys.dont_write_bytecode = True  # 设置不生成pyc文件
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


# 替换列表中包含关键字的字符串,返回一个列表文件 # 使用 itertools 实现多个列表(即多个因变量)的支持
def replace_list_has_key_str(replace_list=[], replace_dict={}):
    # 替换列表中包含关键字的字符串,返回一个列表文件
    # 记录开始替换的时间
    start_time = time.time()
    # 对每次替换进行一次计数
    replace_count = 0
    # 保存替换完毕后的结果文件
    result_list = []
    # 开始替换
    replace_keys = list(replace_dict.keys())
    # replace_values = list(replace_dict.values())
    # dict.values() 和 dict.keys()的顺序是一般一样的
    # 但是在更高版本中，不能保证它们的顺序一致。 最好手动生成
    replace_values = [replace_dict[key] for key in replace_keys]

    for string in replace_list:
        # 使用嵌套循环将多个列表进行组合
        for values in itertools.product(*replace_values):
            # 将占位符用对应的元素替换，然后添加到结果列表中
            new_string = string
            for i in range(len(replace_keys)):
                str_1 = replace_keys[i]
                if str_1 in new_string:
                    new_string = new_string.replace(str_1, values[i])
                    replace_count += 1
            result_list.append(new_string)
    # 去重
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
    output(len(result_list), replace_count, run_time)
    output(result_list)
