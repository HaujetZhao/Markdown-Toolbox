import os, re, time, _io, socket
from http.cookiejar import MozillaCookieJar
from urllib import request, error
import urllib.error
from urllib.parse import urlparse
from shutil import copy, move, rmtree

from moduels.component.NormalValue import 常量, 离线化线程常量

from moduels.function.getHumanReadableFileSize import 得到便于阅读的文件大小
from moduels.function.getFileNameFromUrl import 由url返回获得文件名
from moduels.function.processHeaders import 处理Headers

from PySide2.QtWidgets import *




def 下载链接文件(附件链接, 目标文件夹路径, cookie路径, 提醒是否要覆盖的信号, 进程, 获取进程状态的常量):  # 0 是询问，1 是全部覆盖，2 是全部跳过
    if urlparse(附件链接).netloc in 离线化线程常量.黑名单域名列表:
        print(f'该网址的域名已认为暂时不可访问 {附件链接}')
        return False
    cookie = MozillaCookieJar()
    if os.path.exists(cookie路径):
        cookie.load(cookie路径, ignore_discard=True, ignore_expires=True)
    网络请求器 = request.build_opener(request.HTTPCookieProcessor(cookie))
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4272.0 Safari/537.36 Edg/87.0.654.0"}
    HEADERS = 处理Headers(HEADERS, 附件链接)  # 有的网站可能需要在 Header 中加入 referencer
    try:
        print(f'开始请求网址，查看其类型 {附件链接}')
        返回 = 网络请求器.open(request.Request(附件链接, headers=HEADERS, method='HEAD'), timeout=1)  # 先看看是不是网页
        页面返回类型 = 返回.getheader('content-type')
        print(f'得到网页类型 {页面返回类型}')
        if 'text/html' in 页面返回类型:
            return False
    except urllib.error.URLError as error:
        if 'timed out' in error.__str__():
            print(f'访问超时，认为此网址因网络因素暂时不可访问，故跳过 {附件链接}')
            离线化线程常量.黑名单域名列表.append(urlparse(附件链接).netloc)
            return False
    except socket.timeout as error:
        if 'timed out' in error.__str__():
            print(f'访问超时，认为此网址因网络因素暂时不可访问，故跳过 {附件链接}')
            离线化线程常量.黑名单域名列表.append(urlparse(附件链接).netloc)
            return False
    except:
        print('用 HEAD 方法获取页面类型失败了')
    try:
        返回 = 网络请求器.open(request.Request(附件链接, headers=HEADERS))
    except:
        print(f'附件下载失败：{附件链接}')
        return False
    输出文件名 = 由url返回获得文件名(附件链接, 返回)
    if 输出文件名 == False:
        print(f'附件下载失败：{附件链接}')
        return False
    print(f'要写入的文件名：{目标文件夹路径 + "/" + 输出文件名}')

    if os.path.exists(目标文件夹路径 + '/' + 输出文件名):
        if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
            open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.read())
            print(f'写入完成：{目标文件夹路径 + "/" + 输出文件名}')
        elif 常量.有重名时的处理方式 == 2:
            pass
        else:
            获取进程状态的常量.进程需要等待 = True
            提醒是否要覆盖的信号.emit('冲突',
                                 f'目标附件已存在，是否覆盖？\n\n源文件：\n{附件链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(目标文件夹路径 + "/" + 输出文件名))}）：\n{目标文件夹路径 + "/" + 输出文件名}\n\n')
            while 获取进程状态的常量.进程需要等待:
                进程.sleep(1)
            是否要覆盖 = 获取进程状态的常量.进程是否下载文件覆盖本地文件
            if 是否要覆盖 == QMessageBox.YesToAll:
                常量.有重名时的处理方式 = 1
                open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.read())
                print(f'写入完成：{目标文件夹路径 + "/" + 输出文件名}')
            elif 是否要覆盖 == QMessageBox.Yes:
                open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.read())
                print(f'写入完成：{目标文件夹路径 + "/" + 输出文件名}')
            elif 是否要覆盖 == QMessageBox.No:
                pass
            elif 是否要覆盖 == QMessageBox.NoToAll:
                常量.有重名时的处理方式 = 2
                pass
    else:
        open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.read())
        print(f'写入完成：{目标文件夹路径 + "/" + 输出文件名}')
    return 输出文件名