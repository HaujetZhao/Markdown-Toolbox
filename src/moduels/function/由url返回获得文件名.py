import os, re
from http.cookiejar import MozillaCookieJar
from urllib import request, error
import urllib.error
from urllib.parse import urlparse
from shutil import copy, move, rmtree

from moduels.component.NormalValue import 常量


def 由url返回获得文件名(url, 返回):
    print(f'要询问文件名的 url：{url}')
    try:
        页面返回类型 = 返回.getheader('content-type')
        if 'text/html' in 页面返回类型:
            return False
        内容布置 = 返回.getheader('Content-Disposition')
    except:
        return False
    print(f'内容布置：{内容布置}')
    if 内容布置 != None:
        文件名 = re.search('(filename=")(.+?)(";)', 内容布置).group(2)
        print('从 Content - Disposition 得到文件名')
    elif 返回.geturl() != url:
        重导向的url = 返回.geturl()
        重导向后解析结果 = urlparse(重导向的url)
        文件名 = os.path.basename(重导向后解析结果.path)
        prin('从重导向的 url 获得文件名')
    else:
        try:
            文件名 = os.path.basename(urlparse(url).path)
            print('从原始 url 获得文件名')
        except:
            print(f'没能获得文件名，url：{url}')
            return False
    print(f'文件名：{文件名}')
    if 文件名 != '':
        return 文件名
    else:
        return False