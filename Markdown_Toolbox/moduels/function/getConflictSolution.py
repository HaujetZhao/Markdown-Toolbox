# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from moduels.component.NormalValue import 常量
from moduels.function.compareTwoFiles import 文件大小比较新旧文件是否相同, MD5比较新旧文件是否相同
from moduels.function.getHumanReadableFileSize import 得到便于阅读的文件大小
import os, webbrowser, pathlib

def 处理相同文件名冲突(对象, 附件复制的源路径Path, 附件复制的目标路径Path):

    # 判断新文件与旧文件是否相同
    if 对象.判断文件是否相同的方式 == 0:
        if os.path.isdir(附件复制的源路径Path) != os.path.isdir(附件复制的目标路径Path):
            是否相同, 旧文件大小, 新文件大小 = False, 0, 0 # 如果是文件和文件夹比较，就直接返回否
        else:
            是否相同, 旧文件大小, 新文件大小 = 文件大小比较新旧文件是否相同(附件复制的源路径Path, 附件复制的目标路径Path)
    elif 对象.判断文件是否相同的方式 == 1:
        if os.path.isdir(附件复制的源路径Path) != os.path.isdir(附件复制的目标路径Path):
            是否相同, 旧文件大小, 新文件大小 = False, 0, 0 # 如果是文件和文件夹比较，就直接返回否
        else:
            大小是否相同, 旧文件大小, 新文件大小 = 文件大小比较新旧文件是否相同(附件复制的源路径Path, 附件复制的目标路径Path)
            if 大小是否相同:
                MD5是否相同, 旧文件MD5, 新文件MD5 = MD5比较新旧文件是否相同(附件复制的源路径Path, 附件复制的目标路径Path)
                if MD5是否相同:
                    是否相同 = True
                else:
                    是否相同 = False
            else:
                是否相同 = False

    # 相同则不处理，不同则处理
    if 是否相同:
        return True, '跳过', 附件复制的目标路径Path
    else:

        # 得到冲突处理方式
        if 对象.文件冲突处理方式 not in [1, 2, 3]:
            询问内容 = f'''
发现文件名冲突，请选择处理方式！

原文件：
    路径：{附件复制的源路径Path}
    大小：{得到便于阅读的文件大小(新文件大小)}

目标路径：
    路径：{附件复制的目标路径Path}
    大小：{得到便于阅读的文件大小(旧文件大小)}
            '''
            对象.文件冲突处理方式 = getConflictSolution(对象, 询问内容)

        # 如果覆盖就把冲突的文件删掉
        if 对象.文件冲突处理方式 in [1, 4]:  # 覆盖
            return False, '覆盖', 附件复制的目标路径Path

        # 如果跳过就处理下一个
        elif 对象.文件冲突处理方式 in [2, 5]:  # 跳过
            return False, '跳过', 附件复制的目标路径Path

        # 如果保留二者就改变附件路径，并修改文档内容
        elif 对象.文件冲突处理方式 in [3, 6]:  # 保留二者

            # 得到附件新路径
            附件目标文件夹 = 附件复制的目标路径Path.parent
            附件目标旧文件名 = 附件复制的目标路径Path.stem
            附件目标拓展名 = 附件复制的目标路径Path.suffix

            附件目标文件名 = 附件目标旧文件名
            新增序号 = 1
            while pathlib.Path(附件目标文件夹, 附件目标文件名 + 附件目标拓展名).exists():
                新增序号 += 1
                附件目标文件名 = 附件目标旧文件名 + str(新增序号)
            附件复制的目标路径Path = pathlib.Path(附件目标文件夹, 附件目标文件名 + 附件目标拓展名)

            return False, '保留二者', 附件复制的目标路径Path

def getConflictSolution(parent, 文本):
    提问对话框 = QMessageBox(parent)
    提问对话框.setIcon(QMessageBox.Question)
    提问对话框.setWindowTitle('冲突')
    提问对话框.setText(文本)

    覆盖按钮 = 提问对话框.addButton('覆盖', QMessageBox.ActionRole)
    全部覆盖按钮 = 提问对话框.addButton('全部覆盖', QMessageBox.ActionRole)
    跳过按钮 = 提问对话框.addButton('跳过', QMessageBox.ActionRole)
    全部跳过按钮 = 提问对话框.addButton('全部跳过', QMessageBox.ActionRole)
    保留二者按钮 = 提问对话框.addButton('保留二者', QMessageBox.ActionRole)
    全部保留二者按钮 = 提问对话框.addButton('全部保留二者', QMessageBox.ActionRole)

    提问对话框.exec_()
    if 提问对话框.clickedButton() == 全部覆盖按钮:
        return 1
    elif 提问对话框.clickedButton() == 全部跳过按钮:
        return 2
    elif 提问对话框.clickedButton() == 全部保留二者按钮:
        return 3
    if 提问对话框.clickedButton() == 覆盖按钮:
        return 4
    elif 提问对话框.clickedButton() == 跳过按钮:
        return 5
    elif 提问对话框.clickedButton() == 保留二者按钮:
        return 6