#!/usr/bin/env python
# encoding: utf-8

import itertools
from libs.lib_rule_dict.base_rule_parser import base_rule_render_list


# 将元组列表转为字符串列表
def frozen_tuple_list(tuple_list, link_symbol="<-->"):
    unique_lst = []
    for str1, str2 in tuple_list:
        unique_lst.append(f"{str1}{link_symbol}{str2}")
    return unique_lst


# 将字符串列表转为元组列表
def unfrozen_tuple_list(str_list, link_symbol="<-->"):
    new_tuple_list = []
    for str_str2 in str_list:
        new_tuple_list.append(str_str2.split(link_symbol, 1))
    return new_tuple_list


# 去重 元组|列表 列表
def de_duplicate_tuple_list(tuple_list):
    # 将元组转换为元素不可变的类型，字符串列表
    # 然后使用set()函数将其转换为集合，
    # 最后再将集合转换回列表即可
    # frozenset(tuple) 会导致元组导致无序 # 不能用
    unique_lst = frozen_tuple_list(tuple_list, link_symbol="<-->")
    unique_lst = list(set(unique_lst))
    tuple_list = unfrozen_tuple_list(unique_lst, link_symbol="<-->")
    return tuple_list


# 笛卡尔积合并两个列表 结果格式[(a,b),(a,b)]
def cartesian_product_merging(name_list, pass_list):
    # 笛卡尔积合并两个列表 结果格式[(a,b),(a,b)]
    # 基于 itertools 生成
    cartesian_product_list = list(itertools.product(name_list, pass_list))
    # # 基于循环生成
    # cartesian_product_list = []
    # for name_ in name_list:
    #     for pass_ in pass_list:
    #         cartesian_product_list.append((name_,pass_))

    # 去重元组列表结果
    # cartesian_product_list = list(set(cartesian_product_list))
    cartesian_product_list = de_duplicate_tuple_list(cartesian_product_list)
    return cartesian_product_list


# 去除已经爆破过的元素
def remove_has_brute_user_pass_pair(name_pass_tuple_list, history_pair_str_list, pair_str_link_symbol):
    # 先将历史爆破记录转为 元组列表格式
    history_tuple_list = split_str_list_to_tuple(history_pair_str_list, pair_str_link_symbol)
    # 去重 user_name_pass_pair_list 中 被  history_user_pass_tuple_list包含的元素
    history_tuple_list = frozen_tuple_list(history_tuple_list, link_symbol=pair_str_link_symbol)
    name_pass_tuple_list = frozen_tuple_list(name_pass_tuple_list, link_symbol=pair_str_link_symbol)

    name_pass_tuple_list = list(set(name_pass_tuple_list) - set(history_tuple_list))

    name_pass_tuple_list = unfrozen_tuple_list(name_pass_tuple_list, link_symbol=pair_str_link_symbol)
    return name_pass_tuple_list


# 分割写法 分离用户名密码对
def split_str_list_to_tuple(pair_str_list, pair_link_symbol):
    tuple_list = []
    for pair_str in pair_str_list:
        user_name, user_pass = pair_str.split(pair_link_symbol, 1)
        tuple_list.append((user_name, user_pass))
    return tuple_list


# 替换基于用户名变量的密码
def replace_mark_user_name_base(user_pass_pair_list, mark_string):
    new_user_pass_pair_list = []
    for user_pass in user_pass_pair_list:
        name_ = user_pass[0]
        pass_ = user_pass[1]
        if mark_string in pass_:
            pass_ = pass_.replace(mark_string, name_)
        new_user_pass_pair_list.append((name_, pass_))

    return new_user_pass_pair_list


