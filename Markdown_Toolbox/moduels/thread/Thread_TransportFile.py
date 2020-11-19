# -*- coding: UTF-8 -*-

# 暂时放弃在一个新线程内处理这个了。

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量, 转移线程常量
from moduels.function.getAllUrlFromString import 从字符串搜索到所有附件路径
from moduels.function.checkDirectoryPath import 检查路径
from moduels.function.restoreLinkFromJump import 跳转链接还原

import os, re, time
from shutil import copy, move

class Thread_TransportFile(QThread):

    输入文件列表 = None
    输出文件夹路径= None
    执行期间需要禁用的组件 = []
    提醒是否确认要覆盖的信号 = Signal(str, str)
    转移md文档时是否为移动 = False

    def __init__(self, parent=None):
        super(Thread_TransportFile, self).__init__(parent)

    def run(self):
        输入文件列表 = self.输入文件列表
        for 组件 in self.执行期间需要禁用的组件:
            组件.setDisabled(True)
        if self.转移md文档时是否为移动:
            常量.状态栏.showMessage('正在移动中')
        else:
            常量.状态栏.showMessage('正在复制中')
        常量.mainWindow.setWindowTitle(常量.mainWindow.窗口标题 + '（执行中……）')
        转移线程常量.有重名时的处理方式 = 0 # 0 是覆盖, 1 是全部覆盖 2 是跳过, 3 是全部跳过，
        for 输入文件 in self.输入文件列表:
            print(f'输入文件：{输入文件}')
            if not os.path.exists(输入文件):
                print('    该输入文件不存在，继续下一个文件')
                continue
            try:
                with open(输入文件, 'r', encoding='utf-8') as f:
                    输入文件内容 = f.read()
            except:
                with open(输入文件, 'r', encoding='gbk') as f:
                    输入文件内容 = f.read()
            搜索到的路径列表 = 从字符串搜索到所有附件路径(输入文件内容) # 从文档内容得到链接列表
            if 搜索到的路径列表 != []:
                if not 将文档索引的附件复制(输入文件, 搜索到的路径列表, 输出文件夹路径): # 将链接列表中的附件全都复制移动
                    return False
            md文件的复制输出路径 = 输出文件夹路径 + '/' + os.path.basename(输入文件)
            print('开始转移文档')
            try:
                转移文件(输入文件, md文件的复制输出路径, self.转移md文档时是否为移动, self.提醒是否确认要覆盖的信号, 转移线程常量)
            except:
                print(f'无法将 {输入文件} 移动到指定位置 {md文件的复制输出路径}')
                continue
        转移线程常量.有重名时的处理方式 = 0


        常量.状态栏.showMessage('任务完成')
        常量.mainWindow.setWindowTitle(常量.mainWindow.窗口标题 + '（完成）')
        for 组件 in self.执行期间需要禁用的组件:
            组件.setEnabled(True)
        print('\n\n清理完成\n\n')

def 转移文件(输入路径, 输出路径, 是否为移动, 询问信号, 监控常量):
    # 复制、移动文件，但在转移文件之前，先查看下目标是否已存在
    # 如果目标已存在，就发射一个信息，让上层收到信号弹窗，自身循环 sleep，直到监控的数值有变化
    # 再决定干什么
    # 0 是覆盖, 1 是全部覆盖 2 是跳过, 3 是全部跳过，
    if 是否为移动:  # 再将文档文件本身移动
        if os.path.exists(输出路径):
            if 监控常量.有重名时的处理方式 in [0, 2]:
                监控常量.进程需要等待 = True
                询问信号.emit(输入路径, 输出路径)
                while 监控常量.进程需要等待:
                    time.sleep(0.5)
                if 监控常量.回复数值 in [0, 1]:
                    move(输入文件, md文件的复制输出路径)
                    print(f'成功复制文件：\n    输入：{输入文件}\n    输出：{md文件的复制输出路径}')
            elif 监控常量.有重名时的处理方式 == 1:
                move(输入文件, md文件的复制输出路径)
                print(f'成功移动文件：\n    输入：{输入文件}\n    输出：{md文件的复制输出路径}')
        else:
            move(输入文件, md文件的复制输出路径)
            print(f'成功移动文件：\n    输入：{输入文件}\n    输出：{md文件的复制输出路径}')
    else:
        if os.path.exists(输入路径, 输出路径):
            if 监控常量.有重名时的处理方式 in [0, 2]:
                监控常量.进程需要等待 = True
                询问信号.emit()
                while 监控常量.进程需要等待:
                    time.sleep(0.5)
                if 监控常量.回复数值 in [0, 1]:
                    copy(输入文件, md文件的复制输出路径)
                    print(f'成功复制文件：\n    输入：{输入文件}\n    输出：{md文件的复制输出路径}')
            elif 监控常量.有重名时的处理方式 == 1:
                copy(输入文件, md文件的复制输出路径)
                print(f'成功复制文件：\n    输入：{输入文件}\n    输出：{md文件的复制输出路径}')
        else:
            move(输入文件, md文件的复制输出路径)
            print(f'成功复制文件：\n    输入：{输入文件}\n    输出：{md文件的复制输出路径}')


def 将文档索引的附件复制(文档, 附件列表, 目标文件夹):
    # 提供一个 md 文档路径，然后读取它的内容
    # 提供 md 文档内包含的附件列表
    # 先筛查下有效的相对路径，
    # 再将这个附件列表中的相对路径文件复制到指定文件夹，
    # 再将文档内容中的链接替换
    # 再写入原文档
    文档所在文件夹 = os.path.dirname(文档)
    for 附件路径 in 附件列表:
        if os.path.exists(文档所在文件夹 + '/' + os.path.dirname(附件路径)): # 如果这个图片路径是个相对路径
            if not self.检查路径(目标文件夹 + '/' + os.path.dirname(附件路径)): # 创建目标相对路径
                print('这张图片的目标路径文件夹无法创建，继续下一份附件')
                continue
            附件复制的源路径 = 文档所在文件夹 + '/' + 附件路径
            附件复制的目标路径 = 目标文件夹 + '/' + 附件路径
            # print(f'附件复制的源路径{附件复制的源路径}')
            # print(f'附件复制的目标路径{附件复制的目标路径}')
            if os.path.exists(附件复制的目标路径) and os.path.isdir(附件复制的目标路径):
                QMessageBox.warning(self, '警告', f'附件 {附件复制的源路径} 需要复制到 {附件复制的目标路径}，但是目标路径 {附件复制的目标路径} 已是一个文件夹，所以停止复制，请手动处理后再继续复制')
                return False
            if os.path.exists(附件复制的目标路径) and os.path.isfile(附件复制的目标路径):
                if 常量.有重名时的处理方式 == 1:
                    os.remove(附件复制的目标路径)
                elif 常量.有重名时的处理方式 == 2:
                    continue
                else:
                    是否要覆盖 = QMessageBox.question(self, '冲突', f'目标附件已存在，是否覆盖？\n\n源文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的源路径))}）：\n{附件复制的源路径}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n', QMessageBox.YesToAll | QMessageBox.Yes | QMessageBox.No | QMessageBox.NoToAll)
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
            try:
                if self.转移md文档时是否为移动:
                    move(附件复制的源路径, 附件复制的目标路径)
                else:
                    copy(附件复制的源路径, 附件复制的目标路径)
                # print('复制成功')
            except:
                print('一份附件复制失败')
    return True