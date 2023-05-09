#!/usr/bin/env python
# encoding: utf-8
import copy
import itertools
import sys
import time

from libs.lib_log_print.logger_printer import output

sys.dont_write_bytecode = True  # 设置不生成pyc文件


# 移除列表内包含未渲染字符串（ ["%%domain%%"] 等）的目标
def remove_none_render_value(will_replace_list, replace_key_list, delete_flag="$$$DEL$$$"):
    """
    # 移除列表内包含未渲染字符串（%%domain%%等）的目标
    """

    for replace_key in replace_key_list:
        if replace_key.startswith('%') and replace_key.endswith('%'):
            for index, string in enumerate(will_replace_list):
                if replace_key in string:
                    output(f"[-] {string} 中关键字[{replace_key}]没有被成功替换,正在剔除...")
                    will_replace_list[index] = delete_flag
        else:
            output(f"[-] 关键字[{replace_key}]没有遵循%key%或%%key%%命名规则...")

    will_replace_list = [path for path in will_replace_list if path != delete_flag]
    return will_replace_list


# 替换列表中包含关键字的字符串,返回一个列表文件 # 使用 itertools 实现多个列表(即多个因变量)的支持
def replace_list_has_key_str(will_replace_list=[],
                             replace_used_dict_={},
                             remove_not_render_str=True,
                             keep_no_repl_key_str=True):
    # 替换列表中包含关键字的字符串,返回一个列表文件
    # 记录开始替换的时间
    start_time = time.time()
    # 对每次替换进行一次计数
    replace_count_ = 0
    # 保存替换完毕后的结果文件
    result_list_ = []

    # 所有应该被替换的 关键字
    all_replace_keys = list(replace_used_dict_.keys())
    # 去除其中空值的键 不进行替换
    all_replace_keys = [key for key in all_replace_keys if replace_used_dict_[key]]

    # replace_values = list(replace_dict.values())
    # dict.values() 和 dict.keys()的顺序是一般一样的
    # 但是在更高版本中，不能保证它们的顺序一致。 最好手动生成
    # replace_values = [replace_used_dict_[key] for key in all_replace_keys]
    # 存在问题,会对每个字符串进行大量的替换,需要优化处理逻辑 【对每个字符串生成其最小的替换值列表】

    for string in will_replace_list:
        # 使用嵌套循环将多个列表进行组合
        # 优化 获取这个字符串里面存在的 replace_key
        practical_replace_keys = [key for key in all_replace_keys if key in string]
        # 优化 按长度大->小排序
        practical_replace_keys = sorted(practical_replace_keys, key=len, reverse=True)

        # 保留没有任何替换关键字的变量
        if not practical_replace_keys:
            if keep_no_repl_key_str:
                result_list_.append(string)
        else:
            # 优化 独立生成替换列表进行替换
            replace_values = [replace_used_dict_[key] for key in practical_replace_keys]
            for values in itertools.product(*replace_values):
                # itertools.product(*replace_values) 是要被替换的 元组
                new_string = string  # 保存原始字符串,防止影响循环替换
                for i in range(len(practical_replace_keys)):
                    replace_key = practical_replace_keys[i]
                    replace_values = values[i]
                    # if replace_key in new_string: # 上面已经判断过了，因此肯定有的
                    new_string = str(new_string).replace(replace_key, replace_values)
                    replace_count_ += 1
                result_list_.append(new_string)

    # 去重
    if result_list_:
        result_list_ = list(set(result_list_))

    # 去除没有被渲染的变量
    if remove_not_render_str:
        result_list_ = remove_none_render_value(result_list_, replace_used_dict_.keys())

    end_time = time.time()
    running_time = end_time - start_time
    return result_list_, replace_count_, running_time


def remove_not_used_key(replace_used_dict, rule_str_list):
    """
    删除不会被字典规则使用的键
    :param replace_used_dict:
    :param rule_str_list:
    :return:
    """
    # 处理输入的是二维数组的情况
    for index, str_ in enumerate(rule_str_list):
        if isinstance(rule_str_list, list):
            rule_str_list[index] = str(str_)

    # 深度拷贝原始字典
    new_replace_used_dict = copy.deepcopy(replace_used_dict)

    # 逐个判断字典的键值对是否在规则字典内
    for key in replace_used_dict.keys():
        if replace_used_dict[key] and str(key) not in str(rule_str_list):
            del new_replace_used_dict[key]
    return new_replace_used_dict


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