# 替换基于用户名变量的密码 并且支持 在替换过程中对账号密码进行处理
def replace_mark_user_name_itertools(user_pass_pair_list,
                                     mark_string,
                                     name_first_letter_upper=False,
                                     name_all_letter_lower=False,
                                     name_all_letter_upper=False,
                                     pass_first_letter_upper=False,
                                     pass_all_letter_lower=False,
                                     pass_all_letter_upper=False,
                                     only_handle_has_mark_pass=False):
    new_user_pass_pair_list = []
    for user_pass in user_pass_pair_list:
        base_name = str(user_pass[0])
        base_pass = str(user_pass[1])

        # 生成其他账号密码
        user_name_list = []
        user_pass_list = []

        # 首字母大写用户名
        if name_first_letter_upper:
            user_name_list.append(base_name.capitalize())

        # 全部小写用户名
        if name_all_letter_lower:
            user_name_list.append(base_name.lower())

        # 全部大写用户名
        if name_all_letter_upper:
            user_name_list.append(base_name.upper())

        # 替换密码内的用户名标记
        if mark_string not in base_pass:
            new_user_pass_pair_list.append((base_name, base_pass))

            # 仅处理密码中包含用户名变量的密码
            if not only_handle_has_mark_pass:
                # 首字母大写的密码
                if pass_first_letter_upper:
                    user_pass_list.append(base_pass.capitalize())

                # 全部小写的密码
                if pass_all_letter_lower:
                    user_pass_list.append(base_pass.lower())

                # 全部大写的密码
                if pass_all_letter_upper:
                    user_pass_list.append(base_pass.upper())

        else:
            # 添加普通替换
            new_user_pass_pair_list.append((base_name, base_pass.replace(mark_string, base_name)))

            # 用户名首字母大写的密码
            if pass_first_letter_upper:
                user_pass_list.append(base_pass.replace(mark_string, base_name.capitalize()))

            # 用户名全部小写的密码
            if pass_all_letter_lower:
                user_pass_list.append(base_pass.replace(mark_string, base_name.lower()))

            # 用户名全部大写的密码
            if pass_all_letter_upper:
                user_pass_list.append(base_pass.replace(mark_string, base_name.upper()))

        # 去重和填充用户名密码元素
        if user_name_list:
            user_name_list = list(set(user_name_list))
        else:
            user_name_list.append(base_name)

        if user_pass_list:
            user_pass_list = list(set(user_pass_list))
        else:
            user_pass_list.append(base_pass.replace(mark_string, base_name))

        # 组合账户密码 并存入
        product_list = list(itertools.product(user_name_list, user_pass_list))
        new_user_pass_pair_list.extend(product_list)

    return new_user_pass_pair_list


# 对列表内的元素进行长度过滤
def filter_list_by_length(string_list, min_len=0, max_len=99):
    # 处理max_len赋值错误的情况
    if max_len <= 0 or max_len <= min_len:
        max_len = 99

    # 使用列表推导式获取长度在6到16之间的元素
    result = [s for s in string_list if min_len <= len(s) <= max_len]
    return result


# 对账号密码元组进行长度过滤
def filter_pair_tuples_by_length(tuple_list, name_min_len=3, name_max_len=16, pass_min_len=3, pass_max_len=16):
    """
    tuple_list 元组列表
    ele_index   元素在元组内的索引
    """
    # 处理max_len赋值错误的情况
    if name_max_len <= name_min_len:
        name_max_len = 99

    if pass_max_len <= pass_min_len:
        pass_max_len = 99

    # 使用列表推导式获取长度在6到16之间的元素
    result = []
    for tuple_ in tuple_list:
        name_ = tuple_[0]
        pass_ = tuple_[1]
        if (name_min_len <= len(name_) <= name_max_len) and (pass_min_len <= len(pass_) <= pass_max_len):
            result.append(tuple_)
    return result


# 对 替换规则字典中的 值列表 进行 动态规则解析
def dict_content_base_rule_render(var_dict):
    # 对 替换规则字典中的 值列表 进行 动态规则解析
    for var_name, value_list in var_dict.items():
        if value_list:
            # 解析列表中的每一个元素
            result_list, render_count, run_time = base_rule_render_list(value_list)
            var_dict[var_name] = result_list
    return var_dict
