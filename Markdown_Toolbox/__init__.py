# -*- coding: UTF-8 -*-

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__))) # 更改工作目录，指向正确的当前文件夹
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # 将当前目录导入 python 寻找 package 和 moduel 的变量

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from moduels.component.NormalValue import 常量
from moduels.gui.MainWindow import MainWindow
from moduels.gui.SystemTray import SystemTray

from moduels.function.createDB import 准备数据库 # 引入检查和创建创建数据库的函数

def 高分屏变量设置(app):
    os.environ['QT_SCALE_FACTOR'] = '1'
    QCoreApplication.instance().setAttribute(Qt.AA_UseHighDpiPixmaps)


############# 主窗口和托盘 ################

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    高分屏变量设置(app)
    准备数据库()
    mainWindow = MainWindow()
    常量.主窗口 = mainWindow
    tray = SystemTray(mainWindow)
    常量.托盘 = tray
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
