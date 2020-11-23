import os, re, time, _io, socket, requests
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




def 下载链接文件(线程序号, 附件链接, 目标文件夹路径, cookie路径, 提醒是否要覆盖的信号, 进程, 线程锁):  # 0 是询问，1 是全部覆盖，2 是全部跳过
    if urlparse(附件链接).netloc in 离线化线程常量.黑名单域名列表:
        print(f'{线程序号} 号线程：该网址的域名已认为暂时不可访问 {附件链接}')
        return False
    if os.path.exists(cookie路径):
        cookies = parseCookieFile(cookie路径)
    else:
        cookies = {}
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4272.0 Safari/537.36 Edg/87.0.654.0"}
    HEADERS = 处理Headers(HEADERS, 附件链接)  # 有的网站可能需要在 Header 中加入 referencer
    try:
        print(f'{线程序号} 号线程：开始请求网址，查看其类型 {附件链接}')
        返回 = requests.request('head', 附件链接, headers=HEADERS, cookies=cookies, timeout=离线化线程常量.检查链接超时时长)
        页面返回类型 = 返回.headers['content-type']
        print(f'{线程序号} 号线程：得到网页类型 {页面返回类型}')
        if 'text/html' in 页面返回类型:
            return False
        try:
            页面状态 = 返回.headers['status']
            if '404' in 页面状态:
                print(f'404 未找到网页 {附件链接}')
                return False
        except:
            pass
    except requests.Timeout as error:
        print(f'{线程序号} 号线程：访问超时，认为此网址因网络因素暂时不可访问，故跳过 {附件链接}')
        离线化线程常量.黑名单域名列表.append(urlparse(附件链接).netloc)
        return False
    except requests.exceptions.ConnectionError:
        print(f'{线程序号} 号线程：连接错误，故跳过 {附件链接}')
        return False
    except requests.exceptions.ConnectTimeout:
        print(f'{线程序号} 号线程：访问超时，认为此网址因网络因素暂时不可访问，故跳过 {附件链接}')
        离线化线程常量.黑名单域名列表.append(urlparse(附件链接).netloc)
        return False
    except:
        print(f'{线程序号} 号线程：用 HEAD 方法获取页面类型失败了，放弃下载 {附件链接}')
        return False
    # try:


    try:
        返回 = requests.request('get', 附件链接, headers=HEADERS, cookies=cookies, stream=True, timeout=离线化线程常量.检查链接超时时长)
    except:
        print(f'{线程序号} 号线程：附件下载失败：{附件链接}')
        return False
    try:
        页面返回内容大小 = 得到便于阅读的文件大小(int(返回.headers['content-length']))
        输出文件名 = 由url返回获得文件名(附件链接, 返回)
    except:
        print(f'{线程序号} 号线程：网址无法访问，可能不是有效网址 {附件链接}')
        return False
    if 输出文件名 == False:
        print(f'{线程序号} 号线程：附件下载失败：{附件链接}')
        return False
    print(f'{线程序号} 号线程：文件大小为 {页面返回内容大小}，要写入的文件名：{目标文件夹路径 + "/" + 输出文件名}')

    if os.path.exists(目标文件夹路径 + '/' + 输出文件名):
        线程锁.acquire()
        if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
            线程锁.release()
            try:
                open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.content)
            except:
                print(f'写入失败：{输出文件名}')
            print(f'{线程序号} 号线程：写入完成：{目标文件夹路径 + "/" + 输出文件名}')
        elif 常量.有重名时的处理方式 == 2:
            线程锁.release()
        else:
            离线化线程常量.进程需要等待 = True
            提醒是否要覆盖的信号.emit('冲突', f'{线程序号} 号线程：目标附件已存在，是否覆盖？\n\n源文件（大小 {页面返回内容大小}）：\n{附件链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(目标文件夹路径 + "/" + 输出文件名))}）：\n{目标文件夹路径 + "/" + 输出文件名}\n\n')
            while 离线化线程常量.进程需要等待:
                进程.sleep(1)
            线程锁.release()
            是否要覆盖 = 离线化线程常量.进程是否下载文件覆盖本地文件
            if 是否要覆盖 == QMessageBox.YesToAll:
                常量.有重名时的处理方式 = 1
                try:
                    open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.content)
                except:
                    print(f'写入失败：{输出文件名}')
                print(f'{线程序号} 号线程：写入完成：{目标文件夹路径 + "/" + 输出文件名}')
            elif 是否要覆盖 == QMessageBox.Yes:
                open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.content)
                print(f'{线程序号} 号线程：写入完成：{目标文件夹路径 + "/" + 输出文件名}')
            elif 是否要覆盖 == QMessageBox.No:
                pass
            elif 是否要覆盖 == QMessageBox.NoToAll:
                常量.有重名时的处理方式 = 2
                pass
    else:
        try:
            open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.content)
        except:
            print(f'写入失败：{输出文件名}')
        print(f'{线程序号} 号线程：写入完成：{目标文件夹路径 + "/" + 输出文件名}')
    return 输出文件名


def parseCookieFile(cookiefile):
    """Parse a cookies.txt file and return a dictionary of key value pairs
    compatible with requests."""

    cookies = {}
    with open (cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^[#\r\n ]', line):
                lineFields = line.strip().split('\t')
                cookies[lineFields[5]] = lineFields[6]
    return cookies