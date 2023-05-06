#!/usr/bin/env python
# encoding: utf-8

import datetime
import re
import string
import sys
import time

import exrex
import sre_yield

from libs.lib_log_print.logger_printer import output, LOG_ERROR

sys.dont_write_bytecode = True  # 设置不生成pyc文件


# 规则解释器，四种模式：date/int/str/re
class RuleParser(object):
    """
    docstring for RuleParser
    字典可配置规则解析器
    {类型=名称#长度$step:开始-结束}
    """

    def __init__(self, dict_str):
        super(RuleParser, self).__init__()
        self.dict_str = dict_str

    def parse(self):
        if self.get_reg_rule():
            parse_result = []
            start_str = self.get_start_str()
            end_str = self.get_end_str()
            # output("dict_str:",self.dict_str,"start_str:",start_str,"end_str:", end_str,"rule:",self.get_reg_rule())
            dic_result = self.generate_dic(self.get_reg_rule())
            for line in dic_result:
                parse_result.append('%s%s%s' % (start_str, line, end_str))
            return parse_result
        else:
            return ''

    def get_reg_rule(self):
        # 获取字典生成规则
        reg_str = re.compile(r'(\{date|\{int|\{re|\{str).+\}\$')
        result = reg_str.search(self.dict_str)
        if result:
            # 判断是否有分隔符存在,是否正常规则
            if ':' in result.group() and result.group().startswith('{') and result.group().endswith('}$'):
                return result.group()[1:][:-2]
            else:
                return ''

    def generate_dic(self, myrule):
        """
                分离规则，获取条件和参数
                rule_name : 规则类型 ['DATE','INT','STR']
                rule_type : 规则子分类
                option_start : 起始字符
                option_end : 结束字符
        """
        # re=exrex:(201[7-9]{1}[0-1]{1}[0-9]{1})(\.rar|\.zip|\.gz|\.tar|\.tgz|\.tar\.gz|\.7z|\.z|\.bz2|\.tar\.bz2|\.iso|\.cab)
        # re=exrex:/(www\.baidu\.com\.cn:8080|www\.baidu\.com\.cn|baidu\.com\.cn|baidu)!
        # rules, options = myrule.split() # 如果myrule内有冒号会报错的 # ValueError: too many values to unpack (expected 2)
        rules, options = myrule.split(':', 1)
        rule_name, rule_type = rules.split('=')

        # 解析规则类型
        # 日期、整数、字符
        if rule_name == 'date':  # 处理日期

            """
                    日期会出现的子分类情况，初始位数补充0911,911
                    年(YEAR) 2005-2015
                    月(MON) 1-12
                    日(DAY) 0-30 !!! 这种情况几乎不存在
                    年月(YEAR_MON) 200501-201512
                    月日(MON_DAY) 0101-1231
                    年月日(YEAR_MON_DAY) 20050101-20151231
                    月日年(MON_DAY_YEAR) 01012005-12312015
            """

            if rule_type == 'year':  # 返回指定年份列表
                result = []
                option_from, option_to = options.split('-')
                if len(option_from) == 4 and len(option_to) == 4:
                    for year in range(int(option_from), int(option_to) + 1):
                        result.append(str(year))
                        result.append(str(year)[-2:4])
                return result
            elif rule_type == 'mon':  # 返回指定月份列表
                result = []
                option_from, option_to = options.split('-')
                if len(option_from) <= 2 and len(option_to) <= 2:
                    for month in range(int(option_from), int(option_to) + 1):
                        result.append(str(month))
                        if len(str(month)) == 1:
                            result.append('0' + str(month))
                return result
            elif rule_type == 'day':  # 返回日期列表 !!! 这种情况几乎不存在
                result = []
                option_from, option_to = options.split('-')
                if len(option_from) <= 2 and len(option_to) <= 2:
                    for day in range(int(option_from), int(option_to) + 1):
                        result.append(str(day))
                        if len(str(day)) == 1:
                            result.append('0' + str(day))
                return result
            elif rule_type == 'year_mon':  # 年月
                result = []
                option_from, option_to = options.split('-')
                if len(option_from) == 6 and len(option_to) == 6:
                    from_year = option_from[0:4]
                    from_mon = option_from[4:6]
                    to_year = option_to[0:4]
                    to_mon = option_to[4:6]
                    for year in range(int(from_year), int(to_year) + 1):
                        for month in range(int(from_mon), int(to_mon) + 1):
                            if len(str(month)) == 1:
                                result.append(str(year) + '0' + str(month))
                            result.append(str(year) + str(month))
                return result
            elif rule_type == 'mon_day':  # 月日，采用库函数
                result = []
                today = datetime.date.today()
                this_year = today.year
                option_from, option_to = options.split('-')
                if len(option_from) == 4 and len(option_to) == 4:
                    from_mon = option_from[0:2]
                    from_day = option_from[2:4]
                    to_mon = option_to[0:2]
                    to_day = option_to[2:4]
                    from_date = datetime.date(int(this_year), int(
                        from_mon), int(from_day))
                    to_date = datetime.date(int(this_year), int(to_mon), int(to_day))
                    total_days = to_date - from_date
                    for day in range(total_days.days):
                        day += 1
                        concat_date = from_date + datetime.timedelta(days=day)
                        result.append(concat_date.strftime('%m-%d'))
                        result.append(concat_date.strftime('%m%d'))  # 保留前置零
                if result:
                    result = list(set(result))
                return result
            elif rule_type == 'year_mon_day':  # 年月日
                result = []
                option_from, option_to = options.split('-')
                if len(option_from) == 8 and len(option_to) == 8:
                    from_year = option_from[0:4]
                    from_mon = option_from[4:6]
                    from_day = option_from[6:8]
                    to_year = option_to[0:4]
                    to_mon = option_to[4:6]
                    to_day = option_to[6:8]
                    from_date = datetime.date(int(from_year), int(
                        from_mon), int(from_day))
                    to_date = datetime.date(int(to_year), int(to_mon), int(to_day))
                    total_days = to_date - from_date
                    for day in range(total_days.days):
                        day += 1
                        concat_date = from_date + datetime.timedelta(days=day)
                        result.append(concat_date.strftime('%y-%m-%d'))
                        result.append(concat_date.strftime('%Y-%m-%d'))
                        result.append(concat_date.strftime('%y%m%d'))  # 保留前置零
                        result.append(concat_date.strftime('%Y%m%d'))  # 保留前置零
                if result:
                    result = list(set(result))
                return result
            elif rule_type == 'mon_day_year':  # 月日年
                result = []
                option_from, option_to = options.split('-')
                if len(option_from) == 8 and len(option_to) == 8:
                    from_year = option_from[4:8]
                    from_mon = option_from[0:2]
                    from_day = option_from[2:4]
                    to_year = option_to[4:8]
                    to_mon = option_to[0:2]
                    to_day = option_to[2:4]
                    from_date = datetime.date(int(from_year), int(from_mon), int(from_day))
                    to_date = datetime.date(int(to_year), int(to_mon), int(to_day))
                    total_days = to_date - from_date
                    for day in range(total_days.days):
                        day += 1
                        concat_date = from_date + datetime.timedelta(days=day)
                        result.append(concat_date.strftime('%y-%m-%d'))
                        result.append(concat_date.strftime('%Y-%m-%d'))
                        result.append(concat_date.strftime('%y%m%d'))  # 保留前置零
                        result.append(concat_date.strftime('%Y%m%d'))  # 保留前置零
                if result:
                    result = list(set(result))
                return result

        elif rule_name == 'int':  # 处理整数
            if rule_type.startswith('series'):  # 正常按照顺序递进，单步处理step
                result = []
                option_from, option_to = options.split('-')
                step_reg = re.compile(r'\$\d+')
                if step_reg.search(rule_type):  # 存在步长选项
                    step = step_reg.search(rule_type).group().lstrip('$')
                    for i in range(int(option_from), int(option_to) + 1, int(step)):
                        result.append(i)
                else:  # 没有步长选项，默认为1
                    for i in range(int(option_from), int(option_to) + 1):
                        result.append(i)
                return result
            elif rule_type.startswith('digits'):  # 连号数字，硬编码写入键盘连续位
                result = []
                option_from, option_to = options.split('-')
                length_reg = re.compile(r'\#\d+')
                if length_reg.search(rule_type):  # 存在长度选项
                    length = length_reg.search(rule_type).group().lstrip('#')
                    length = int(length)
                    for i in range(int(option_from), int(option_to) + 2 - length):
                        concat_char = []
                        for value in range(length):
                            concat_char.append(str(i + value))
                        result.append(''.join(concat_char))
                        result.append(''.join(concat_char)[::-1])  # 倒序
                return result
            elif rule_type.startswith('overlap'):  # 重叠数字
                result = []
                option_from, option_to = options.split('-')
                length_reg = re.compile(r'\#\d+')
                if length_reg.search(rule_type):  # 存在长度选项
                    length = length_reg.search(rule_type).group().lstrip('#')
                    for i in range(int(option_from), int(option_to) + 1):
                        result.append(str(i) * int(length))
                return result

        elif rule_name == 'str':  # 处理字符
            if rule_type.startswith('letters'):  # 正常按照顺序递进，单步处理step
                result = []
                option_from, option_to = options.split('-')
                length_reg = re.compile(r'\#\d+')
                if length_reg.search(rule_type):  # 存在长度选项
                    length = length_reg.search(rule_type).group().lstrip('#')
                    length = int(length)
                    # 字母的临界值 (z-length) (Z-length)
                    """
						小于91，都是大写
						a(97) - z(122)
						A(65) - Z(90)
						大于91，都是小写
					"""
                    if ord(option_from) > 96 and ord(option_to) > 96:  # 都是小写
                        str_from_id = string.ascii_letters.index(option_from)
                        str_to_id = string.ascii_letters.index(option_to)
                    elif ord(option_from) < 91 and ord(option_to) < 91:  # 都是大写
                        str_from_id = string.letters.index(option_from)
                        str_to_id = string.letters.index(option_to)
                    elif ord(option_from) > 91 and ord(option_to) < 96:  # 开始小写，结束大写
                        str_from_id = string.letters.index(option_from)
                        str_to_id = string.letters.index(option_to)
                    else:
                        pass  # print '规则错误'
                    for i in range(str_from_id, str_to_id - length + 2):  # 平衡range分配id从0开始
                        concat_char = []
                        for value in range(length):
                            concat_char.append(string.ascii_letters[i + value])
                        result.append(''.join(concat_char))
                        # result.append(''.join(concat_char)[::-1]) # 结果倒序
                return result

            if rule_type.startswith('overlap'):  # 重叠字母
                result = []
                option_from, option_to = options.split('-')
                if ord(option_from) > 96 and ord(option_to) > 96:  # 都是小写
                    str_from_id = string.ascii_letters.index(option_from)
                    str_to_id = string.ascii_letters.index(option_to)
                elif ord(option_from) < 91 and ord(option_to) < 91:  # 都是大写
                    str_from_id = string.ascii_letters.index(option_from)
                    str_to_id = string.ascii_letters.index(option_to)
                elif ord(option_from) > 91 and ord(option_to) < 96:  # 开始小写，结束大写
                    str_from_id = string.ascii_letters.index(option_from)
                    str_to_id = string.ascii_letters.index(option_to)
                else:
                    pass  # print '规则错误'
                length_reg = re.compile(r'\#\d+')
                if length_reg.search(rule_type):  # 存在长度选项
                    length = length_reg.search(rule_type).group().lstrip('#')
                    length = int(length)
                    for letter in string.ascii_letters[str_from_id:str_to_id + 1]:
                        result.append(letter * length)
                return result

        elif rule_name == 're':  # 自定义正则解析器
            """
            已知的正则解析生成器有 exrex、sre_yield
            """
            if rule_type.startswith('exrex'):  # exrex 引擎
                result = list(exrex.generate(options))
                return result
            if rule_type.startswith('sre_yield'):  # sre_yield 引擎
                result = list(sre_yield.AllStrings(options))
                return result
            else:
                pass

    def get_start_str(self):
        # 获取字典起始字符串
        start_str = re.compile(r'^.+(\{date|\{int|\{re|\{str)')
        result = start_str.search(self.dict_str)
        if result:
            return re.sub('(\{date|\{int|\{re|\{str)', '', result.group())
        else:
            return ''

    def get_end_str(self):
        # 获取字典结束字符串
        end_str = re.compile(r'(\}\$).+')
        result = end_str.search(self.dict_str)
        if result:
            return result.group().replace('}$', '')
        else:
            return ''


