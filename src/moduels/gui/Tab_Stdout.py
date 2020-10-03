# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from moduels.component.Widget_StdoutBox import Widget_StdoutBox
from moduels.component.NormalValue import 常量


class Tab_Stdout(QWidget):
    def __init__(self):
        super().__init__()
        self.initElement()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayout()  # 然后布局
        self.initValue()  # 再定义各个控件的值

    def initElement(self):
        self.标准输出框 = Widget_StdoutBox()
        self.主布局 = QVBoxLayout()
        pass

    def initSlots(self):
        pass

    def initLayout(self):
        self.主布局.addWidget(self.标准输出框)
        self.setLayout(self.主布局)

    def initValue(self):
        # 常量.控制台标签页 = self
        pass

    def print(self, text):
        self.标准输出框.print(text)




