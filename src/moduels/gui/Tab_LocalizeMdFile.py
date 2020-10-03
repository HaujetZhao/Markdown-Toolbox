# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量
from moduels.component.Widget_FileList import Widget_FileList
from moduels.component.Widget_FileLineEdit import Widget_FileLineEdit
from moduels.function.fileSizeNormalize import fileSizeNormalize
from moduels.function.从字符串搜索到所有附件路径 import 从字符串搜索到所有附件路径

import os, re
from http.cookiejar import MozillaCookieJar
from urllib import request
from urllib.parse import urlparse
from shutil import copy, move


class Tab_LocalizeMdFile(QWidget):
    def __init__(self):
        super().__init__()
        self.initElement()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayout()  # 然后布局
        self.initValue()  # 再定义各个控件的值

    def initElement(self):
        self.文件列表控件 = Widget_FileList()
        self.新增文件按钮 = QPushButton('+')
        self.删除选中文件按钮 = QPushButton('-')
        self.cookie路径提醒 = QLabel('  Cookie：')
        self.cookie路径输入框 = Widget_FileLineEdit()
        self.cookie路径选择按钮 = QPushButton('选择cookie文件')
        self.输出相对路径提醒 = QLabel('相对路径：')
        self.输出相对路径输入框 = Widget_FileLineEdit()
        self.离线化执行按钮 = QPushButton('开始离线化')

        self.输入文件部分盒子 = QGroupBox('输入')
        self.cookie部分盒子 = QGroupBox('Cookie')
        self.输出相对路径部分盒子 = QGroupBox('输出')
        self.动作部分盒子 = QGroupBox('动作')


        self.输入文件部分布局 = QVBoxLayout()
        self.输入文件按钮布局 = QHBoxLayout()

        self.cookie文件部分布局 = QVBoxLayout()
        self.cookie文件一行布局 = QHBoxLayout()

        self.输出文件部分布局 = QVBoxLayout()
        self.输出文件一行布局 = QHBoxLayout()

        self.动作部分布局 = QHBoxLayout()

        self.主布局 = QVBoxLayout()
        pass

    def initSlots(self):
        self.新增文件按钮.clicked.connect(self.文件列表控件.增加条目)
        self.删除选中文件按钮.clicked.connect(self.文件列表控件.删除条目)
        self.cookie路径选择按钮.clicked.connect(self.选择cookie文件)
        self.离线化执行按钮.clicked.connect(self.本地化任务)



        pass

    def initLayout(self):
        self.输入文件按钮布局.addWidget(self.新增文件按钮)
        self.输入文件按钮布局.addWidget(self.删除选中文件按钮)
        self.输入文件部分布局.addWidget(self.文件列表控件)
        self.输入文件部分布局.addLayout(self.输入文件按钮布局)
        self.输入文件部分盒子.setLayout(self.输入文件部分布局)

        self.cookie文件一行布局.addWidget(self.cookie路径提醒)
        self.cookie文件一行布局.addWidget(self.cookie路径输入框)
        self.cookie文件一行布局.addWidget(self.cookie路径选择按钮)
        # self.cookie文件部分布局.addLayout(self.cookie文件一行布局)
        # self.cookie部分盒子.setLayout(self.cookie文件部分布局)

        self.输出文件一行布局.addWidget(self.输出相对路径提醒)
        self.输出文件一行布局.addWidget(self.输出相对路径输入框)
        self.输出文件部分布局.addLayout(self.cookie文件一行布局)
        self.输出文件部分布局.addLayout(self.输出文件一行布局)
        self.输出相对路径部分盒子.setLayout(self.输出文件部分布局)


        self.动作部分布局.addWidget(self.离线化执行按钮)
        self.动作部分盒子.setLayout(self.动作部分布局)


        self.主布局.addWidget(self.输入文件部分盒子)
        # self.主布局.addWidget(self.cookie部分盒子)
        self.主布局.addWidget(self.输出相对路径部分盒子)
        self.主布局.addWidget(self.动作部分盒子)
        self.setLayout(self.主布局)

        pass

    def initValue(self):
        self.文件列表控件.文件列表.append('D:/Users/Haujet/Documents/Markdown 文档/软件笔记/Shortcut Mapper.md')
        self.文件列表控件.刷新列表()
        self.输出相对路径输入框.setText('assets')
        self.cookie路径输入框.setPlaceholderText('可选，txt 格式（Netscape HTTP cookie File）')
        pass




    # def 选择一个文件填充到输入框(self, 文件类型, 输入框):
    #     获得的文件, _ = QFileDialog.getSaveFileName(self, self.tr('选择保存位置'), 文件类型)
    #     if file != '':
    #         self.输入框.setText(获得的文件)




    def 检查路径(self, 路径):
        # print(f'要检查的路径：{路径}')
        if not os.path.exists(路径):
            try:
                os.makedirs(路径)
                return True
            except:
                # print('创建文件夹失败，有可能是权限问题')
                return False
        else:
            return True

    def 选择cookie文件(self):
        获得的路径, _ = QFileDialog.getOpenFileName(self, self.tr('选择cookie文件'), filter='cookie文件 (*.txt)')
        if 获得的路径 != '':
            self.cookie路径输入框.setText(获得的路径)

    def 本地化任务(self):
        常量.状态栏.showMessage('正在本地化中')
        常量.有重名时的处理方式 = 0 # 0 是询问，1 是全部覆盖，2 是全部跳过
        输入文件列表 = self.文件列表控件.文件列表
        目标相对文件夹路径 = self.输出相对路径输入框.text().rstrip('/').lstrip('/')
        if len(输入文件列表) == 0 or 目标相对文件夹路径 == '':
            return
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

            if not self.将文档索引的链接本地化(输入文件, 搜索到的路径列表, 目标相对文件夹路径): # 将链接列表中的附件全都复制移动
                return False
        self.下载附件冲突时的做法 = 0
        常量.状态栏.showMessage('任务完成')




    def 将文档索引的链接本地化(self, 文档, 附件链接列表, 目标相对文件夹路径):
        下载目标路径 = os.path.dirname(文档) + '/' + 目标相对文件夹路径
        if not self.检查路径(下载目标路径):
            return False
        try:
            with open(文档, 'r', encoding='utf-8') as f:
                文档内容 = f.read()
        except:
            with open(文档, 'r', encoding='gbk') as f:
                文档内容 = f.read()
        cookie路径 = self.cookie路径输入框.text()


        for 附件链接 in 附件链接列表:
            if os.path.exists(附件链接): # 如果这个文件是本地绝对路径，就转为相对路径
                目标文件完整路径 = 下载目标路径 + '/' + os.path.basename(附件链接)
                if os.path.exists(目标文件完整路径):
                    if 常量.有重名时的处理方式 == 1: # 0 是询问，1 是全部覆盖，2 是全部跳过
                        os.remove(附件复制的目标路径)
                    elif 常量.有重名时的处理方式 == 2:
                        continue
                    else:
                        是否要覆盖 = QMessageBox.question(self, '冲突', f'目标附件已存在，是否覆盖？\n\n源文件（大小 {fileSizeNormalize(os.path.getsize(附件链接))}）：\n{附件链接}\n\n目标文件（大小 {fileSizeNormalize(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n', QMessageBox.YesToAll | QMessageBox.Yes | QMessageBox.No | QMessageBox.NoToAll)
                        if 是否要覆盖 == QMessageBox.YesToAll:
                            常量.有重名时的处理方式 = 1
                            os.remove(附件复制的目标路径)
                        elif 是否要覆盖 == QMessageBox.Yes:
                            os.remove(附件复制的目标路径)
                        elif 是否要覆盖 == QMessageBox.No:
                            continue
                        elif 是否要覆盖 == QMessageBox.NoToAll:
                            常量.有重名时的处理方式 = 2
                            continue
                move(附件链接, 目标文件完整路径)
                文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + os.path.basename(附件链接))
            elif os.path.exists(os.path.dirname(文档) + '/' + 附件链接): # 如果这个链接是相对链接，那就跳过
                continue
            else: # 如果即不是本地绝对路径，也不是本地相对路径，那就尝试是不是网络路径
                下载的文件名 = self.下载链接文件(附件链接, 目标相对文件夹路径, cookie路径)
                if 下载的文件名 == False:
                    continue
                文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + 下载的文件名)
        try:
            with open(文档, 'w', encoding='utf-8') as f:
                f.write(文档内容)
        except:
            with open(文档, 'w', encoding='gbk') as f:
                f.write(文档内容)




                # 下载的文件 = 网络请求器.open(request.Request(url, headers=DEFAULT_HEADERS))

                pass
            # if os.path.exists(文档所在文件夹 + '/' + os.path.dirname(附件链接)): # 如果这个图片路径是个相对路径
            #     if not self.检查路径(目标文件夹 + '/' + os.path.dirname(附件链接)): # 创建目标相对路径
            #         print('这张图片的目标路径文件夹无法创建，继续下一份附件')
            #         continue
            #     附件复制的源路径 = 文档所在文件夹 + '/' + 附件链接
            #     附件复制的目标路径 = 目标文件夹 + '/' + 附件链接
            #     # print(f'附件复制的源路径{附件复制的源路径}')
            #     # print(f'附件复制的目标路径{附件复制的目标路径}')
            #     if os.path.exists(附件复制的目标路径) and os.path.isdir(附件复制的目标路径):
            #         QMessageBox.warning(self, '警告', f'附件 {附件复制的源路径} 需要复制到 {附件复制的目标路径}，但是目标路径 {附件复制的目标路径} 已是一个文件夹，所以停止复制，请手动处理后再继续复制')
            #         return False
            #     if os.path.exists(附件复制的目标路径) and os.path.isfile(附件复制的目标路径):
            #         if self.下载附件冲突时的做法 == 1:
            #             os.remove(附件复制的目标路径)
            #         elif self.下载附件冲突时的做法 == 2:
            #             continue
            #         else:
            #             是否要覆盖 = QMessageBox.question(self, '冲突', f'目标附件已存在，是否覆盖？\n\n源文件（大小 {fileSizeNormalize(os.path.getsize(附件复制的源路径))}）：\n{附件复制的源路径}\n\n目标文件（大小 {fileSizeNormalize(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n', QMessageBox.YesToAll | QMessageBox.Yes | QMessageBox.No | QMessageBox.NoToAll)
            #             if 是否要覆盖 == QMessageBox.YesToAll:
            #                 self.下载附件冲突时的做法 = 1
            #                 os.remove(附件复制的目标路径)
            #             elif 是否要覆盖 == QMessageBox.Yes:
            #                 os.remove(附件复制的目标路径)
            #             elif 是否要覆盖 == QMessageBox.No:
            #                 continue
            #             elif 是否要覆盖 == QMessageBox.NoToAll:
            #                 self.下载附件冲突时的做法 = 2
            #                 continue
            #     try:
            #         if self.转移md文档时是否为移动:
            #             move(附件复制的源路径, 附件复制的目标路径)
            #         else:
            #             copy(附件复制的源路径, 附件复制的目标路径)
            #         # print('复制成功')
            #     except:
            #         print('一份附件复制失败')
        return True

    def 处理Headers(self, HEADERS, 附件链接):
        pass

    def 下载链接文件(self, 附件链接, 目标文件夹路径, cookie路径): # 0 是询问，1 是全部覆盖，2 是全部跳过
        cookie = MozillaCookieJar()
        if os.path.exists(cookie路径):
            cookie.load(cookie路径, ignore_discard=True, ignore_expires=True)
        网络请求器 = request.build_opener(request.HTTPCookieProcessor(cookie))
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4272.0 Safari/537.36 Edg/87.0.654.0"}
        self.处理Headers(HEADERS, 附件链接) # 有的网站可能需要在 Header 中加入 referencer
        返回 = 网络请求器.open(request.Request(附件链接, headers=HEADERS))
        输出文件名 = self.由url返回获得文件名(附件链接, 返回)
        if 输出文件名 == False:
            print(f'附件下载失败：{附件链接}')
            return False
        if os.path.exists(目标文件夹路径 + '/' + 输出文件名):
            if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
                open(目标文件夹路径 + '/' + 输出文件名, 'wb', encoding='utf-8').write(返回.read())
            elif 常量.有重名时的处理方式 == 2:
                pass
            else:
                是否要覆盖 = QMessageBox.question(self, '冲突',
                                             f'目标附件已存在，是否覆盖？\n\n源文件（大小 {fileSizeNormalize(os.path.getsize(附件链接))}）：\n{附件链接}\n\n目标文件（大小 {fileSizeNormalize(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n',
                                             QMessageBox.YesToAll | QMessageBox.Yes | QMessageBox.No | QMessageBox.NoToAll)
                if 是否要覆盖 == QMessageBox.YesToAll:
                    常量.有重名时的处理方式 = 1
                    open(目标文件夹路径 + '/' + 输出文件名, 'wb', encoding='utf-8').write(返回.read())
                elif 是否要覆盖 == QMessageBox.Yes:
                    open(目标文件夹路径 + '/' + 输出文件名, 'wb', encoding='utf-8').write(返回.read())
                elif 是否要覆盖 == QMessageBox.No:
                    pass
                elif 是否要覆盖 == QMessageBox.NoToAll:
                    有重名时的处理方式 = 2
                    pass
        return 输出文件名

    def 由url返回获得文件名(self, url, 返回):
        内容布置 =返回.getheader('Content-Disposition')
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
        return 文件名



