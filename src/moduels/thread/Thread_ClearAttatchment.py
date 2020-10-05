# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量, 清理化线程常量
from moduels.function.getAllUrlFromString import 从字符串搜索到所有附件路径
from moduels.function.localizeLinksInDocument import 将文档索引的链接本地化
from moduels.function.checkDirectoryPath import 检查路径
from moduels.function.restoreLinkFromJump import 跳转链接还原

import os, re, time
from http.cookiejar import MozillaCookieJar
from urllib import request, error
import urllib.error
from urllib.parse import urlparse
from shutil import copy, move, rmtree

class Thread_ClearAttatchment(QThread):

    输入文件夹列表 = None
    执行期间需要禁用的组件 = []
    提醒是否确认要删除的信号 = Signal()


    def __init__(self, parent=None):
        super(Thread_ClearAttatchment, self).__init__(parent)

    def run(self):
        输入文件列表 = self.输入文件夹列表
        for 组件 in self.执行期间需要禁用的组件:
            组件.setDisabled(True)
        常量.状态栏.showMessage('正在清理中')
        # 常量.mainWindow.setWindowTitle(常量.mainWindow.窗口标题 + '（执行中……）')
        # 常量.有重名时的处理方式 = 0  # 0 是询问，1 是全部覆盖，2 是全部跳过
        无效附件移动到的文件夹列表 = []
        for 输入文件夹 in 输入文件列表:
            print(f'正在处理的输入文件夹：{输入文件夹}')
            当前文件夹下的附件路径列表 = []
            当前文件夹下的存储相对路径附件的文件夹的列表 = []
            if not os.path.exists(输入文件夹):
                continue
            输入文件夹下的文件列表 = os.listdir(输入文件夹)
            md文档目录 = []
            print(f'当前搜索文件夹的md文档有：')
            for 文件名 in 输入文件夹下的文件列表:
                if re.match('.+\.md$', 文件名):
                    md文档目录.append(输入文件夹 + '/' + 文件名)
                    print(f'      {文件名}')
            if len(md文档目录) < 1:
                continue
            for md文档 in md文档目录:
                print(f'正在文档中搜索相对路径。{md文档}')
                try:
                    md文档内容 = open(md文档, 'r', encoding='utf-8').read()
                except:
                    md文档内容 = open(md文档, 'r', encoding='gbk').read()
                搜索到的附件路径列表 = 从字符串搜索到所有附件路径(md文档内容)
                for 附件路径 in 搜索到的附件路径列表:
                    print('当前文档中的有效相对路径附件有：')
                    附件路径加上文档路径转换的绝对路径 = os.path.dirname(md文档) + '/' + 附件路径
                    if os.path.exists(附件路径加上文档路径转换的绝对路径):
                        if 附件路径加上文档路径转换的绝对路径 not in 当前文件夹下的附件路径列表:
                            当前文件夹下的附件路径列表.append(附件路径加上文档路径转换的绝对路径)
                            print(f'   {附件路径}')
                            print(f'   而其所处的文件夹是{os.path.dirname(附件路径加上文档路径转换的绝对路径)}')
                        if os.path.dirname(附件路径加上文档路径转换的绝对路径) not in 当前文件夹下的存储相对路径附件的文件夹的列表:
                            当前文件夹下的存储相对路径附件的文件夹的列表.append(os.path.dirname(附件路径加上文档路径转换的绝对路径))
                    elif os.path.exists(附件路径):
                        if 附件路径 not in 当前文件夹下的附件路径列表:
                            当前文件夹下的附件路径列表.append(附件路径)
                            print(f'   {附件路径}')
                            print(f'   而其所处的文件夹是{os.path.dirname(附件路径加上文档路径转换的绝对路径)}')
            已找到的附件文件夹中的文件列表 = []
            for 附件文件夹 in 当前文件夹下的存储相对路径附件的文件夹的列表:
                print(f'现在开始统计附件文件夹中的所有附件：{附件文件夹}')
                for 路径 in os.listdir(附件文件夹):
                    路径 = 附件文件夹 + '/' + 路径
                    if os.path.isfile(路径):
                        已找到的附件文件夹中的文件列表.append(路径)
                        print(f'      找到一个附件文件：{路径}')

            print('现在开始统计无用的附件')
            无用的附件列表 = []
            for 附件文件 in 已找到的附件文件夹中的文件列表:
                if 附件文件 not in 当前文件夹下的附件路径列表:
                    无用的附件列表.append(附件文件)
            print('现在开始移动无用的附件')
            for 无用附件 in 无用的附件列表:
                目标文件夹 = os.path.dirname(os.path.dirname(无用附件)) + '/' + '未引用附件'
                if not 检查路径(目标文件夹):
                    print(f'要移动到的目录未能成功创建：{目标文件夹}')
                    continue
                原完整路径名 = 目标文件夹 + '/' + os.path.basename(无用附件)
                目标完整路径名 = 原完整路径名
                重复后文件名加的后缀数字 = 1
                while os.path.exists(目标完整路径名):
                    print(f'无用附件要移动到目标的目标位置已有同名文件：{目标完整路径名}')
                    print('保留两者')
                    原完整路径名分割后 = os.path.splitext(原完整路径名)
                    目标完整路径名 = 原完整路径名分割后[0] + str(重复后文件名加的后缀数字) + 原完整路径名分割后[1]
                    print(f'尝试新目标文件名：{目标完整路径名}')
                    重复后文件名加的后缀数字 += 1
                move(无用附件, 目标完整路径名)
                if 目标文件夹 not in 无效附件移动到的文件夹列表:
                    无效附件移动到的文件夹列表.append(目标文件夹)
                print(f'成功将 {无用附件} 移动到 {目标完整路径名}')
        清理化线程常量.进程需要等待 = True
        if len(无效附件移动到的文件夹列表) > 0:
            self.提醒是否确认要删除的信号.emit()
            while 清理化线程常量.进程需要等待:
                self.sleep(1)
            if 清理化线程常量.是否确认要删除找到的无用文件:
                print('确认要删除无用附件')
                for 无效附件目录 in 无效附件移动到的文件夹列表:
                    try:
                        rmtree(无效附件目录)
                    except:
                        print(f'一个无效附件目录移除失败：{无效附件目录}')
        常量.状态栏.showMessage('任务完成')
        # 常量.mainWindow.setWindowTitle(常量.mainWindow.窗口标题 + '（完成）')
        for 组件 in self.执行期间需要禁用的组件:
            组件.setEnabled(True)
        print(f'\n\n清理完成 {time.time()}\n\n')