# 解析列表中包含规则的字符串,返回一个列表文件
def base_rule_render_list(rule_list):
    """
    # 解析列表中包含规则的字符串,返回一个列表文件
    """
    # 记录开始替换的时间
    start_time = time.time()

    # 对每次渲染进行一次计数
    render_count = 0

    result_list = []
    for rule_line in rule_list:
        # 直接判断规则应该有的多个元素同时在列表内   # issubset 用于判断一个集合是否是另一个集合的子集。
        if {'{', '=', ':', '}', '$'}.issubset(set(list(rule_line))):
            # 如果行内存在合法的解析规则
            parser = RuleParser(rule_line)
            rule = parser.get_reg_rule()
            if rule:
                try:
                    # 尝试解析规则
                    rules, options = rule.split(':')
                    rule_name, rule_type = rules.split('=')
                except Exception as error:
                    if 'too many values to unpack' in str(error):
                        output(f"[-] 规则 {rule_line} 发生编写错误,每条规则仅支持单个格式规则!!!", level=LOG_ERROR)
                    else:
                        output(f"[-] 规则 {rule_line} 发生未知解析错误!!! Error: {error}", level=LOG_ERROR)
                else:
                    # 实际解析规则返回结果
                    parser_result = parser.parse()
                    result_list.extend(parser_result)
                    render_count = render_count + 1
            else:
                output(f"[!] 字典 {rule_line} 疑似解析规则,可能存在编写错误...", level=LOG_ERROR)
                result_list.append(rule_line)
        else:
            # 不进行渲染
            result_list.append(rule_line)

    if result_list:
        result_list = list(set(result_list))
    end_time = time.time()
    run_time = end_time - start_time
    return result_list, render_count, run_time


