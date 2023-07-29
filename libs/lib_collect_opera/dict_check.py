from libs.lib_log_print.logger_printer import output, LOG_DEBUG, LOG_ERROR


def check_dict_update_eq(old_dict, new_dict):
    """
    通过循环相等判断 检查新旧字典的相同键的值更新
    :param old_dict:
    :param new_dict:
    :return:
    """
    update_dict = {}
    for same_key, old_value in old_dict.items():
        if same_key in new_dict:
            new_value = new_dict[same_key]
            if old_value != new_value:
                # print(f"Key: {same_key} | value: {old_value} --> {new_value}")
                update_dict[same_key] = new_value
    return update_dict


def check_dict_update_zip(old_dict, new_dict):
    """
    使用字典推导式和 zip() 函数找到相同键但不同值的项
    :param old_dict:
    :param new_dict:
    :return:
    """
    update_dict = {}
    different_values = {
        same_key: (old_value, new_value)
        for same_key, old_value, new_value in zip(old_dict.keys(), old_dict.values(), new_dict.values())
        if old_value != new_value
    }

    # 输出相同键但不同值的项
    for same_key, (old_value, new_value) in different_values.items():
        # print(f"Key: {same_key} | value: {old_value} --> {new_value}")
        update_dict[same_key] = new_value
    return update_dict


def check_keys_in_list(params_dict, allowed_keys):
    """
    查找参数字典中是否存在非预期的参数
    :param params_dict: 参数字典
    :param allowed_keys: 运行的参数
    :return:
    """
    unexpected = [key for key in params_dict.keys() if key not in set(allowed_keys)]
    return unexpected


def analysis_dict_same_keys(result_dict_list, exclude_value_dict, filter_ignore_keys):
    """
    分析多个字典中的相同键值对
    result_dict_list     多个字典组合的列表
    default_value_dict   需要排除的默认值（字典格式）
    filter_ignore_keys   不进行对比的键（列表格式）
    """
    # 分析 多个 字典列表 的 每个键的值是否相同, 并且不为默认值或空值
    same_key_value_dict = {}
    # 对结果字典的每个键做对比
    for key in list(result_dict_list[0].keys()):
        if key in filter_ignore_keys:
            continue
        value_list = [value_dict[key] for value_dict in result_dict_list]
        # all() 是 Python 的内置函数之一，用于判断可迭代对象中的所有元素是否都为 True
        if all(value == value_list[0] for value in value_list):
            value = value_list[0]
            if key in list(exclude_value_dict.keys()):
                if value not in exclude_value_dict[key]:
                    same_key_value_dict[key] = value
    return same_key_value_dict


def dict_eq_dict(dict_1, dict_2):
    if len(dict_1) != len(dict_2):
        return False

    # 方案21 使用==运算符来判断两个字典是否相等，因为它更简洁、更高效
    # 但 == 运算符会对字典的键和对应的值进行深度比较，对于嵌套字典或包含可变对象的情况，可能会有一些陷阱。
    # return dict_1 == dict_2

    # 方案2 遍历判断字典是否相等
    for key in dict_1:
        if key not in dict_2 or dict_1[key] != dict_2[key]:
            return False
    return True


def dict_in_dict(dict_1={}, dict_2={}, keys=None):
    # 判断dict_1字典的键的值 是否 都在dict_2 的对应键的值里面
    # 如 dict1 = {"AAA":AAA} dict2 = {"AAA":[AAA,BBB]}
    # keys 自定义需要对比的项目和顺序
    if len(dict_1) != len(dict_2):
        return False

    keys = keys or dict_1.keys()
    for k1 in keys:
        if dict_1[k1] not in dict_2[k1]:
            return False
    return True


