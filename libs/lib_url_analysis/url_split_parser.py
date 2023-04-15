#!/usr/bin/env python
# encoding: utf-8

# URL处理对象
import sys

from tldextract import extract

sys.dont_write_bytecode = True  # 设置不生成pyc文件
sys.path.append("../../")


class UrlSplitParser(object):
    # 碎片化信息处理并集，生成其因变量组 [dependents]

    def __init__(self, url_obj, extension=None):
        super(UrlSplitParser, self).__init__()
        self.url = url_obj.geturl()
        self.scheme = url_obj.scheme
        self.netloc = url_obj.netloc
        self.path = url_obj.path
        self.paths = self.split_path()
        self.query = url_obj.query
        self.fragment = url_obj.fragment
        self.domain = extract(url_obj.netloc).domain
        self.root_domain = extract(url_obj.netloc).registered_domain
        self.subdomain = extract(url_obj.netloc).subdomain.split('.')
        self.domain_info = self.get_domain_info()
        self.extension = extension
        self.file_ext = self.get_extension()
        self.urlfile = self.get_urlfile()
        self.baseurl = self.scheme + '://' + self.netloc
        self.dependent = self.get_dependent()

    def parse(self):
        urlsplit = {'url': self.url,
                    'scheme': self.scheme,
                    'netloc': self.netloc,
                    'query': self.split_query(),
                    'path': self.split_path(),
                    'extension': self.get_extension(),
                    'fragment': self.fragment}
        return urlsplit

    def split_query(self):
        query = {}
        condition = self.query.split('&')
        if len(condition) >= 1:
            for line in condition:
                line_split = line.split('=')
                if len(line_split) > 1:
                    query[line_split[0]] = line_split[1]
                else:
                    query[line_split[0]] = ''
            return query
        else:
            return ''

    def split_path(self):
        path = []
        for dirs in self.path.split('/'):
            if dirs != '': path.append(dirs)
        return path

    def split_fragment(self):
        fragment = []
        for frags in self.fragment.split('='):
            if frags != '':
                fragment.append(frags)
        return fragment

    def get_domain_info(self):
        # 扩充域名信息节点
        domain = self.domain
        subdomain = self.subdomain
        subdomain.append(domain)
        if '' in subdomain:
            subdomain.remove('')
        return subdomain

    def get_dependent(self):
        # 生成其因变量组
        dependent = []
        dependent.extend(self.split_query().keys())
        dependent.extend(self.split_query().values())
        dependent.extend(self.split_fragment())
        dependent.extend(self.get_paths()['path'])
        dependent.extend(self.domain_info)
        dependent.append(self.file_ext)
        if dependent:
            dependent = list(set(dependent))
        if '' in dependent:
            dependent.remove('')
        return dependent

    def get_extension(self):
        path = self.split_path()
        if len(path) >= 1:
            filename = path[-1].split('.')
            if len(filename) > 1:
                return filename[-1]
            else:
                return self.extension
        else:
            return self.extension

    def get_urlfile(self):
        # 初始化脚本文件
        urlfile = self.path
        if self.get_extension():
            file_ext = self.get_extension()
            if urlfile == '/':
                urlfile = urlfile + 'index.' + file_ext
            elif urlfile == '':
                urlfile = urlfile + '/index.' + file_ext
            elif not urlfile.endswith(file_ext):
                urlfile = urlfile + '.' + file_ext
        return urlfile

    def get_paths(self):
        paths = []
        segments = ['/']
        fullpath = ''
        if self.path.endswith('/'):
            for path_line in self.paths:
                paths.append(path_line)
                fullpath += '/' + path_line
                segments.append(fullpath)
        else:
            for path_line in self.paths:
                if path_line == self.paths[-1]:
                    if '.' in path_line:  # 最后一个是文件，判断是否存在扩展名
                        right_strip_path = str(path_line).replace(('.' + self.file_ext), '')
                        paths.append(right_strip_path)
                    else:
                        paths.append(path_line)
                else:
                    paths.append(path_line)
                    fullpath += '/' + path_line
                    segments.append(fullpath)

        return {'segment': segments, 'path': paths}
