#!/usr/bin/env python
# encoding: utf-8

import os
import os.path
import random
import time
import urllib
from pathlib import Path
import re
from urllib.parse import urlparse
from tldextract import extract
from libs.UrlSplitParser import UrlSplitParser
from libs.utils_dict.BaseRuleParser import rule_list_base_render
from libs.utils_dict.BaseKeyReplace import replace_list_has_key_str

"""
from filecmp import cmp

# 文件处理工具类
class File(object):

    def __init__(self, *pathComponents):
        self._path = FileUtils.buildPath(*pathComponents)
        self.content = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        raise NotImplemented

    def isValid(self):
        return FileUtils.isFile(self.path)

    def exists(self):
        return FileUtils.exists(self.path)

    def canRead(self):
        return FileUtils.canRead(self.path)

    def canWrite(self):
        return FileUtils.canWrite(self.path)

    def read(self):
        return FileUtils.read(self.path)

    def update(self):
        self.content = self.read()

    def content(self):
        if not self.content:
            self.content = FileUtils.read()
        return self.content()

    def getLines(self):
        for line in FileUtils.getLines(self.path):
            yield line

    def __cmp__(self, other):
        if not isinstance(other, File):
            raise NotImplemented
        return cmp(self.content(), other.content())

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

# 文件处理工具类
class FileUtils(object):

    @staticmethod
    def buildPath(*pathComponents):
        if pathComponents:
            path = os.path.join(*pathComponents)
        else:
            path = ''
        return path

    @staticmethod
    def exists(fileName):
        return os.access(fileName, os.F_OK)

    @staticmethod
    def canRead(fileName):
        if not os.access(fileName, os.R_OK):
            return False
        try:
            with open(fileName):
                pass
        except IOError:
            return False
        return True

    @staticmethod
    def canWrite(fileName):
        return os.access(fileName, os.W_OK)

    @staticmethod
    def read(fileName):
        result = ''
        with open(fileName, 'r') as fd:
            for line in fd.readlines():
                result += line
        return result

    @staticmethod
    def getLines(fileName):
        with open(fileName, 'r') as fd:
            for line in fd.readlines():
                yield line.replace('\n', '')

    @staticmethod
    def isDir(fileName):
        return os.path.isdir(fileName)

    @staticmethod
    def isFile(fileName):
        return os.path.isfile(fileName)

    @staticmethod
    def createDirectory(directory):
        if not FileUtils.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def sizeHuman(num):
        base_var = 1024
        for x in ['B ', 'KB', 'MB', 'GB']:
            if num < base_var and num > -base_var:
                return "%3.0f%s" % (num, x)
            num /= base_var
        return "%3.0f %s" % (num, 'TB')
"""


########字典文件读取相关######################
# 获取目录下的文件列表,返回基于输入文件目录的拼接文件名路径列表【半绝对路径】
def get_absolute_file_name(file_dir, ext=''):
    """
    获取目录下的文件列表,返回基于输入文件目录的拼接文件名路径列表
    """
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        """
        print(root) #当前目录路径
        print(dirs) #当前路径下所有子目录
        print(combin_files) #当前路径下所有非目录子文件
        """
        for file in files:
            if file.endswith(ext):
                file_list.append(root + '/' + file)
    return file_list


# 获取目录下的文件列表,返回目录下的文件名列表【相对路径】
def get_relative_file_name(file_dir, ext=''):
    """
    获取目录下的文件列表,返回目录下的文件名列表
    """
    file_list = []
    for root, dirs, files in os.walk(file_dir):
        """
        print(root) #当前目录路径
        print(dirs) #当前路径下所有子目录
        print(combin_files) #当前路径下所有非目录子文件
        """
        for file in files:
            if file.endswith(ext):
                file_list.append(file)
    return file_list


# 判断文件是否存在
def file_is_exist(filepath):
    '''判断文件是否存在'''
    if filepath:
        path = Path(filepath)
        if path.is_file():
            return True
        else:
            return False


# 读取文件内容并返回字符串
def read_file_to_str(file_name, type='utf-8'):
    """
    读取文件内容并返回字符串
    """
    result_str = ""
    with open(file_name, 'r', encoding=type) as f_obj:
        result_str = f_obj.read().strip()
        return result_str


