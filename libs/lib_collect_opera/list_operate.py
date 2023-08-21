import itertools

from libs.lib_collect_opera.tuple_operate import de_dup_tuples


def cartesian_product_merging(name_list, pass_list):
    """
    # 笛卡尔积合并两个列表 结果格式[(a,b),(a,b)] 基于 itertools 生成
    :param name_list:
    :param pass_list:
    :return:
    """
    cartesian_product_list = list(itertools.product(name_list, pass_list))

    # # 基于循环生成
    # cartesian_product_list = []
    # for name_ in name_list:
    #     for pass_ in pass_list:
    #         cartesian_product_list.append((name_,pass_))

    # 去重元组列表结果
    # cartesian_product_list = list(set(cartesian_product_list))
    cartesian_product_list = de_dup_tuples(cartesian_product_list)
    return cartesian_product_list


def de_dup_list(unique_lst):
    # 使用字典去重
    unique_lst = list(dict.fromkeys(unique_lst))
    # 使用set去重
    # unique_lst = sorted(set(unique_lst), key=unique_lst.index)
    return unique_lst


def split_list(task_list, size):
    """
    将列表安装指定的大小分割为多个列表
    :param task_list: 原始列表
    :param size: 分割大小
    :return: 分割后的列表
    """
    task_list = [task_list[i:i + size] for i in range(0, len(task_list), size)]
    return task_list
