# -*- coding: UTF-8 -*-

import os
import pathlib
import tempfile
import time
from shutil import move, rmtree

from PySide2.QtCore import *

from moduels.function.getAllUrlFromString import 从字符串搜索到所有附件路径


class Confirmation():
    '''
    当要提醒用户删除文件时
    先构造一个实例，
    将这个实例用信号发出去，
    图形界面通过弹窗得到回馈后，将获得的内容写入这个实例
    '''
    def __init__(self):
        self.已回复 = False
        self.是否删除 = False

class Thread_ClearAttatchment(QThread):
    完成 = Signal()
    状态栏消息 = Signal(str, int)
    提醒是否确认要删除的信号 = Signal(Confirmation)


    def __init__(self, parent=None):
        super(Thread_ClearAttatchment, self).__init__(parent)
        self.输入文件夹列表 = None

    def run(self):
        self.状态栏消息.emit('正在清理中', 5000)


        # 常量.mainWindow.setWindowTitle(常量.mainWindow.窗口标题 + '（执行中……）')
        # 常量.有重名时的处理方式 = 0  # 0 是询问，1 是全部覆盖，2 是全部跳过
        # 无效附件移动到的文件夹列表 = []
        临时文件夹列表 = []

        for index, 输入文件夹 in enumerate(self.输入文件夹列表):
            self.状态栏消息.emit(f'有 {len(self.输入文件夹列表)} 个文件夹中需要清理，正在清理第 {index + 1} 个', 5000)
            md文件列表 = self.得到文件夹中的md文件(输入文件夹)

            临时文件夹 = tempfile.mkdtemp(dir=输入文件夹, prefix='未引用附件-')
            临时文件夹列表.append(临时文件夹)
            所有相对路径文件夹的绝对路径列表, 所有md文件的有效相对路径文件词典 = self.得到所有相对路径文件夹的绝对路径(md文件列表)
            print(所有相对路径文件夹的绝对路径列表)
            所有相对路径中的文件列表 = self.得到所有相对路径中的文件(所有相对路径文件夹的绝对路径列表)
            print(所有相对路径中的文件列表)
            for 待测文件 in 所有相对路径中的文件列表:
                if 待测文件 in 所有md文件的有效相对路径文件词典:
                    print(f'文件被引用，不删除：\n    文件：{待测文件}\n    引用者：{所有md文件的有效相对路径文件词典[待测文件]}\n')
                    continue
                else:
                    print(f'未引用，删除！\n    文件：{待测文件}\n')
                    move(待测文件, 临时文件夹)
        确认 = Confirmation()
        self.提醒是否确认要删除的信号.emit(确认)
        while not 确认.已回复:
            time.sleep(0.1)
        if 确认.是否删除:
            for 临时文件夹 in 临时文件夹列表:
                try:
                    rmtree(临时文件夹)
                except Exception as e:
                    print(f'删除临时文件夹出错: \n    文件夹: {临时文件夹}\n    原因: {e}')
        self.状态栏消息.emit(f'清理完成', 5000)
        self.完成.emit()

    def 得到文件夹中的md文件(self, 文件夹):
        Md文件列表 = []
        for item in os.listdir(文件夹):
            if os.path.isfile(pathlib.Path(文件夹) / item) and pathlib.Path(item).suffix == '.md':
                Md文件列表.append((pathlib.Path(文件夹) / item).as_posix())
        print(f'得到文件夹下的所有md文件：\n    文件夹：{文件夹}\n    md文件：{Md文件列表}\n')
        return Md文件列表

    def 得到文件内容(self, 输入文件):
        try:
            with open(输入文件, 'r', encoding='utf-8') as f:
                输入文件内容 = f.read()
        except:
            with open(输入文件, 'r', encoding='gbk') as f:
                输入文件内容 = f.read()
        return 输入文件内容

    def 得到所有相对路径文件夹的绝对路径(self, md文件列表):
        文件夹集合 = set()
        文件词典 = {}
        for 文件 in md文件列表:
            文件内容 = self.得到文件内容(文件)
            链接集合 = set()
            链接集合 |= set(从字符串搜索到所有附件路径(文件内容))
            有效相对路径集合 = self.得到有效相对路径集合(链接集合, 文件)
            有效相对路径的绝对路径集合 = set((pathlib.Path(文件).parent / 相对路径).as_posix() for 相对路径 in 有效相对路径集合)
            有效相对路径所在文件夹的绝对路径集合 = set(os.path.dirname(文件路径) for 文件路径 in 有效相对路径的绝对路径集合)
            文件夹集合 |= 有效相对路径所在文件夹的绝对路径集合
            当前文档附件路径词典 = {路径:文件 for 路径 in 有效相对路径的绝对路径集合}
            文件词典.update(当前文档附件路径词典)
        print(f'统计出当前文件夹下的所有md文件引用的相对路径集合：\n    文件夹集合：{文件夹集合}\n')
        return list(文件夹集合), 文件词典

    def 得到有效相对路径集合(self, 链接集合, 文件):
        有效相对路径集合 = set()
        for 链接 in 链接集合:
            if os.path.exists(链接): continue
            if os.path.exists(os.path.join(os.path.dirname(文件), 链接)) and os.path.dirname(链接) != '':
                if os.path.dirname(文件) in (pathlib.Path(os.path.dirname(文件)) / 链接).as_posix():
                    有效相对路径集合.add(链接)
        print(f'得到文档的所有相对路径：\n    文档：{文件}\n    相对文件夹：{有效相对路径集合}\n')
        return 有效相对路径集合

    def 得到所有相对路径中的文件(self, 文件夹列表):
        文件列表 = []
        for 文件夹 in 文件夹列表:
            for 文件 in os.listdir(文件夹):
                if os.path.isfile(pathlib.Path(文件夹) / 文件):
                    文件列表.append((pathlib.Path(文件夹) / 文件).as_posix())
        return 文件列表