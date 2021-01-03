# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量
from moduels.component.Widget_FileList import Widget_FileList
from moduels.component.Widget_FileLineEdit import Widget_FileLineEdit
from moduels.function.getHumanReadableFileSize import 得到便于阅读的文件大小
from moduels.function.getAllUrlFromString import 从字符串搜索到所有附件路径
from moduels.function.getConflictSolution import 处理相同文件名冲突


import os, re, pathlib

from shutil import copy, move

class Tab_CopyMdFile(QWidget):
    状态栏消息 = Signal(str, int)
    def __init__(self):
        super().__init__()
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值

    def initElements(self):
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

    def initSlots(self):
        self.新增文件按钮.clicked.connect(self.文件列表控件.增加条目)
        self.删除选中文件按钮.clicked.connect(self.文件列表控件.删除条目)
        self.选择目标路径按钮.clicked.connect(self.选择目标文件夹)
        self.复制按钮.clicked.connect(self.执行复制任务)
        self.移动按钮.clicked.connect(self.执行移动任务)

    def initLayouts(self):
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

    def initValues(self):
        self.文件列表控件.需要验证为文件 = True
        self.文件列表控件.需要验证为文件夹 = False
        self.文件列表控件.正则匹配样式 = r'.+\.md$'
        self.文件列表控件选择文件时候的提示 = '选择要添加的 md 文件'
        self.文件列表控件选择文件时候的过滤器 = 'MD文档 (*.md)'
        常量.复制功能标签页 = self
        # self.test()
        pass

    def 选择目标文件夹(self):
        获得的路径 = QFileDialog.getExistingDirectory(self, self.tr('选择保存文件夹'))
        if 获得的路径 != '':
            self.输出位置输入框.setText(获得的路径)

    def 执行复制任务(self):
        self.转移md文档时是否为移动 = False
        self.转移md文档()

    def 执行移动任务(self):
        self.转移md文档时是否为移动 = True
        self.转移md文档()

    def 得到文件内容(self, 输入文件):
        try:
            with open(输入文件, 'r', encoding='utf-8') as f:
                文件内容 = f.read()
        except:
            with open(输入文件, 'r', encoding='gbk') as f:
                文件内容 = f.read()
        return 文件内容

    def 转移md文档(self):
        # 得到输入输出列表，判断是否继续
        if len(self.文件列表控件.路径列表) == 0 or self.输出位置输入框.text() == '':
            常量.状态栏.showMessage('输入文件不存在或输出文件夹为空，无法继续', 1000)
            return
        输入文件Path列表 = [pathlib.Path(x) for x in self.文件列表控件.路径列表]
        输出文件夹Path = pathlib.Path(self.输出位置输入框.text())

        # 禁用组件，避免多次执行
        执行期间要禁用的控件 = [self.移动按钮, self.复制按钮]
        for 控件 in 执行期间要禁用的控件:
            控件.setDisabled(True)

        # 状态栏提示信息
        if self.转移md文档时是否为移动:
            常量.状态栏.showMessage('正在移动中')
        else:
            常量.状态栏.showMessage('正在复制中')

        # 初始化文件冲突相关变量
        self.判断文件是否相同的方式 = 常量.判断文件是否相同的方式
        self.文件冲突处理方式 = 常量.文件冲突处理方式

        # 对文件列表开始循环
        for 输入文件Path in 输入文件Path列表:

            # 判断输入文件是否存在
            print(f'输入文件：{输入文件Path}')
            if not 输入文件Path.exists():
                print(f'源文件不存在，故跳过：{输入文件Path}\n')
                continue

            # 得到输入文件内容
            self.输入文件内容 = self.得到文件内容(输入文件Path)
            self.新文档内容有作修改 = False

            # 得到输入文件附件列表
            搜索到的路径字符串列表 = 从字符串搜索到所有附件路径(self.输入文件内容) # 从文档内容得到链接列表

            # 复制或移动所有附件
            if 搜索到的路径字符串列表 != []:
                if self.复制或移动文档内的相对路径附件(输入文件Path, 搜索到的路径字符串列表, 输出文件夹Path): # 将链接列表中的附件全都复制移动
                    ...
                else:
                    return False

            # 得到文档目标路径
            Md文件的输出目标Path = 输出文件夹Path / 输入文件Path.name

            if Md文件的输出目标Path.exists():
                新旧文件相同, 处理手段, Md文件的输出目标Path = 处理相同文件名冲突(self, 输入文件Path, Md文件的输出目标Path)

                if not 新旧文件相同:
                    if 处理手段 == '保留二者':...
                    elif 处理手段 == '跳过':continue
                    elif 处理手段 == '覆盖':os.remove(Md文件的输出目标Path)
                else:
                    print(f'''遇到同名相同文件，跳过：
    源文件：{输入文件Path}
    目标文件：{Md文件的输出目标Path}\n''')
                    continue
            # 复制或移动文档
            print('开始转移文档')
            try:
                self.检查文件夹路径(Md文件的输出目标Path.parent)
                if self.转移md文档时是否为移动: # 再将文档文件本身移动
                    move(输入文件Path, Md文件的输出目标Path)
                    print(f'成功移动文件：\n    输入：{输入文件Path}\n    输出：{Md文件的输出目标Path}')
                else:
                    copy(输入文件Path, Md文件的输出目标Path)
                    print(f'成功复制文件：\n    输入：{输入文件Path}\n    输出：{Md文件的输出目标Path}')
            except:
                print(f'无法将 {输入文件Path} 移动到指定位置 {Md文件的输出目标Path}')
                continue

            # 如果文档内容有修改，写入新内容
            if self.新文档内容有作修改:
                with open(Md文件的输出目标Path, 'w', encoding='utf-8') as f:
                    f.write(self.输入文件内容)

        # 恢复禁用的按钮，显示成功
        for 控件 in 执行期间要禁用的控件:控件.setEnabled(True)
        常量.状态栏.showMessage('任务完成')

    def 复制或移动文档内的相对路径附件(self, 文档Path, 附件字符串路径列表, 文档目标文件夹Path):

        # 先得到文档所在文件夹
        文档所在文件夹Path = 文档Path.parent

        # 得到所有的有效的相对路径
        有效相对路径Path列表 = set()
        for 附件路径 in 附件字符串路径列表:

            # 得到附件绝对路径
            绝对路径Path = 文档所在文件夹Path / 附件路径

            # 如果附件绝对路径不存在，则返回
            if not os.path.exists(绝对路径Path): continue

            # 如果附件路径是文件，加入列表
            if 绝对路径Path.is_file():
                有效相对路径Path列表.add(pathlib.Path(附件路径))

            # 如果附件路径是文件夹，将其中的文件迭代加入列表
            elif 绝对路径Path.is_dir():
                有效相对路径Path列表 |= self.迭代得到文件夹Path下的文件(文档所在文件夹Path, pathlib.Path(附件路径))
                # 遍历得到这个文件夹下的所有文件相对于文档的相对路径
                ...

        # 对文档中有效的的相对路径附件开始循环
        for 附件路径Path in 有效相对路径Path列表:

            # 得到附件源路径和目标路径
            附件相对路径Path = 附件路径Path
            附件绝对路径Path = 文档所在文件夹Path / 附件相对路径Path
            附件目标绝对路径Path = 文档目标文件夹Path  / 附件相对路径Path
            if not self.检查文件夹路径(附件目标绝对路径Path.parent): # 创建目标相对路径
                print('这张图片的目标路径文件夹无法创建，继续下一份附件')
                continue

            # 检查附件是不是文件夹
            附件是文件夹 = 附件绝对路径Path.is_dir()

            # 如果目标路径冲突
            if 附件目标绝对路径Path.exists():

                # 得到文件是否相同，并从对话框得到文件不同时的处理方式
                新旧文件相同, 处理手段, 附件目标绝对路径Path = 处理相同文件名冲突(self, 附件绝对路径Path, 附件目标绝对路径Path)

                # 如果新旧文件不同，进行处理
                if not 新旧文件相同:

                    if 处理手段 == '保留二者':

                        # 标记文档内容已做修改
                        if not self.新文档内容有作修改:
                            self.新文档内容有作修改 = True

                        # 将文档内容中的旧路径改为新路径
                        附件目标旧文件名 = 附件相对路径Path.name
                        附件目标新文件名 = 附件目标绝对路径Path.name
                        附件新相对路径 = str(附件相对路径Path).replace(附件目标旧文件名, 附件目标新文件名)
                        self.输入文件内容 = self.输入文件内容.replace(附件相对路径Path, 附件新相对路径)

                    elif 处理手段 == '跳过':
                        continue

                    elif 处理手段 == '覆盖':
                        os.remove(附件复制的目标路径)

                # 如果新旧文件相同，则跳过
                else:
                    print(f'''遇到同名相同文件，跳过：
    源文件：{附件绝对路径Path}
    目标文件：{附件目标绝对路径Path}\n''')
                    continue

            # 复制或移动附件
            try:
                if self.转移md文档时是否为移动:
                    move(附件绝对路径Path, 附件目标绝对路径Path)
                else:
                    copy(附件绝对路径Path, 附件目标绝对路径Path)
            except:
                print(f'''一份附件复制失败，有可能是多个文档共同引用这个文件，移动其他文档的时候，已经将这个文件转移过去了：
    源文件：{附件绝对路径Path}
    目标文件：{附件目标绝对路径Path}\n''')

        return True


        ...

    def 检查文件夹路径(self, 文件夹路径Path):
        '''
        确保一个文件夹路径存在
        '''
        if not 文件夹路径Path.exists():
            try:
                文件夹路径Path.mkdir(parents=True)
                return True
            except Exception:
                print(Exception)
                return False
        else:
            return True

    def 迭代得到文件夹Path下的文件(self, 文档所在文件夹Path, 文件夹Path: pathlib.Path):
        文件Path列表 = set()
        for item in (文档所在文件夹Path / 文件夹Path).iterdir():
            if item.is_file():
                文件Path列表.add(item.relative_to(文档所在文件夹Path))
            elif item.is_dir():
                文件Path列表 |= self.迭代得到文件夹Path下的文件(文档所在文件夹Path, item)
        return 文件Path列表

    def test(self):
        return False
        import shutil
        用于重置的文件夹 = 'D:/Users/Haujet/Desktop/MD 工具箱测试/复制和移动测试/_测试源'
        用于测试的文件夹 = 'D:/Users/Haujet/Desktop/MD 工具箱测试/复制和移动测试/源'
        用于测试的文件 = 'D:/Users/Haujet/Desktop/MD 工具箱测试/复制和移动测试/源/弹跳.md'
        shutil.rmtree(用于测试的文件夹)
        os.makedirs(用于测试的文件夹)
        shutil.copytree(用于重置的文件夹, 用于测试的文件夹, dirs_exist_ok=True)
        self.文件列表控件.路径列表.append(用于测试的文件)
        self.文件列表控件.刷新列表()
        self.输出位置输入框.setText('D:/Users/Haujet/Desktop/MD 工具箱测试/复制和移动测试/目标')