if __name__ == '__main__':
    ##########RuleParser
    # result = RuleParser('{date=year:2017-2018}$').parse() #['2017', '17', '2018', '18']
    # result = RuleParser('{date=mon:9-10}$').parse() #['9', '09', '10']
    # result = RuleParser('{date=day:12-15}$').parse() #['12', '13', '14', '15']
    # result = RuleParser('{date=day:9-10}$').parse() #['9', '09', '10']

    # result = RuleParser('{date=year_mon:201709-201712}$').parse() #['201709', '20179', '201710', '201711', '201712']
    # result = RuleParser('{date=mon_day:0928-1003}$').parse() #['0930', '1001', '0929', '09-29', '1003', '10-01', '09-30', '10-02', '10-03', '1002']

    # result = RuleParser('{date=year_mon_day:20170111-20170112}$').parse()  #['170112', '20170112', '17-01-12', '2017-01-12']

    # result = RuleParser('{date=mon_day_year:01112017-01122017}$').parse() #['2017-01-12', '17-01-12', '170112', '20170112']

    # result = RuleParser('{int=series:1-5}$').parse() #['1', '2', '3', '4', '5']
    # result = RuleParser('{int=series$2:1-15}$').parse()  #    ['1', '3', '5', '7', '9', '11', '13', '15']
    # result = RuleParser('{int=digits#3:1-5}$').parse() #['123', '321', '234', '432', '345', '543']
    # result = RuleParser('{int=overlap#3:1-9}$').parse() #['111', '222', '333', '444', '555', '666', '777', '888', '999']
    # result = RuleParser('{int=overlap#3:11-22}$').parse() #['111111', '121212', '131313', '141414', '151515', '161616', '171717', '181818', '191919', '202020', '212121', '222222']

    # result = RuleParser('{str=letters#3:a-d}$').parse() #['abc', 'bcd']
    # result = RuleParser('{str=overlap#3:A-D}$').parse() #['AAA', 'BBB', 'CCC', 'DDD']

    # result = RuleParser('{re=exrex:(201[7-9]{1}[1]{1}[8-9]{1})}$').parse() #['201718', '201719', '201818', '201819', '201918', '201919']
    # result = RuleParser('{re=sre_yield:(201[7-9]{1}[1]{1}[8-9]{1})}$').parse()
    # ['201718', '201818', '201918', '201719', '201819', '201919']

    # result = RuleParser('{re=exrex:(''|admin/|exec/)}$').parse() # ['', 'admin/', 'exec/']
    result = RuleParser(
        '/{re=exrex:(|v[1-3]|v1\.[0-9]|v[2-3]\.[0-5]|api|api/v[1-3]|api/v1\.[0-9]|api/v[2-3]\.[0-5])}$/agent/self').parse()  # ['', 'admin/', 'exec/']

    output(result)

    ##########base_rule_render_list
    # rule_list = ['.{re=exrex:(zip|rar|asp)}$','.re={exrex:(zip|rar|asp)}$','.aspx']
    # result_list,render_count,run_time = base_rule_render_list(rule_list)
    # output(len(result_list),render_count,run_time)
    # output(result_list)
