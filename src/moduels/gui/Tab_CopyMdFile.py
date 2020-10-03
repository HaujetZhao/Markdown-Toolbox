# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量
from moduels.component.Widget_FileList import Widget_FileList
from moduels.component.Widget_FileLineEdit import Widget_FileLineEdit
from moduels.function.fileSizeNormalize import fileSizeNormalize

import os, re

from shutil import copy, move

class Tab_CopyMdFile(QWidget):
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
        self.输出提醒 = QLabel('输出路径：')
        self.输出位置输入框 = Widget_FileLineEdit()
        self.选择目标路径按钮 = QPushButton('选择目标文件夹')
        self.复制按钮 = QPushButton('复制')
        self.移动按钮 = QPushButton('移动')

        self.输入文件部分盒子 = QGroupBox('输入')
        self.输出文件部分盒子 = QGroupBox('输出')
        self.动作部分盒子 = QGroupBox('动作')


        self.输入文件部分布局 = QVBoxLayout()
        self.输入文件按钮布局 = QHBoxLayout()

        self.输出文件部分布局 = QVBoxLayout()
        self.输出文件一行布局 = QHBoxLayout()

        self.动作部分布局 = QHBoxLayout()

        self.主布局 = QVBoxLayout()
        pass

    def initSlots(self):
        self.新增文件按钮.clicked.connect(self.文件列表控件.增加条目)
        self.删除选中文件按钮.clicked.connect(self.文件列表控件.删除条目)
        self.选择目标路径按钮.clicked.connect(self.选择目标文件夹)
        self.复制按钮.clicked.connect(self.执行复制任务)
        self.移动按钮.clicked.connect(self.执行移动任务)



        pass

    def initLayout(self):
        self.输入文件按钮布局.addWidget(self.新增文件按钮)
        self.输入文件按钮布局.addWidget(self.删除选中文件按钮)
        self.输入文件部分布局.addWidget(self.文件列表控件)
        self.输入文件部分布局.addLayout(self.输入文件按钮布局)
        self.输入文件部分盒子.setLayout(self.输入文件部分布局)

        self.输出文件一行布局.addWidget(self.输出提醒)
        self.输出文件一行布局.addWidget(self.输出位置输入框)
        self.输出文件一行布局.addWidget(self.选择目标路径按钮)
        self.输出文件部分布局.addLayout(self.输出文件一行布局)
        self.输出文件部分盒子.setLayout(self.输出文件部分布局)


        self.动作部分布局.addWidget(self.复制按钮)
        self.动作部分布局.addWidget(self.移动按钮)
        self.动作部分盒子.setLayout(self.动作部分布局)


        self.主布局.addWidget(self.输入文件部分盒子)
        self.主布局.addWidget(self.输出文件部分盒子)
        self.主布局.addWidget(self.动作部分盒子)
        self.setLayout(self.主布局)

        pass

    def initValue(self):
        self.文件列表控件.addItem('D:/Users/Haujet/Documents/Markdown 文档/软件笔记/Shortcut Mapper.md')
        self.文件列表控件.文件列表.append('D:/Users/Haujet/Documents/Markdown 文档/软件笔记/Shortcut Mapper.md')
        self.输出位置输入框.setText('D:/Users/Haujet/Desktop/测试md复制')
        pass

    def 选择目标文件夹(self):
        获得的路径 = QFileDialog.getExistingDirectory(self, self.tr('选择保存文件夹'))
        if 获得的路径 != '':
            self.输出位置输入框.setText(获得的路径)




    # def 选择一个文件填充到输入框(self, 文件类型, 输入框):
    #     获得的文件, _ = QFileDialog.getSaveFileName(self, self.tr('选择保存位置'), 文件类型)
    #     if file != '':
    #         self.输入框.setText(获得的文件)

    def 执行复制任务(self):
        self.转移md文档时是否为移动 = False
        self.转移md文档()

    def 执行移动任务(self):
        self.转移md文档时是否为移动 = True
        self.转移md文档()


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


    def 转移md文档(self):
        if self.转移md文档时是否为移动:
            常量.状态栏.showMessage('正在移动中')
        else:
            常量.状态栏.showMessage('正在复制中')
        self.复制附件冲突时的做法 = 0 # 0 是询问，1 是全部覆盖，2 是全部跳过
        输入文件列表 = self.文件列表控件.文件列表
        输出文件夹路径 = self.输出位置输入框.text().rstrip('/')
        if len(输入文件列表) == 0 or 输出文件夹路径 == '':
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
            搜索到的粗糙路径列表 = re.findall(r'\]\(.*?\)', 输入文件内容)
            搜索到的路径列表 = []
            if 搜索到的粗糙路径列表 != []:
                for 索引, 附件路径 in enumerate(搜索到的粗糙路径列表):
                    附件路径 = re.search(r'(?<=\]\()[^ \)]+?(?=[ \)])', 附件路径)
                    if 附件路径 == None: continue
                    附件路径 = 附件路径.group()
                    print(f'附件路径：{附件路径}')
                    搜索到的路径列表.append(附件路径)
                if not self.将文档索引的附件复制(输入文件, 搜索到的路径列表, 输出文件夹路径):
                    return False
            md文件的复制输出路径 = 输出文件夹路径 + '/' + os.path.basename(输入文件)
            if self.转移md文档时是否为移动:
                move(输入文件, md文件的复制输出路径)
            else:
                copy(输入文件, md文件的复制输出路径)
        self.复制附件冲突时的做法 = 0
        常量.状态栏.showMessage('任务完成')




    def 将文档索引的附件复制(self, 文档, 附件列表, 目标文件夹):
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
                    if self.复制附件冲突时的做法 == 1:
                        os.remove(附件复制的目标路径)
                    elif self.复制附件冲突时的做法 == 2:
                        continue
                    else:
                        是否要覆盖 = QMessageBox.question(self, '冲突', f'目标附件已存在，是否覆盖？\n\n源文件（大小 {fileSizeNormalize(os.path.getsize(附件复制的源路径))}）：\n{附件复制的源路径}\n\n目标文件（大小 {fileSizeNormalize(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n', QMessageBox.YesToAll | QMessageBox.Yes | QMessageBox.No | QMessageBox.NoToAll)
                        if 是否要覆盖 == QMessageBox.YesToAll:
                            self.复制附件冲突时的做法 = 1
                            os.remove(附件复制的目标路径)
                        elif 是否要覆盖 == QMessageBox.Yes:
                            os.remove(附件复制的目标路径)
                        elif 是否要覆盖 == QMessageBox.No:
                            continue
                        elif 是否要覆盖 == QMessageBox.NoToAll:
                            self.复制附件冲突时的做法 = 2
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




