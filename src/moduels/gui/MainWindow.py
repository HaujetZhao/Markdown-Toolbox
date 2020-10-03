# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.NormalValue import 常量

# try:
from moduels.gui.Tab_CopyMdFile import Tab_CopyMdFile
from moduels.gui.Tab_LocalizeMdFile import Tab_LocalizeMdFile




import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.loadStyleSheet()
        self.initElement()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayout()  # 然后布局
        self.initValue()  # 再定义各个控件的值
        self.show()



        # self.setWindowState(Qt.WindowMaximized)
        # sys.stdout = Stream(newText=self.onUpdateText)

    def initElement(self):
        self.状态栏 = self.statusBar()
        self.标签页控件 = QTabWidget() # 定义中心控件为多 tab 页面

        self.复制功能标签页 = Tab_CopyMdFile()
        self.离线化功能标签页 = Tab_LocalizeMdFile()

        # self.adjustSize()
        # if 常量.platfm == 'Darwin':
        #     self.setWindowIcon(QIcon('misc/icon.icns'))
        # else:
        #     self.setWindowIcon(QIcon('misc/icon.ico'))
        # self.setWindowTitle('Quick Cut')

        #


    def initSlots(self):
        pass

    def initLayout(self):
        self.setCentralWidget(self.标签页控件)
        self.标签页控件.addTab(self.复制功能标签页, self.tr('复制'))
        self.标签页控件.addTab(self.离线化功能标签页, self.tr('离线化'))

    def initValue(self):
        常量.状态栏 = self.状态栏
        self.setWindowTitle('MarkDown 工具箱')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)  # 始终在前台
        pass


    def loadStyleSheet(self):
        try:
            try:
                with open(常量.styleFile, 'r', encoding='utf-8') as style:
                    self.setStyleSheet(style.read())
            except:
                with open(常量.styleFile, 'r', encoding='gbk') as style:
                    self.setStyleSheet(style.read())
        except:
            QMessageBox.warning(self, self.tr('主题载入错误'), self.tr('未能成功载入主题，请确保软件根目录有 "style.css" 文件存在。'))

    def keyPressEvent(self, event) -> None:
        # 在按下 F5 的时候重载 style.css 主题
        if (event.key() == Qt.Key_F5):
            self.loadStyleSheet()
            self.status.showMessage('已成功更新主题', 800)


    # def closeEvent(self, event):
    #     """Shuts down application on close."""
    #     # Return stdout to defaults.
    #     if 常量.mainWindow.ConfigTab.hideToSystemTraySwitch.isChecked():
    #         event.ignore()
    #         self.hide()
    #     else:
    #         sys.stdout = sys.__stdout__
    #         super().closeEvent(event)
