# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量, 离线化进程常量
from moduels.component.Widget_FileList import Widget_FileList
from moduels.component.Widget_FileLineEdit import Widget_FileLineEdit
from moduels.thread.Thread_LocalizeMdFile import Thread_LocalizeMdFile

import os
from shutil import copy, move, rmtree


class Tab_ClearAttatchment(QWidget):
    def __init__(self):
        super().__init__()
        self.initElement()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayout()  # 然后布局
        self.initValue()  # 再定义各个控件的值

    def initElement(self):
        self.文件夹列表控件 = Widget_FileList()
        self.新增文件夹按钮 = QPushButton('+')
        self.删除选中文件夹按钮 = QPushButton('-')
        self.清理动作执行按钮 = QPushButton('清理相对路径未引用的附件')

        self.输入文件夹部分盒子 = QGroupBox('输入需要清理的文件夹')
        self.动作部分盒子 = QGroupBox('动作')


        self.输入文件夹部分布局 = QVBoxLayout()
        self.输入文件夹按钮布局 = QHBoxLayout()

        self.动作部分布局 = QHBoxLayout()

        self.主布局 = QVBoxLayout()
        pass

    def initSlots(self):
        self.新增文件夹按钮.clicked.connect(self.文件夹列表控件.增加条目)
        self.删除选中文件夹按钮.clicked.connect(self.文件夹列表控件.删除条目)
        self.清理动作执行按钮.clicked.connect(self.开始执行清理任务)
        pass

    def initLayout(self):
        self.输入文件夹按钮布局.addWidget(self.新增文件夹按钮)
        self.输入文件夹按钮布局.addWidget(self.删除选中文件夹按钮)
        self.输入文件夹部分布局.addWidget(self.文件夹列表控件)
        self.输入文件夹部分布局.addLayout(self.输入文件夹按钮布局)
        self.输入文件夹部分盒子.setLayout(self.输入文件夹部分布局)

        # self.cookie文件一行布局.addWidget(self.cookie路径提醒)
        # self.cookie文件一行布局.addWidget(self.cookie路径输入框)
        # self.cookie文件一行布局.addWidget(self.cookie路径选择按钮)
        # self.cookie文件部分布局.addLayout(self.cookie文件一行布局)
        # self.cookie部分盒子.setLayout(self.cookie文件部分布局)

        # self.输出文件一行布局.addWidget(self.输出相对路径提醒)
        # self.输出文件一行布局.addWidget(self.输出相对路径输入框)
        # self.输出文件部分布局.addLayout(self.cookie文件一行布局)
        # self.输出文件部分布局.addLayout(self.输出文件一行布局)
        # self.输出相对路径部分盒子.setLayout(self.输出文件部分布局)


        self.动作部分布局.addWidget(self.清理动作执行按钮)
        self.动作部分盒子.setLayout(self.动作部分布局)


        self.主布局.addWidget(self.输入文件夹部分盒子)
        # self.主布局.addWidget(self.cookie部分盒子)
        # self.主布局.addWidget(self.输出相对路径部分盒子)
        self.主布局.addWidget(self.动作部分盒子)
        self.setLayout(self.主布局)

        pass

    def initValue(self):
        self.文件夹列表控件.需要验证为文件 = False
        self.文件夹列表控件.需要验证为文件夹 = True
        self.文件夹列表控件.正则匹配样式 = '.+'
        self.文件夹列表控件.选择文件时候的提示 = '选择要清理无用附件的 md 文件所在目录'
        常量.离线化功能标签页 = self
        # if os.path.exists('D:/Users/Haujet/Desktop/测试md复制/test_derive.md'):
        #     os.remove('D:/Users/Haujet/Desktop/测试md复制/test_derive.md')
        # if os.path.exists('D:/Users/Haujet/Desktop/测试md复制/test_derive2.md'):
        #     os.remove('D:/Users/Haujet/Desktop/测试md复制/test_derive2.md')
        # if os.path.exists('D:/Users/Haujet/Desktop/测试md复制/assets'):
        #     rmtree('D:/Users/Haujet/Desktop/测试md复制/assets')
        # copy('D:/Users/Haujet/Desktop/测试md复制/test_origin.md', 'D:/Users/Haujet/Desktop/测试md复制/test_derive.md')
        # copy('D:/Users/Haujet/Desktop/测试md复制/test_origin2.md', 'D:/Users/Haujet/Desktop/测试md复制/test_derive2.md')
        # self.文件列表控件.文件列表.append('D:/Users/Haujet/Desktop/测试md复制/test_derive.md')
        # self.文件列表控件.文件列表.append('D:/Users/Haujet/Desktop/测试md复制/test_derive2.md')
        # self.文件列表控件.刷新列表()
        # self.输出相对路径输入框.setText('assets')
        # self.cookie路径输入框.setPlaceholderText('可选，txt 格式（Netscape HTTP cookie File）')



    # def 选择一个文件填充到输入框(self, 文件类型, 输入框):
    #     获得的文件, _ = QFileDialog.getSaveFileName(self, self.tr('选择保存位置'), 文件类型)
    #     if file != '':
    #         self.输入框.setText(获得的文件)




    def 选择cookie文件(self):
        获得的路径, _ = QFileDialog.getOpenFileName(self, self.tr('选择cookie文件'), filter='cookie文件 (*.txt)')
        if 获得的路径 != '':
            self.cookie路径输入框.setText(获得的路径)



    def 开始执行清理任务(self):
        return True
        self.进程 = Thread_LocalizeMdFile()
        self.进程.输入文件列表 = self.文件夹列表控件.路径列表
        self.进程.cookie路径 = self.cookie路径输入框.text()
        self.进程.目标相对路径 = self.输出相对路径输入框.text()
        self.进程.执行期间需要禁用的组件 = [self.清理动作执行按钮]
        self.进程.提醒是否要覆盖的信号.connect(self.弹窗询问是否要覆盖写入文件)
        self.进程.start()

    def 弹窗询问是否要覆盖写入文件(self, 标题, 内容):
        离线化进程常量.进程是否要覆盖 = QMessageBox.question(self, 标题, 内容, QMessageBox.YesToAll | QMessageBox.Yes | QMessageBox.No | QMessageBox.NoToAll)
        离线化进程常量.进程需要等待 = False