# 读取文件内容并返回结果列表
def read_file_to_list_de_weight(file_name, type='utf-8'):
    """
    读取文件内容并返回结果列表
    """
    with open(file_name, 'r', encoding=type) as f_obj:
        result_list = []
        for line in f_obj.readlines():
            if line.strip() != "":
                result_list.append(line.strip())
        return result_list


# 读取一个文件内容并返回结果字典 {"路径”:频率}
def read_file_to_dict_with_frequency(file_name, type='utf-8', separator='frequency==', annotation='#', additional=True):
    """
    读取文件内容并返回结果字典
    文件的每一行格式类似 path separator==10
    没有separatorq的默认为1
    # print(read_file_to_dict_with_frequency("../dict/base_var/backup_ext.lst"))
    # {'.rar': 1, '.zip': 1, '.gz': 1, '.tar': 1, '.tgz': 1, '.tar.gz': 1, '.7z': 1, '.z': 1, '.bz2': 1, '.tar.bz2': 1, '.iso': 1, '.cab': 1}

    separator 指定切割每一行的字符串
    additional 遇到字典中已有的值,是追加频率还是覆盖频率
    annotation = '#' 如果启用注释,对#号开头的行,和频率字符串后面的#号都会进行删除
    """
    with open(file_name, 'r', encoding=type) as f_obj:
        result_dict = {}
        for line in f_obj.readlines():
            # 忽略#号开头的行
            if annotation and line.startswith(annotation):
                line = ''
            if line.strip() != "":
                # 如果规则存在频率选项 path [frequency==10]
                if separator in line.strip():
                    line_string = line.rsplit(separator, 1)[0].strip()
                    # 忽略frequency字符串后 #号开头的内容
                    line_frequency = line.rsplit(separator, 1)[-1].split(annotation, 1)[0].strip()
                    line_frequency = int(line_frequency)
                    # print(line_string,line_frequency)

                else:
                    line_string = line.strip()
                    line_frequency = 1
                # 如果字典已经存在就追加频率,否则直接赋值
                # 判断字典是否包含键,可以使用in，__contains__()
                # if result_dict.__contains__(line_string):
                if line_string in result_dict and additional == True:
                    line_frequency += result_dict[line_string]
                    result_dict[line_string] = line_frequency
                else:
                    result_dict[line_string] = line_frequency
        return result_dict


# 读取多个文件内容并返回结果字典 {"路径”:频率}
def read_many_file_to_dict_with_frequency(base_dir='.', list_dir_base_file=[], separator='frequency==', annotation='#',
                                          additional=True):  # 存储所有字典及其对应键值对
    # 存储所有字典及其对应键值对
    frequency_dict_ = {}
    # 实现多个文件的分步读取,但是频率叠加
    for file_name in list_dir_base_file:
        # 读取字典内容时,
        tmp_frequency_dict_ = read_file_to_dict_with_frequency(base_dir + '/' + file_name, separator=separator,
                                                               annotation=annotation, additional=additional)
        # print(tmp_frequency_dict_)
        # 叠加字典的频率
        for key in tmp_frequency_dict_.keys():
            if key not in frequency_dict_.keys():
                frequency_dict_[key] = tmp_frequency_dict_[key]
            else:
                frequency_dict_[key] = frequency_dict_[key] + tmp_frequency_dict_[key]
    return frequency_dict_


# 得到{"路径”:频率}字典中频率大于指定值的列表
def get_key_list_with_frequency(frequency_dict={}, frequency=1, frequency_max=99999):
    frequency_list = []
    for key, value in frequency_dict.items():
        if frequency <= value <= frequency_max:
            frequency_list.append(key)
    return frequency_list


