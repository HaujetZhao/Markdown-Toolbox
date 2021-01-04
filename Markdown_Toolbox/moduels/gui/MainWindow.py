# -*- coding: UTF-8 -*-

import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from moduels.component.NormalValue import 常量
from moduels.gui.Tab_ClearAttatchment import Tab_ClearAttatchment
from moduels.gui.Tab_Config import Tab_Config
# try:
from moduels.gui.Tab_CopyMdFile import Tab_CopyMdFile
from moduels.gui.Tab_Help import Tab_Help
from moduels.gui.Tab_LocalizeMdFile import Tab_LocalizeMdFile
from moduels.gui.Tab_Stdout import Tab_Stdout


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.loadStyleSheet()
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值


        # self.setWindowState(Qt.WindowMaximized)
        # sys.stdout = Stream(newText=self.onUpdateText)

    def initElements(self):
        self.状态栏 = self.statusBar()
        self.标签页控件 = QTabWidget() # 定义中心控件为多 tab 页面

        self.设置标签页 = Tab_Config()

        self.复制功能标签页 = Tab_CopyMdFile()
        self.离线化功能标签页 = Tab_LocalizeMdFile()
        self.清理功能标签页 = Tab_ClearAttatchment()
        self.控制台标签页 = Tab_Stdout()
        self.帮助标签页 = Tab_Help()

    def initSlots(self):
        self.复制功能标签页.状态栏消息.connect(lambda 消息, 时间: self.状态栏.showMessage(消息, 时间))
        self.离线化功能标签页.状态栏消息.connect(lambda 消息, 时间: self.状态栏.showMessage(消息, 时间))
        self.清理功能标签页.状态栏消息.connect(lambda 消息, 时间: self.状态栏.showMessage(消息, 时间))

    def initLayouts(self):
        self.setCentralWidget(self.标签页控件)
        self.标签页控件.addTab(self.复制功能标签页, self.tr('复制'))
        self.标签页控件.addTab(self.离线化功能标签页, self.tr('离线化'))
        self.标签页控件.addTab(self.清理功能标签页, self.tr('清理'))
        # self.标签页控件.addTab(self.控制台标签页, self.tr('控制台'))
        self.标签页控件.addTab(self.设置标签页, self.tr('设置'))
        self.标签页控件.addTab(self.帮助标签页, self.tr('帮助'))

    def initValues(self):
        # self.窗口标题 = 'MarkDown 工具箱'
        常量.状态栏 = self.状态栏
        self.setWindowTitle('MarkDown 工具箱')
        self.setWindowIcon(QIcon(常量.图标路径))
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 始终在前台
        self.show()

    def loadStyleSheet(self):
        try:
            try:
                with open(常量.样式文件, 'r', encoding='utf-8') as style:
                    self.setStyleSheet(style.read())
            except:
                with open(常量.样式文件, 'r', encoding='gbk') as style:
                    self.setStyleSheet(style.read())
        except:
            QMessageBox.warning(self, self.tr('主题载入错误'), self.tr('未能成功载入主题，请确保软件 misc 目录有 "style.css" 文件存在。'))

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if (event.key() == Qt.Key_F5):
            self.loadStyleSheet()
            self.状态栏.showMessage('已成功更新主题', 800)

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        if 常量.关闭时隐藏到托盘:
            event.ignore()
            self.hide()
        else:
            sys.stdout = sys.__stdout__
            super().closeEvent(event)
