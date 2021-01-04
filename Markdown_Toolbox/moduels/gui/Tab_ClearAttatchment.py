# -*- coding: UTF-8 -*-

import os
from shutil import rmtree, copytree

from PySide2.QtCore import *
from PySide2.QtWidgets import *

from moduels.component.NormalValue import 常量
from moduels.component.Widget_FileList import Widget_FileList
from moduels.thread.Thread_ClearAttatchment import Thread_ClearAttatchment


class Tab_ClearAttatchment(QWidget):
    状态栏消息 = Signal(str, int)
    def __init__(self):
        super().__init__()
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值
        # self.test()

    def initElements(self):
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

        self.进程 = Thread_ClearAttatchment()
        pass

    def initSlots(self):
        self.新增文件夹按钮.clicked.connect(self.文件夹列表控件.增加条目)
        self.删除选中文件夹按钮.clicked.connect(self.文件夹列表控件.删除条目)
        self.清理动作执行按钮.clicked.connect(self.开始执行清理任务)
        self.进程.提醒是否确认要删除的信号.connect(self.弹窗提示已移动但需要手动确认删除)
        self.进程.完成.connect(self.完成)
        self.进程.状态栏消息.connect(lambda 文本, 时长: self.状态栏消息.emit(文本, 时长))
        pass

    def initLayouts(self):
        self.输入文件夹按钮布局.addWidget(self.新增文件夹按钮)
        self.输入文件夹按钮布局.addWidget(self.删除选中文件夹按钮)
        self.输入文件夹部分布局.addWidget(self.文件夹列表控件)
        self.输入文件夹部分布局.addLayout(self.输入文件夹按钮布局)
        self.输入文件夹部分盒子.setLayout(self.输入文件夹部分布局)


        self.动作部分布局.addWidget(self.清理动作执行按钮)
        self.动作部分盒子.setLayout(self.动作部分布局)


        self.主布局.addWidget(self.输入文件夹部分盒子)
        self.主布局.addWidget(self.动作部分盒子)
        self.setLayout(self.主布局)

        pass

    def initValues(self):
        self.文件夹列表控件.需要验证为文件 = False
        self.文件夹列表控件.需要验证为文件夹 = True
        self.文件夹列表控件.正则匹配样式 = '.+'
        self.文件夹列表控件.选择文件时候的提示 = '选择要清理无用附件的 md 文件所在目录'
        self.执行期间需要禁用的组件 = [self.清理动作执行按钮]
        常量.离线化功能标签页 = self

    def 开始执行清理任务(self):
        if len(self.文件夹列表控件.路径列表) < 1:
            self.状态栏消息.emit('没有需要清理的文件夹', 5000)
            return False

        for 控件 in self.执行期间需要禁用的组件:
            控件.setDisabled(True)

        self.进程.输入文件夹列表 = self.文件夹列表控件.路径列表
        self.进程.start()


    def 弹窗提示已移动但需要手动确认删除(self, confirmation):
        结果 = QMessageBox.question(self, '请确认是否要删除', '为了安全起见，已将所有 md 文档的相对路径未引用的附件移动到了同级的“未引用附件”文件夹中，删除需要你手动二次确认，是否要删除？', QMessageBox.Yes | QMessageBox.No)
        if 结果 == QMessageBox.Yes:
            confirmation.是否删除 = True
        else:
            confirmation.是否删除 = False
        confirmation.已回复 = True

    def 完成(self):
        for 控件 in self.执行期间需要禁用的组件:
            控件.setEnabled(True)

    def test(self):
        if os.path.exists('D:/Users/Haujet/Desktop/测试md复制/测试用/测试1'):
            rmtree('D:/Users/Haujet/Desktop/测试md复制/测试用/测试1')
        copytree('D:/Users/Haujet/Desktop/测试md复制/原始/测试1', 'D:/Users/Haujet/Desktop/测试md复制/测试用/测试1')
        self.文件夹列表控件.路径列表.append('D:/Users/Haujet/Desktop/测试md复制/测试用/测试1')
        self.文件夹列表控件.刷新列表()
        # 常量.mainWindow.








