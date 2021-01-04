# -*- coding: UTF-8 -*-

import os

from PySide2.QtCore import *
from PySide2.QtWidgets import *

from moduels.component.NormalValue import 常量
from moduels.component.Widget_FileLineEdit import Widget_FileLineEdit
from moduels.component.Widget_FileList import Widget_FileList
from moduels.function.getConflictSolution import 处理相同文件名冲突
from moduels.thread.Thread_LocalizeMdFile import Thread_LocalizeMdFile


class Tab_LocalizeMdFile(QWidget):
    状态栏消息 = Signal(str, int)
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
        self.相对化执行按钮 = QPushButton('本地资源离线化')
        self.离线化执行按钮 = QPushButton('所有资源离线化')
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

        self.离线化进程 = Thread_LocalizeMdFile(self)

    def initSlots(self):
        self.新增文件按钮.clicked.connect(self.文件列表控件.增加条目)
        self.删除选中文件按钮.clicked.connect(self.文件列表控件.删除条目)
        self.cookie路径选择按钮.clicked.connect(self.选择cookie文件)
        self.相对化执行按钮.clicked.connect(self.相对化执行)
        self.离线化执行按钮.clicked.connect(self.离线化执行)

        self.离线化进程.文件冲突信号.connect(self.子进程文件冲突)
        self.离线化进程.状态栏消息.connect(lambda 文字, 时间: self.状态栏消息.emit(文字, 时间))
        self.离线化进程.完成.connect(self.离线化完成)

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


        self.动作部分布局.addWidget(self.相对化执行按钮)
        self.动作部分布局.addWidget(self.离线化执行按钮)
        self.动作部分盒子.setLayout(self.动作部分布局)


        self.主布局.addWidget(self.输入文件部分盒子)
        # self.主布局.addWidget(self.cookie部分盒子)
        self.主布局.addWidget(self.输出相对路径部分盒子)
        self.主布局.addWidget(self.动作部分盒子)
        self.setLayout(self.主布局)
        pass

    def initValue(self):
        self.相对化执行按钮.setToolTip('仅离线本地资源，不离线网络资源')
        self.离线化执行按钮.setToolTip('离线所有资源')
        self.文件列表控件.需要验证为文件 = True
        self.文件列表控件.需要验证为文件夹 = False
        self.文件列表控件.正则匹配样式 = r'.+\.md$'
        self.文件列表控件选择文件时候的提示 = '选择要添加的 md 文件'
        self.文件列表控件选择文件时候的过滤器 = 'MD文档 (*.md)'
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
        self.输出相对路径输入框.setText('assets')
        self.cookie路径输入框.setPlaceholderText('可选，txt 格式（Netscape HTTP cookie File）')
        # self.test()





    def 选择cookie文件(self):
        获得的路径, _ = QFileDialog.getOpenFileName(self, self.tr('选择cookie文件'), filter='cookie文件 (*.txt)')
        if 获得的路径 != '':
            self.cookie路径输入框.setText(获得的路径)

    def 得到文件冲突时的处理方式(self, 文本):
        self.离线化进程.文件冲突处理方式 = getConflictSolution(self, 询问内容)
        self.离线化进程.需要暂停 = False

    def 相对化执行(self):
        self.离线化进程.离线网络路径 = False
        self.离线化执行进程开始()

    def 离线化执行(self):
        self.离线化进程.离线网络路径 = True
        self.离线化执行进程开始()

    def 离线化执行进程开始(self):

        # 检查能否执行任务
        if len(self.文件列表控件.路径列表) == 0 or self.输出相对路径输入框.text() == '':
            常量.状态栏.showMessage('没有输入文件，或相对路径为空，无法继续')
            return False

        # 禁用组件，防止重复执行
        self.需要禁用的组件 = [self.离线化执行按钮, self.相对化执行按钮]
        for 组件 in self.需要禁用的组件:
            组件.setDisabled(True)

        # 为进程设置初始值
        self.判断文件是否相同的方式 = self.离线化进程.判断文件是否相同的方式 = 常量.判断文件是否相同的方式
        self.文件冲突处理方式 = self.离线化进程.文件冲突处理方式 = 常量.文件冲突处理方式

        self.离线化进程.输入文件列表 = self.文件列表控件.路径列表
        self.离线化进程.cookie路径 = self.cookie路径输入框.text()
        self.离线化进程.目标相对路径 = self.输出相对路径输入框.text()
        self.离线化进程.提醒是否要覆盖的信号.connect(self.弹窗询问是否要覆盖写入文件)
        self.离线化进程.start()

    def 弹窗询问是否要覆盖写入文件(self, 标题, 内容):
        离线化线程常量.进程是否下载文件覆盖本地文件 = QMessageBox.question(self, 标题, 内容, QMessageBox.YesToAll | QMessageBox.Yes | QMessageBox.No | QMessageBox.NoToAll)
        离线化线程常量.进程需要等待 = False

    def 子进程文件冲突(self, 回复, 源文件Path, 目标文件Path):
        回复.新旧文件相同, 回复.处理手段, 回复.目标绝对路径Path = 处理相同文件名冲突(self, 源文件Path, 目标文件Path)
        回复.已回复 = True
        ...

    def 离线化完成(self):
        for 组件 in self.需要禁用的组件:
            组件.setEnabled(True)



    def test(self):
        import shutil
        用于重置的文件夹 = 'D:/Users/Haujet/Desktop/MD 工具箱测试/离线化测试/_测试源'
        用于测试的文件夹 = 'D:/Users/Haujet/Desktop/MD 工具箱测试/离线化测试/源'
        用于测试的文件 = 'D:/Users/Haujet/Desktop/MD 工具箱测试/离线化测试/源/弹跳.md'
        shutil.rmtree(用于测试的文件夹, ignore_errors=True)
        os.makedirs(用于测试的文件夹)
        shutil.copytree(用于重置的文件夹, 用于测试的文件夹, dirs_exist_ok=True)
        self.文件列表控件.路径列表.append(用于测试的文件)
        self.文件列表控件.刷新列表()

        # 测试部分代码
        # copy('D:/Users/Haujet/Desktop/Markdown 离线化测试/文档/测试文档 - 源文件.md', 'D:/Users/Haujet/Desktop/Markdown 离线化测试/文档/测试文档.md')
        # self.文件列表控件.路径列表.append('D:/Users/Haujet/Desktop/Markdown 离线化测试/文档/测试文档.md')
        # self.文件列表控件.刷新列表()



