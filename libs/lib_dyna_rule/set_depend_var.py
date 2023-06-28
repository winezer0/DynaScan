#!/usr/bin/env python
# encoding: utf-8


# 从URL中获取域名相关的单词
import copy

from libs.lib_dyna_rule.dyna_rule_const import STR_VAR_PATH, STR_VAR_DOMAIN, STR_VAR_FILE_NAME, STR_VAR_PURE_NAME
from libs.lib_log_print.logger_printer import output, LOG_ERROR
from libs.lib_dyna_rule.dyna_rule_tools import dict_content_base_rule_render
from libs.lib_url_analysis.url_parser import parse_url_file_part
from libs.lib_url_analysis.url_tools import get_domain_words, get_path_words


# 获取 基于 HTTP 请求的 因变量
def set_dependent_var_dict(target_url,
                           base_dependent_dict,
                           ignore_ip_format=None,
                           symbol_replace_dict=None,
                           not_allowed_symbol=None):
    """
    获取 基于 HTTP 请求的 因变量
    STR_VAR_DOMAIN == %%DOMAIN%%  域名相关--较多
    STR_VAR_PATH == "%%PATH%%"  路径相关--备份文件中较多
    """
    dependent_var_dict = copy.copy(base_dependent_dict)

    # 基于URL获取因变量
    if not target_url:
        output(f"[-] 注意: 未输入目标URL参数,无法获取因变量", level=LOG_ERROR)
        dependent_var_dict[STR_VAR_DOMAIN] = None
        dependent_var_dict[STR_VAR_PATH] = None
        dependent_var_dict[STR_VAR_FILE_NAME] = None
        dependent_var_dict[STR_VAR_PURE_NAME] = None
    else:
        # 域名相关因变量
        domain_words = get_domain_words(target_url,
                                        ignore_ip_format=ignore_ip_format,
                                        symbol_replace_dict=symbol_replace_dict,
                                        not_allowed_symbol=not_allowed_symbol)
        dependent_var_dict[STR_VAR_DOMAIN] = domain_words

        # 路径相关因变量
        path_words = get_path_words(target_url,
                                    symbol_replace_dict=symbol_replace_dict,
                                    not_allowed_symbol=not_allowed_symbol)
        dependent_var_dict[STR_VAR_PATH] = path_words

        # 文件名相关变量
        file_name, pure_name = parse_url_file_part(target_url)
        dependent_var_dict[STR_VAR_FILE_NAME] = [file_name] if file_name else None
        dependent_var_dict[STR_VAR_PURE_NAME] = [pure_name] if pure_name else None

    # 对 内容列表 中的规则进行 进行 动态解析
    dependent_var_dict = dict_content_base_rule_render(dependent_var_dict)
    return dependent_var_dict