########字典列表处理相关######################
# 读取字典文件列表、进行规则解析、进行基本变量替换
def read_list_file_to_dict_with_frequency_and_rule_parse_and_replace_base_var(module, dir_path='.',
                                                                              list_dir_file=[],
                                                                              replace_dict={},
                                                                              separator='frequency==',
                                                                              annotation='#',
                                                                              additional=True, frequency=1,
                                                                              logger=None):
    # 1、读取多个文件,并叠加频率参数
    # 2、取出其中符合频率规则的元素
    # 3、每个元素进行规则解析
    # 4、对每个元素进行规则替换
    # 5、返回替换后的规则列表

    # 读取直接文件目录下的所有字典
    frequency_dict_ = read_many_file_to_dict_with_frequency(dir_path, list_dir_file, separator=separator,
                                                            annotation=annotation, additional=additional)
    logger.debug("[*] 路径 {} 下所有字典文件 {} 内容读取结果: {} 条 详情: {}".format(dir_path, list_dir_file, len(frequency_dict_),
                                                                   frequency_dict_))

    # 提取符合频率的键
    frequency_list_ = get_key_list_with_frequency(frequency_dict_, frequency=frequency)
    logger.debug("[*] 路径 {} 下所有字典文件 {} 频率筛选结果: {} 条 详情: {}".format(dir_path, list_dir_file, len(frequency_list_),
                                                                   frequency_list_))

    # 对直接规则字典列表里的元素进行规则解析 # 每一行字典解析顺序-规则解析,基本变量替换,因变量替换
    logger.info("[*] {}字典 元素 {{XX=XXX:XXXXX}}$ 规则解析渲染开始...".format(module))
    frequency_list_, render_count, run_time = rule_list_base_render(frequency_list_, logger)
    logger.info("[+] {}字典 元素渲染完毕,剩余元素 {} 个,本次解析规则 {} 次, 耗时 {} 秒".format(module, len(frequency_list_), render_count, run_time))
    logger.debug("[*] {}字典 元素渲染后内容: {}".format(module, frequency_list_))

    # 对直接规则字典列表里的元素进行基本变量替换 # 每一行字典解析顺序-规则解析,基本变量替换,因变量替换
    logger.info("[*] {}字典 元素 {} 变量替换开始...".format(module, replace_dict.keys()))
    frequency_list_, replace_count, run_time = replace_list_has_key_str(frequency_list_, replace_dict)
    logger.info(
        "[+] {}字典 元素 {} 变量替换完毕,剩余元素 {} 个,本次替换 {} 次, 耗时 {} 秒".format(module, replace_dict.keys(), len(frequency_list_),
                                                                    replace_count, run_time))
    logger.debug("[*] {}字典 元素 {} 变量替换后内容: {}".format(module, replace_dict.keys(), frequency_list_))
    return frequency_list_


# 读取多个字典文件、进行规则解析、进行基本变量替换
def read_many_file_to_dict_with_frequency_and_rule_parse_and_replace_base_var(module, dir_path='.',
                                                                              dict_file_suffix='.lst',
                                                                              replace_dict={},
                                                                              separator='frequency==',
                                                                              annotation='#',
                                                                              additional=True,
                                                                              frequency=1,
                                                                              logger=None):
    # 0、获取目录下存在的文件名列表
    # 1、读取多个文件,并叠加频率参数
    # 2、取出其中符合频率规则的元素
    # 3、每个元素进行规则解析
    # 4、对每个元素进行规则替换
    # 5、返回替换后的规则列表

    # 获取字典目录下的所有文件名
    list_dir_file = get_relative_file_name(dir_path, dict_file_suffix)
    logger.info("[*] 路径 {} 下存在 {} 字典: {}".format(dir_path, module, list_dir_file))

    # 读取文件列表中的内容,并进行频率筛选
    frequency_list_ = read_list_file_to_dict_with_frequency_and_rule_parse_and_replace_base_var(module, dir_path=dir_path,
                                                                                                list_dir_file=list_dir_file,
                                                                                                replace_dict=replace_dict,
                                                                                                separator=separator,
                                                                                                annotation=annotation,
                                                                                                additional=additional,
                                                                                                frequency=frequency,
                                                                                                logger=logger)

    return frequency_list_


