# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量, 离线化线程常量
from moduels.function.getAllUrlFromString import 从字符串搜索到所有附件路径
from moduels.function.localizeLinksInDocument import 将文档索引的链接本地化
from moduels.function.checkDirectoryPath import 检查路径
from moduels.function.restoreLinkFromJump import 跳转链接还原

import os, re
from http.cookiejar import MozillaCookieJar
from urllib import request, error
import urllib.error
from urllib.parse import urlparse
from shutil import copy, move, rmtree

class Thread_LocalizeMdFile(QThread):

    输入文件列表 = None
    cookie路径 = None
    目标相对路径 = None
    执行期间需要禁用的组件 = []
    提醒是否要覆盖的信号 = Signal(str, str)


    def __init__(self, parent=None):
        super(Thread_LocalizeMdFile, self).__init__(parent)

    def run(self):
        输入文件列表 = self.输入文件列表
        目标相对文件夹路径 = self.目标相对路径.rstrip('/').lstrip('/')
        if len(输入文件列表) == 0 or 目标相对文件夹路径 == '':
            return
        for 组件 in self.执行期间需要禁用的组件:
            组件.setDisabled(True)
        常量.状态栏.showMessage('正在离线化中')
        常量.mainWindow.setWindowTitle(常量.mainWindow.窗口标题 + '（执行中……）')
        离线化线程常量.黑名单域名列表 = []
        常量.有重名时的处理方式 = 0  # 0 是询问，1 是全部覆盖，2 是全部跳过
        for 输入文件 in 输入文件列表:
            print(f'输入文件：{输入文件}')
            if not os.path.exists(输入文件):
                continue
            try:
                with open(输入文件, 'r', encoding='utf-8') as f:
                    输入文件内容 = f.read()
            except:
                with open(输入文件, 'r', encoding='gbk') as f:
                    输入文件内容 = f.read()

            搜索到的路径列表 = 从字符串搜索到所有附件路径(输入文件内容)  # 从文档内容得到链接列表
            if 搜索到的路径列表 == []:
                continue
            try:  # 将原始文件内容做一下备份，以防万一
                with open(os.path.dirname(输入文件) + '/备份_' + os.path.basename(输入文件), 'w', encoding='utf-8') as f:
                    输入文件内容 = f.write(输入文件内容)
            except:
                with open(os.path.dirname(输入文件) + '/备份_' + os.path.basename(输入文件), 'w', encoding='gbk') as f:
                    输入文件内容 = f.write(输入文件内容)
            是否成功, 搜索到的路径列表 = 跳转链接还原(输入文件, 搜索到的路径列表)
            if not 是否成功:
                continue
            if not 将文档索引的链接本地化(输入文件, 搜索到的路径列表, self.cookie路径, 目标相对文件夹路径, self.提醒是否要覆盖的信号, self, 离线化线程常量):  # 将链接列表中的附件全都复制移动
                return False
        常量.状态栏.showMessage('任务完成')
        常量.mainWindow.setWindowTitle(常量.mainWindow.窗口标题 + '（完成）')
        for 组件 in self.执行期间需要禁用的组件:
            组件.setEnabled(True)
        print('')
        print('全部任务完成')


    # def 将文档索引的链接本地化(self, 文档, 附件链接列表, 目标相对文件夹路径):
    #     下载目标路径 = os.path.dirname(文档) + '/' + 目标相对文件夹路径
    #     if not 检查路径(下载目标路径):
    #         return False
    #     try:
    #         with open(文档, 'r', encoding='utf-8') as f:
    #             文档内容 = f.read()
    #     except:
    #         with open(文档, 'r', encoding='gbk') as f:
    #             文档内容 = f.read()
    #     cookie路径 = self.cookie路径
    #     for 附件链接 in 附件链接列表:
    #         if os.path.exists(附件链接):  # 如果这个文件是本地绝对路径，就转为相对路径
    #             目标文件完整路径 = 下载目标路径 + '/' + os.path.basename(附件链接)
    #             if os.path.exists(目标文件完整路径):
    #                 if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
    #                     os.remove(附件复制的目标路径)
    #                 elif 常量.有重名时的处理方式 == 2:
    #                     continue
    #                 else:
    #                     常量.离线化进程需要等待 = True
    #                     self.提醒是否要覆盖的信号.emit('冲突', f'目标附件已存在，是否覆盖？\n\n源文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件链接))}）：\n{附件链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n')
    #                     while 常量.离线化进程需要等待:
    #                         self.sleep(1)
    #                     是否要覆盖 = 常量.离线化进程是否要覆盖
    #                     if 是否要覆盖 == QMessageBox.YesToAll:
    #                         常量.有重名时的处理方式 = 1
    #                         os.remove(附件复制的目标路径)
    #                     elif 是否要覆盖 == QMessageBox.Yes:
    #                         os.remove(附件复制的目标路径)
    #                     elif 是否要覆盖 == QMessageBox.No:
    #                         continue
    #                     elif 是否要覆盖 == QMessageBox.NoToAll:
    #                         常量.有重名时的处理方式 = 2
    #                         continue
    #             move(附件链接, 目标文件完整路径)
    #             文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + os.path.basename(附件链接))
    #         elif os.path.exists(os.path.dirname(文档) + '/' + 附件链接):  # 如果这个链接是相对链接，那就跳过
    #             continue
    #         else:  # 如果即不是本地绝对路径，也不是本地相对路径，那就尝试是不是网络路径
    #             下载的文件名 = 下载链接文件(附件链接, 下载目标路径, self.cookie路径, self.提醒是否要覆盖的信号, self, 离线化进程常量)
    #             if 下载的文件名 == False:
    #                 continue
    #             文档内容 = 文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + 下载的文件名)
    #             print(f'现在开始替换\n原始：{附件链接}\n替换成：{目标相对文件夹路径 + "/" + 下载的文件名}')
    #             print('')
    #     try:
    #         with open(文档, 'w', encoding='utf-8') as f:
    #             f.write(文档内容)
    #     except:
    #         with open(文档, 'w', encoding='gbk') as f:
    #             f.write(文档内容)
    #     return True

    def 处理Headers(self, HEADERS, 附件链接):
        pass


    # def 下载链接文件(self, 附件链接, 目标文件夹路径, cookie路径): # 0 是询问，1 是全部覆盖，2 是全部跳过
    #     cookie = MozillaCookieJar()
    #     if os.path.exists(cookie路径):
    #         cookie.load(cookie路径, ignore_discard=True, ignore_expires=True)
    #     网络请求器 = request.build_opener(request.HTTPCookieProcessor(cookie))
    #     HEADERS = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4272.0 Safari/537.36 Edg/87.0.654.0"}
    #     self.处理Headers(HEADERS, 附件链接) # 有的网站可能需要在 Header 中加入 referencer
    #     try:
    #         返回 = 网络请求器.open(request.Request(附件链接, headers=HEADERS))
    #     except urllib.error.URLError as error:
    #         print(error)
    #         print(f'附件下载失败：{附件链接}')
    #         return False
    #     输出文件名 = self.由url返回获得文件名(附件链接, 返回)
    #     if 输出文件名 == False:
    #         print(f'附件下载失败：{附件链接}')
    #         return False
    #     print(f'要写入的文件名：{目标文件夹路径 + "/" + 输出文件名}')
    #
    #     if os.path.exists(目标文件夹路径 + '/' + 输出文件名):
    #         if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
    #             open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.read())
    #             print(f'写入完成：{目标文件夹路径 + "/" + 输出文件名}')
    #         elif 常量.有重名时的处理方式 == 2:
    #             pass
    #         else:
    #             常量.离线化进程需要等待 = True
    #             self.提醒是否要覆盖的信号.emit('冲突', f'目标附件已存在，是否覆盖？\n\n源文件：\n{附件链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(目标文件夹路径 + "/" + 输出文件名))}）：\n{目标文件夹路径 + "/" + 输出文件名}\n\n')
    #             while 常量.离线化进程需要等待:
    #                 self.sleep(1)
    #             是否要覆盖 = 常量.离线化进程是否要覆盖
    #             if 是否要覆盖 == QMessageBox.YesToAll:
    #                 常量.有重名时的处理方式 = 1
    #                 open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.read())
    #                 print(f'写入完成：{目标文件夹路径 + "/" + 输出文件名}')
    #             elif 是否要覆盖 == QMessageBox.Yes:
    #                 open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.read())
    #                 print(f'写入完成：{目标文件夹路径 + "/" + 输出文件名}')
    #             elif 是否要覆盖 == QMessageBox.No:
    #                 pass
    #             elif 是否要覆盖 == QMessageBox.NoToAll:
    #                 常量.有重名时的处理方式 = 2
    #                 pass
    #     else:
    #         open(目标文件夹路径 + '/' + 输出文件名, 'wb').write(返回.read())
    #         print(f'写入完成：{目标文件夹路径 + "/" + 输出文件名}')
    #     return 输出文件名


    # def 由url返回获得文件名(self, url, 返回):
    #     print(f'要询问文件名的 url：{url}')
    #     try:
    #         页面返回类型 = 返回.getheader('content-type')
    #         if 'text/html' in 页面返回类型:
    #             return False
    #         内容布置 = 返回.getheader('Content-Disposition')
    #     except:
    #         return False
    #     print(f'内容布置：{内容布置}')
    #     if 内容布置 != None:
    #         文件名 = re.search('(filename=")(.+?)(";)', 内容布置).group(2)
    #         print('从 Content - Disposition 得到文件名')
    #     elif 返回.geturl() != url:
    #         重导向的url = 返回.geturl()
    #         重导向后解析结果 = urlparse(重导向的url)
    #         文件名 = os.path.basename(重导向后解析结果.path)
    #         prin('从重导向的 url 获得文件名')
    #     else:
    #         try:
    #             文件名 = os.path.basename(urlparse(url).path)
    #             print('从原始 url 获得文件名')
    #         except:
    #             print(f'没能获得文件名，url：{url}')
    #             return False
    #     print(f'文件名：{文件名}')
    #     if 文件名 != '':
    #         return 文件名
    #     else:
    #         return False

    # def 检查路径(self, 路径):
    #     # print(f'要检查的路径：{路径}')
    #     if not os.path.exists(路径):
    #         try:
    #             os.makedirs(路径)
    #             return True
    #         except:
    #             # print('创建文件夹失败，有可能是权限问题')
    #             return False
    #     else:
    #         return True
