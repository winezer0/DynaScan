import inspect


def update_global_vars(startswith="GB_", require_blank=True, debug=False):
    # 修改所有全局变量名的值为变量名字符串
    # 当前本函数必须放置到本目录内才行

    def get_var_string(variable):
        # 自动根据输入的变量,获取变量名的字符串
        # 获取全局变量字典
        global_vars = globals()

        # 遍历全局变量字典
        for name, value in global_vars.items():
            if value is variable:
                # print(f"[*] global_vars <--> {variable} <--> {name} <--> {value}")
                return name

        # 获取局部变量字典
        local_vars = locals()
        # 遍历局部变量字典
        for name, value in local_vars.items():
            if value is variable:
                # print(f"[*] local_vars <--> {variable} <--> {name} <--> {value}")
                return name

        return None  # 如果未找到对应的变量名，则返回 None

    def get_global_var_names():
        # 获取本文件所有全局变量名称, 排除函数名等
        global_var_names = list(globals().keys())
        # 获取当前文件中定义的所有函数列表
        current_module = inspect.getmodule(inspect.currentframe())
        functions = inspect.getmembers(current_module, inspect.isfunction)
        function_names = [f[0] for f in functions]
        # 在本文件所有全局变量排除函数列表
        global_var_names = [name for name in global_var_names
                            if name not in function_names  # 排除内置函数名
                            and name.count("__") < 2  # 排除内置__name__等变量
                            and name != "inspect"  # 排除内置inspect包的变量
                            ]

        # 仅处理以 startswith 开头的变量
        if startswith:
            global_var_names = [name for name in global_var_names if name.startswith(startswith)]

        return global_var_names

    for variable_name in get_global_var_names():
        # 仅处理空变量
        if require_blank and globals()[variable_name]:
            if debug:
                print(f"跳过 Name:{variable_name} <--> Value: {globals()[variable_name]}")
            continue

        globals()[variable_name] = "NONE"
        globals()[variable_name] = get_var_string(globals()[variable_name])
        if debug:
            print(f"更新 Name:{variable_name} <--> Value: {globals()[variable_name]}")


######################################################
# 默认参数相关
GB_BASE_DIR = ""
GB_RUN_TIME = ""
GB_VERSION = ""
GB_DEBUG_FLAG = ""

# 日志路径相关
GB_LOG_INFO_FILE = ""
GB_LOG_DEBUG_FILE = ""
GB_LOG_ERROR_FILE = ""

GB_ACCESS_OK_FILE = ""
GB_ACCESS_NO_FILE = ""
######################################################
GB_EXCLUDE_HISTORY = ""  # 排除历史URLs文件
GB_HISTORY_FORMAT = ""  # 自动生成的历史URLs文件路径
GB_EXCLUDE_URLS = ""  # 自定义的历史URLs文件路径,用于联动其他工具

GB_RESULT_DIR = ""

# 输入参数相关
GB_TARGET = ""

GB_MAX_URL_NUM = ""
GB_MAX_ERROR_NUM = ""

# 命中结果动态排除开关
GB_HIT_INFO_EXCLUDE = ""

# HTTP请求相关
GB_DEFAULT_PROTO = ""

GB_PROXIES = ""
GB_THREADS_COUNT = ""
GB_TASK_CHUNK_SIZE = ""

GB_REQ_METHOD = ""
GB_REQ_BODY = ""

GB_REQ_HEADERS = ""
GB_RANDOM_UA = ""
GB_RANDOM_XFF = ""
GB_DYNA_REQ_HOST = ""
GB_DYNA_REQ_REFER = ""

GB_STREAM_MODE = ""
GB_URL_ACCESS_TEST = ""

GB_SPLIT_TARGET = ""
GB_EXCLUDE_STATUS = ""
GB_EXCLUDE_REGEXP = ""

GB_THREAD_SLEEP = ""
GB_SSL_VERIFY = ""
GB_ALLOW_REDIRECTS = ""

# 扫描字典相关
GB_DICT_RULE_SCAN = ""
GB_DICT_RULE_PATH = ""
GB_FREQUENCY_MIN = ""
GB_FREQUENCY_SYMBOL = ""

GB_DICT_SUFFIX = ""
GB_ONLY_SCAN_SPECIFY_EXT = ""
GB_NO_SCAN_SPECIFY_EXT = ""
GB_CUSTOM_URL_PREFIX = ""
GB_REMOVE_END_SYMBOLS = ""

GB_TIME_OUT = ""
GB_RETRY_TIMES = ""

# 其他常量
STR_BASE_PATH = "base_path"
STR_BASE_ROOT = "base_root"

# 未整理常量
GB_BASE_VAR_DIR = ""
GB_BASE_REPLACE_DICT = ""
GB_DEPENDENT_REPLACE_DICT = ""

GB_ANNOTATION_SYMBOL = ""

GB_BASE_PATH_STR = ""
GB_BASE_ROOT_STR = ""
GB_SCAN_BASE_PATH = ""
GB_SCAN_BASE_ROOT = ""
GB_ANNOTATION_SYMBOL = ""

GB_SYMBOL_REPLACE_DICT = ""
GB_NOT_ALLOW_SYMBOL = ""
GB_IGNORE_IP_FORMAT = ""

GB_REMOVE_MULTI_SLASHES = ""

GB_URL_PATH_LOWERCASE = ""
GB_CHINESE_ENCODE = ""
GB_ONLY_ENCODE_CHINESE = ""
######################################################
# 命中结果保存
GB_SAVE_HIT_RESULT = ""
GB_HIT_OVER_CALC = ""
GB_HIT_EXT_FILE = ""
GB_HIT_PATH_FILE = ""
GB_HIT_DIR_FILE = ""
GB_HIT_FILE_FILE = ""
######################################################
# 自动更新变量的值为变量名字符串 # 必须放在末尾
update_global_vars(startswith="GB_", require_blank=True, debug=False)