########字典合并相关######################
# 合并folders目录字典列表和files目录字典列表,返回结果和时间
def combine_folder_list_and_files_list(folder_list, files_list):
    # 记录开始替换的时间
    start_time = time.time()

    combin_folder_files_list = []
    folder_list = list(set(folder_list))
    files_list = list(set(files_list))
    for folders in folder_list:
        for files in files_list:
            folders = folders if folders.startswith('/') else '/' + folders
            files = files if files.startswith('/') else '/' + files
            combin_folder_files_list.append(folders.rsplit('/', 1)[0] + files)
    combin_folder_files_list = list(set(combin_folder_files_list))
    end_time = time.time()
    run_time = end_time - start_time
    return combin_folder_files_list, run_time


# 组合URL列表和动态路径列表
def combine_target_list_and_path_list(target_url_list, url_path_list):
    target_url_path_list = []
    for target in target_url_list:
        for url_path in url_path_list:
            url_path = url_path if url_path.startswith('/') else '/' + url_path
            target_url_path_list.append(target + url_path)
    target_url_path_list = list(set(target_url_path_list))
    return target_url_path_list


# 组合URL和目标和路径
def combine_one_target_and_path_list(target, path_list):
    url_path_list = []
    for url_path in path_list:
        url_path = url_path if url_path.startswith('/') else '/' + url_path
        url_path_list.append(target + url_path)
    url_path_list = list(set(url_path_list))
    return url_path_list


# 移除字典内没有值、或值为'()'的键
def remove_dict_none_value_key(dict_, bracket=True):
    """
    移除字典内没有值、或 值为'()'的键
    bracket 是否移除值为'()'括号的键
    """
    for key in list(dict_.keys()):
        if not dict_.get(key) or dict_.get(key) is None:
            del dict_[key]
        elif bracket and dict_.get(key) == '()':
            del dict_[key]
    return dict_


# 移除列表内包含未渲染字符串（%%domain%%d等）的目标
def remove_list_none_render_value(path_list, ALL_REPLACE_KEY, logger=None):
    """
    # 移除列表内包含未渲染字符串（%%domain%%d等）的目标
    # print(ALL_REPLACE_KEY) # {'%%domain%%': '(www\\.baidu\\.com|baidu\\.com|baidu)'}
    """
    for replace_str in ALL_REPLACE_KEY:
        if replace_str.startswith('%') and replace_str.endswith('%'):
            for index in range(0, len(path_list)):
                if replace_str in path_list[index]:
                    print_str = "[-] {} 中关键字[{}]没有被成功替换,正在剔除...".format(path_list[index], replace_str)
                    logger.error(print_str) if logger else print(print_str)
                    path_list[index] = ""
        else:
            print_str = "[-] 关键字[{}]没有遵循%key%或%%key%%命名规则...".format(replace_str)
            logger.error(print_str) if logger else print(print_str)

    path_list = [path for path in path_list if path != ""]
    return path_list


# 对列表中的元素进行中文判断和处理
def url_path_chinese_encode(path_list, logger, encode_list=['utf-8', 'gb2312']):
    """
    对列表中的元素进行中文判断和多个编码处理
    show_differ_path=True
    # new_path = urllib.parse.quote(path.encode("gb2312")) #解决/备份.zip读取问题失败
    # new_path = urllib.parse.quote(path.encode("utf-8")) #解决/备份.zip读取问题成功
    # new_path = urllib.parse.quote(path) #解决/备份.zip读取问题成功
    """
    zh_model = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
    new_path_list = []
    for path in path_list:
        new_path_list.append(path)
        match = zh_model.search(path)
        if match:
            new_path = None
            for encode in encode_list:
                try:
                    new_path = urllib.parse.quote(path.encode(encode))  # 解决/备份.zip读取问题失败
                    if path != new_path:
                        new_path_list.append(new_path)
                        logger.debug("[*] 中文编码模式: 路径列表中的元素[{}] 已基于 [{}] 编码 URL编码为:{}".format(path, encode, new_path))
                except Exception as error:
                    logger.error("[-] 中文编码模式: 路径列表中的元素[{}] 基于 [{}] 编码进行URL编码时,发生错误:{}".format(path, encode, error))
    new_path_list = list(set(new_path_list))
    return new_path_list


