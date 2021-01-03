import os, re
from http.cookiejar import MozillaCookieJar
from urllib import request, error
import urllib.error
from urllib.parse import urlparse
from shutil import copy, move, rmtree

from moduels.component.NormalValue import 常量


def 由url返回获得文件名(url, 返回):
    print(f'要询问文件名的 url：{url}')

    # 如果是 html 就放弃下载
    内容类型 = 返回.headers['content-type']
    if 'text/html' in 内容类型:
        print(f'该链接导向的是一个 text/html 网页，放弃下载：{url}')
        return False

    # 从 content-disposition 得到文件名
    if 'content-disposition' in 返回.headers:
        内容布置 = 返回.headers['content-disposition']
        print(f'content-disposition：{内容布置}')
        文件名 = re.search('(filename=")(.+?)(";)', 内容布置).group(2)
        print(f'从 Content - Disposition 得到文件名: {文件名}')

    # 页面重导向，从新 url 获得文件名
    elif 返回.url != url:
        重导向的url = 返回.url
        文件名 = 从url得到文件名(重导向的url)
        prin(f'从重导向的 url 获得文件名: {文件名}')

    # 从 url 解析获得文件名
    else:
        文件名 = 从url得到文件名(url, 内容类型)
        if os.path.splitext(文件名)[1] == '':
            文件名 = 从返回类型为文件名补齐后缀(文件名, 内容类型)
    print(f'文件名：{文件名}')

    if 文件名 != '':
        return 文件名
    else:
        return False

def 从url得到文件名(url, 内容类型=None):
    文件名 = os.path.basename(urlparse(url).path)
    if os.path.splitext(文件名)[1] == '' and 内容类型 != None:
        文件名 = 从返回类型为文件名补齐后缀(文件名, 内容类型)
    return 文件名

def 从返回类型为文件名补齐后缀(文件名, 内容类型):
    if 'image/jpeg' in 内容类型:
        文件名 += '.jpg'
    elif 'image/png' in 内容类型:
        文件名 += '.png'
    elif 'image/svg' in 内容类型:
        文件名 += '.svg'
    return 文件名