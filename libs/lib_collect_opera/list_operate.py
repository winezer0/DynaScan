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


def de_dep_list(unique_lst):
    unique_lst = list(dict.fromkeys(unique_lst))
    return unique_lst