# 对列表中的所有元素进行URL编码
def url_path_url_encode(path_list, logger, encode_list=['utf-8', 'gb2312']):
    """
    # 对列表中的所有元素进行URL编码,
    # new_path = urllib.parse.quote(path.encode("gb2312")) #解决/备份.zip读取问题失败
    # new_path = urllib.parse.quote(path.encode("utf-8")) #解决/备份.zip读取问题成功
    # new_path = urllib.parse.quote(path) #解决/备份.zip读取问题成功
    """
    new_path_list = []
    for path in path_list:
        new_path_list.append(path)
        for encode in encode_list:
            try:
                new_path = urllib.parse.quote(path.encode(encode))  # 解决/备份.zip读取问题失败
                if path != new_path:
                    new_path_list.append(new_path)
                    logger.debug("[*] 全部编码模式: 路径列表中的元素 [{}] 已基于 [{}] 编码 URL编码为:{}".format(path, encode, new_path))
            except Exception as error:
                logger.error("[-] 全部编码模式: 路径列表中的元素 [{}] 基于 [{}] 编码进行URL编码时,发生错误:{}".format(path, encode, error))
    new_path_list = list(set(new_path_list))
    return new_path_list


# 获得随机字符串
def get_random_str(length=12, has_dot=True, with_slash=True, has_symbols=False):
    """
    # length 随机字符串长度
    # has_dot 是否随机字符串是否必须.字符,是的话就把倒数第四个字符替换为.
    # with_slash 最终返回结果是否要添加/开头
    # has_symbols 基本字符串是否包含特殊字符

    生成一个指定长度的随机字符串
    # 一种实现方式
    random_str =  ''.join(random.sample(base_str,length))
    # if must_has_dot:random_str[-4] = '.'  # 字符串不支持直接用下标访问

    # 另一种实现方式
    random_str = ''
    length = len(base_str) - 1
    for i in range(length):
        random_str += base_str[random.randint(0, length)]
    """
    if has_symbols:
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789~!@#$%^&*()_+-=><'
    else:
        base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    random_str = ''
    for i in range(0, length - 1):
        if has_dot and i == length - 5:
            random_str += '.'
        else:
            random_str += base_str[random.randint(0, len(base_str) - 1)]
    if with_slash:
        random_str = '/' + random_str
    return random_str

# 替换列表中所有元素的///为一个/
def replace_multi_slashes(list_):
    new_list_ =[]
    for str_ in list_:
        if '//' in str_:
            str_ = re.sub("/{1,}", '/', str_)
        new_list_.append(str_)
    new_list_ = list(set(new_list_))
    return new_list_


# 判断列表(元组1,元组2,元组3)对应位置的值是否相同
def three_tuple_index_value_equal(tuple_result_list, index):
    if tuple_result_list[0][index] == tuple_result_list[1][index] == tuple_result_list[2][index]:
        return True
    else:
        return False


# 判断列表(元组1,元组2)除开URL以外的位置值是否相同
def two_tuple_list_value_equal(tuple_result_list):
    list_tuple_1 = list(tuple_result_list[-1])
    list_tuple_2 = list(tuple_result_list[-2])
    if list_tuple_1[1:] == list_tuple_2[1:]:
        return True
    else:
        return False


# 判断列表的元素是否有在字符串内
def list_in_str(list=[], string=""):
    flag = False
    if list:
        for i in list:
            if i in string:
                flag = True
                break
    return flag


