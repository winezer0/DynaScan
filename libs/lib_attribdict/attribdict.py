#!/usr/bin/env python
# encoding: utf-8

"""
Copyright (c) 2006-2019 sqlmap developers (http://sqlmap.org/)
See the file 'LICENSE' for copying permission
"""

import copy
import types


class AttribDict(dict):
    """
    This class defines the sqlmap object, inheriting from Python data
    type dictionary.

    >>> foo = AttribDict()
    >>> foo.bar = 1
    >>> foo.bar
    1
    """

    def __init__(self, indict=None, attribute=None):
        # 初始化方法，可以传入一个字典对象 indict 和一个可选的属性 attribute。
        if indict is None:
            indict = {}

        # 在初始化之前设置任何属性 这些仍然是普通属性
        self.attribute = attribute
        dict.__init__(self, indict)
        self.__initialised = True
        # 初始化后，设置属性 与 设置项相同

    def __getattr__(self, item):
        # 将值映射到属性 只有当不存在带有此名称的属性时才调用
        # 当访问不存在的属性时被调用，将其映射到字典中对应的值。

        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError("unable to access item '%s'" % item)

    def __setattr__(self, item, value):
        # 将属性映射到值 只有当我们被初始化时
        # 当设置属性时被调用，将其映射到字典中对应的键值对。

        # 这个测试允许在__init__方法中设置属性
        if "_AttribDict__initialised" not in self.__dict__:
            return dict.__setattr__(self, item, value)

        # 任何正常属性都被正常处理
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)

        else:
            self.__setitem__(item, value)

    def __getstate__(self):
        # 用于序列化对象的状态
        return self.__dict__

    def __setstate__(self, dict):
        # 用于反序列化对象的状态
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        # 深度复制对象
        retVal = self.__class__()
        memo[id(self)] = retVal

        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                if not isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)):
                    setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal
