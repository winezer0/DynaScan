def frozen_tuples(tuple_list, link_symbol="<-->"):
    """
    # 冻结(账号-密码)集合列表, 将集合列表转为字符串列表
    :param tuple_list:
    :param link_symbol:
    :return:
    """
    unique_lst = []
    for str1, str2 in tuple_list:
        unique_lst.append(f"{str1}{link_symbol}{str2}")
    return unique_lst


def unfrozen_tuples(str_list, link_symbol="<-->"):
    """
    # 解冻(账号-密码)字符串列表, 将字符串列表转为元组列表
    :param str_list:
    :param link_symbol:
    :return:
    """
    tuple_list = []
    for str_ in str_list:
        tuple_list.append(tuple(str_.split(link_symbol, 1)))
    return tuple_list


def de_dup_tuples(tuple_list):
    """
    # 去重(账号-密码)元组列表  PS:列表元素如果是元组也可以直接set去重
    :param tuple_list:
    :return:
    """
    # 将元组转换为元素不可变的类型，字符串列表
    # 然后使用set()函数将其转换为集合，
    # 最后再将集合转换回列表即可
    # frozenset(tuple) 会导致元组导致无序 # 不能用
    unique_lst = frozen_tuples(tuple_list, link_symbol="<-->")
    if unique_lst:
        unique_lst = list(set(unique_lst))
    tuple_list = unfrozen_tuples(unique_lst, link_symbol="<-->")
    return tuple_list


def tuples_subtract(reduced_tuples, reduce_tuples, link_symbol):
    """
    冻结 元组 解冻并相减 （去除已经爆破过的元素 ）
    :param reduced_tuples:
    :param reduce_tuples:
    :param link_symbol:
    :return:
    """
    if reduced_tuples and reduce_tuples:
        # 去重 user_name_pass_pair_list 中 被  history_user_pass_tuple_list包含的元素
        reduce_tuples = frozen_tuples(reduce_tuples, link_symbol=link_symbol)
        reduced_tuples = frozen_tuples(reduced_tuples, link_symbol=link_symbol)
        reduced_tuples = list(set(reduced_tuples) - set(reduce_tuples))
        reduced_tuples = unfrozen_tuples(reduced_tuples, link_symbol=link_symbol)
    return reduced_tuples