############URL解析处理相关###############
# 从URL中获取域名相关的单词列表
def get_domain_words(url, ignore_ip_format=True, sysbol_replace_dict={}, remove_not_path_symbol=True,
                     not_path_symbol=[':']):
    """
    从URL中获取域名相关的单词
    print(get_basedomain('http://www.baidu.com/xxx.aspx?p=123'))  # ['www.baidu.com', 'baidu.com', 'baidu']
    print(get_basedomain('http://www.baidu.com.cn:8080/xxx.aspx?p=123'))  # ['www.baidu.com.cn:8080', 'www.baidu.com.cn', 'baidu.com.cn', 'baidu']
    print(get_basedomain('http://1.1.1.1:8080/xxx.aspx?p=123'))  # ['1.1.1.1:8080', '1.1.1.1', '1.1.1.1']

    print(get_domain_words('http://www.baidu.com.cn:8080/xxx.aspx?p=123'))  # ['www.baidu.com.cn:8080', 'www.baidu.com.cn', 'baidu.com.cn', 'baidu']
    print(get_domain_words('http://1.1.1.1:8080/xxx.aspx?p=123'))  # ['1.1.1.1:8080', '1.1.1.1', '1.1.1.1']
    ['www.baidu.com.cn:8080', 'www.baidu.com.cn', 'www.baidu.com.cn_8080', 'baidu.com.cn', 'baidu']
    ['1.1.1.1:8080', '1.1.1.1', '1.1.1.1_8080', '1.1.1.1']
    """
    try:
        real_domain_val_list = []
        domain_val_1 = urlparse(url).netloc
        if ignore_ip_format:
            re_search_ip_result = re.search(
                r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])', domain_val_1)
            if re_search_ip_result:
                # 如果从域名中搜索到IP,就直接返回
                return real_domain_val_list

        # print(domain_val_1) # www.baidu.com.cn:8080
        domain_val_2 = extract(url).registered_domain
        # print(domain_val_2) # baidu.com.cn
        domain_val_3 = extract(url).domain
        # print(domain_val_3) #baidu
        tmp_domain_val_list = [domain_val_1, domain_val_2, domain_val_3]
        """
        # colon_to_other_list = ["_", "-"]
        colon_to_other_list = ["_"] #建议将变量移动到seting.py 要解决各个包之间相互导入的问题
        for domain_val in tmp_domain_val_list:
            if domain_val.strip() != '':
                real_domain_val_list.append(domain_val.strip())
            if ':' in domain_val:
                real_domain_val_list.append(domain_val.split(":")[0])
                for sysbol in colon_to_other_list:
                    real_domain_val_list.append(domain_val.replace(":",sysbol))
        """
        # 根据字典动态替换
        # sysbol_replace_dict = {":": ["_"],".": ["_"]}
        if sysbol_replace_dict:
            for domain_val in tmp_domain_val_list:
                if domain_val.strip() != '':
                    real_domain_val_list.append(domain_val.strip())
                    # 如果里面有冒号,需要再添加一边
                    if ':' in domain_val:
                        real_domain_val_list.append(domain_val.split(":")[0])

        # 对所有结果再进行一次替换和添加
        for domain_val in real_domain_val_list:
            for key, value in sysbol_replace_dict.items():
                for sysbol in value:
                    if key in domain_val:
                        real_domain_val_list.append(domain_val.replace(key, sysbol))

        real_domain_val_list = list(set(real_domain_val_list))


        # 如果开启删除非路径字符开关
        if remove_not_path_symbol:
            tmp_words_list = []
            for word in real_domain_val_list:
                if not list_in_str(not_path_symbol, word):
                    tmp_words_list.append(word)
            real_domain_val_list = tmp_words_list
        return real_domain_val_list
    except Exception as e:
        print("[*] Get_basedomain No Knowed Error:{}".format(str(e)))


# 获取URL的脚本语言后缀
def get_url_extion(url):
    parser_obj = UrlSplitParser(urlparse(url))
    extion = parser_obj.get_extion()
    return extion


# 获取URL目录单词和参数单词列表
def get_path_words(url, sysbol_replace_dict={}, remove_not_path_symbol=True,not_path_symbol=[':']):
    """
    # 获取URL目录单词和参数单词
    # UrlSplitParser(urlparse('http://www.baidu.com.cn:8080/xxxxx/xxx.aspx?p=123'))
    # print(parser_obj.get_paths()) # {'segment': ['/', '/xxxxx'], 'path': ['xxxxx', 'xxx']}

    UrlSplitParser中的其他方法
    #print(parser_obj.get_extion()) # aspx
    #print(parser_obj.get_urlfile()) # /xxxxx/xxx.aspx
    #print(parser_obj.get_dependent()) # ['p', 'xxx', 'baidu', 'www', '123', 'aspx', 'xxxxx']
    #print(parser_obj.get_domain_info()) # ['www', 'baidu', 'baidu'] ???
    """
    parser_obj = UrlSplitParser(urlparse(url))
    path_words_list = parser_obj.get_paths()['path']
    # 对所有结果再进行一次替换和添加
    for path_var in path_words_list:
        for key, value in sysbol_replace_dict.items():
            for sysbol in value:
                if key in path_var:
                    path_words_list.append(path_var.replace(key, sysbol))
    path_words_list = list(set(path_words_list))

    # 如果开启删除非路径字符开关
    if remove_not_path_symbol:
        tmp_words_list = []
        for word in path_words_list:
            if not list_in_str(not_path_symbol, word):
                tmp_words_list.append(word)
        real_domain_val_list = tmp_words_list
    return real_domain_val_list

    return path_words_list


# 从URL中提取无参数无目录的URL
def get_baseurl(link):
    """
    print(get_baseurl('http://www.baidu.com/xxx.aspx?p=123'))  # http://www.baidu.com
    print(get_baseurl('http://www.baidu.com.cn:8080/xxx.aspx?p=123'))  # http://www.baidu.com.cn:8080
    print(get_baseurl('http://1.1.1.1:8080/xxx.aspx?p=123'))  # http://1.1.1.1:8080
    """
    netloc = urlparse(link).netloc
    if netloc:
        split_url = link.split(netloc)
        baseurl = '%s%s' % (split_url[0], netloc)
        return baseurl


# 获取URL中的目录单词
def get_segments(url):
    """
    # 获取URL中的目录单词
    #UrlSplitParser(urlparse('http://www.baidu.com.cn:8080/xxxxx/xxx.aspx?p=123'))
    #print(parser_obj.get_paths()) # {'segment': ['/', '/xxxxx'], 'path': ['xxxxx', 'xxx']}
    """
    url_web_dirs = []
    parser_obj = UrlSplitParser(urlparse(url))

    for segment in parser_obj.get_paths()['segment']:
        url_web_dirs.append(parser_obj.baseurl + segment)
    return url_web_dirs


# 从URL中提取第一层目录
def get_first_segment(url):
    """
    # 从URL中提取第一层目录
    print(get_first_segment('http://www.baidu.com.cn:8080/111/222/3.aspx?p=123')) #/111/
    """
    path_obj = urlparse(url)
    path = path_obj.path.replace('//', '/')
    if len(path.split('/')) < 3:
        return '/'
        # return pathobj.scheme+'://'+pathobj.netloc+'/'
    else:
        segment = path.split('/')[1]
        return '/' + segment + '/'
        # return pathobj.scheme+'://'+pathobj.netloc+'/'+segment+'/'


# 从URL中获取HOST:PORT
def get_host_port(url):
    """
    从URL中获取HOST头部
    print(get_host_port('http://www.baidu.com.cn:8080/111/222/3.aspx?p=123')) #www.baidu.com.cn:8080
    """
    path_obj = urlparse(url)
    return path_obj.netloc


############命中结果写入相关###############
# 字典还原为规则格式

# # 将字符串转为不会被正则规则影响的正则字符串 #存在符号缺陷
def str_to_re(str_):
    # 将字符串转为不会被正则规则影响的正则字符串 #存在符号缺陷
    str_ = str_.replace('\\', '\\\\)').replace('.', '\\.').replace('$', '\\$').replace('^', '\\^')\
        .replace('*', '\\*').replace('+', '\\+').replace('?', '\\?').replace('[', '\\[').replace(']', '\\]') \
        .replace('{', '\\{').replace('}', '\\}').replace('|', '\\|')  .replace('(', '\\(').replace(')', '\\)')
    return str_

# # 将后缀字典列表转为一个正则替换规则字符串 #存在符号缺陷
def list_to_re_str(replace_list, bracket=True):
    # 将后缀字典列表转为一个正则替换规则字符串
    # 列表['.ccc','.bbb']转为一个正则替换字符串(\\.ccc|\\.bbb)
    # bracket=是否给正则结果添加括号
    regexp = ''
    if replace_list:
        for i in replace_list:
            regexp = regexp + str_to_re(i) + '|'
        regexp = regexp.strip(r"|")
    else:
        regexp = ""
    if bracket:
        replace_str = '({regexp})'.format(regexp=regexp)
    else:
        replace_str = '{regexp}'.format(regexp=regexp)
    return replace_str

# 将URL转换为原始规则
def url_to_raw_rule(url_list=[], BASE_VAR_REPLACE_DICT={}, DEPEND_VAR_REPLACE_DICT={}):
    result_add_dict = {"add_to_base": [], "add_to_direct": [], "add_to_combin_folders": [], "add_to_combin_files": []}

    for url_str in url_list:
        # 提取路径
        url_path = url_str.split(get_baseurl(url_str), 1)[-1]  # /config.inc.php
        # print(url_str,'提取路径', url_path)

        # 循环替换因变量值为%%键%%
        url_path_reverse_depend_var = url_path
        # print(DEPEND_VAR_REPLACE_DICT)
        for key, value in DEPEND_VAR_REPLACE_DICT.items():
            url_path_reverse_depend_var = re.sub(list_to_re_str(value), key, url_path, count=0)
        # print(url_str,'替换因变量值',url_path_reverse_depend_var)

        # 循环替换基础变量值为%键%
        url_path_reverse_base_var = url_path_reverse_depend_var
        # print(replace_dict)
        for key, value in BASE_VAR_REPLACE_DICT.items():
            url_path_reverse_base_var = re.sub(list_to_re_str(value), key, url_path_reverse_depend_var, count=0)
        # print(url_str,"替换基础变量值",url_path_reverse_base_var)

        # 提取URL中的后缀
        url_extion = get_url_extion(url_str)
        # print(url_str, url_extion)
        if url_extion:
            # 如果URL中确实存在后缀
            result_add_dict["add_to_base"].append(url_extion)  # 需要添加到hit_ext.lst这个文件中
            # 如果后缀没有被成功替换,那应该使用命中的ext进行替换
            url_path_reverse_base_var = re.sub(list_to_re_str(result_add_dict["add_to_base"]), "%hit_ext%",url_path_reverse_depend_var, count=0)
            # print(url_str, url_path_reverse_base_var)

        result_add_dict["add_to_direct"].append(url_path_reverse_base_var)
        result_add_dict["add_to_combin_folders"].append('/' + url_path_reverse_base_var.rsplit("/", 1)[0].rsplit("/", 1)[-1])
        result_add_dict["add_to_combin_files"].append('/' + url_path_reverse_base_var.rsplit("/", 1)[-1])

    return result_add_dict


# 将命中的结果写入到文件中
def write_hit_result_to_file_with_frequency(file_name, result_list, type='utf-8', separator='frequency==',
                                            additional=True):
    # result_dict
    result_dict = {}
    # 先读取文件内容
    if file_is_exist(file_name):
        result_dict = read_file_to_dict_with_frequency(file_name, type=type, separator=separator, additional=additional)

    # 遍历命中结果列表对结果列表进行添加
    for path in result_list:
        if path in result_dict:
            result_dict[path] = result_dict[path] + 1
        else:
            result_dict[path] = 1

    # 将结果字典写入文件
    with open(file_name, 'w+', encoding=type) as f_obj:
        for key, value in result_dict.items():
            f_obj.write("{path}     {separator}{frequency}\n".format(path=key, separator=separator, frequency=value))

# 自动解析命中结果,并将命中结果写入到文件中
def auto_analyse_hit_result_and_write_file(url_list, BASE_VAR_REPLACE_DICT, DEPEND_VAR_REPLACE_DICT, hit_ext_path,
                                           hit_direct_path, hit_folder_path, hit_files_path, logger):
    # 自动将命中结果写入到文件中

    result_add_dict = url_to_raw_rule(url_list, BASE_VAR_REPLACE_DICT, DEPEND_VAR_REPLACE_DICT)
    # 设置写入文件的路径
    # base_dir = '../dict/base_var'
    # dir_path = '../dict/direct_path'
    # dir_combin_folder = '../dict/combin_folder'
    # dir_combin_files = '../dict/combin_files'
    add_to_base = hit_ext_path
    add_to_direct = hit_direct_path
    add_to_combin_folders = hit_folder_path
    add_to_combin_files = hit_files_path

    for key, value in result_add_dict.items():
        if value:
            logger.info("[+] 正在往 {} 文件写入命中结果 {}".format(vars()[key], value))
            write_hit_result_to_file_with_frequency(vars()[key], value)
#######################################
