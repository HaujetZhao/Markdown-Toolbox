# -*- coding: UTF-8 -*-

import os
import re

from PySide2.QtCore import *
from PySide2.QtWidgets import *

from moduels.component.NormalValue import 常量


class Widget_FileList(QListWidget):
    """这个列表控件可以拖入文件"""
    # signal = Signal(list)
    正则匹配样式  = r'.+\.md$'
    选择文件时候的提示  = '选择要添加的 md 文件'
    选择文件时候的过滤器  = 'MD文档 (*.md)'
    需要验证为文件 = True
    需要验证为文件夹 = False

    def __init__(self, parent=None):
        super(Widget_FileList, self).__init__(parent)
        self.路径列表 = []
        self.setAcceptDrops(True)
        self.doubleClicked.connect(self.被双击)

    def enterEvent(self, a0: QEvent) -> None:
        常量.状态栏.showMessage(self.tr('双击列表项可以清空文件列表'))

    def leaveEvent(self, a0: QEvent) -> None:
        常量.状态栏.showMessage('')

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                文件路径 = str(url.toLocalFile())
                if self.验证文件路径(文件路径):
                    self.路径列表.append(str(url.toLocalFile()))
            self.刷新列表()
        else:
            event.ignore()

    def 验证文件路径(self, 文件路径):
        路径是否为文件夹 = os.path.isdir(文件路径)
        路径是否为文件 = os.path.isfile(文件路径)
        if not re.match(self.正则匹配样式, 文件路径):
            return False
        if 文件路径 in self.路径列表:
            return False
        if self.需要验证为文件 and 路径是否为文件:
            return True
        elif self.需要验证为文件夹 and 路径是否为文件夹:
            return True
        return False

    def 刷新列表(self):
        self.clear()
        for item in self.路径列表:
            item =  '.../' + os.path.basename(os.path.dirname(os.path.dirname(item))) + '/' + os.path.basename(os.path.dirname(item)) + '/' + os.path.basename(item)
            self.addItem(item)
        # self.addItems(self.文件列表)

    def 删除条目(self):
        条目序号 = self.currentRow()
        print(条目序号)
        if 条目序号 < 0:
            return
        self.路径列表.pop(条目序号)
        self.刷新列表()
        if len(self.路径列表) > 条目序号:
            self.setCurrentRow(条目序号)
        elif len(self.路径列表) == 0:
            pass
        elif len(self.路径列表) == 条目序号:
            self.setCurrentRow(条目序号 - 1)

    def 增加条目(self):
        if self.需要验证为文件夹:
            路径 = QFileDialog.getExistingDirectory(self, self.选择文件时候的提示)
            if self.验证文件路径(路径):
                self.路径列表.append(路径)
        elif self.需要验证为文件:
            路径列表 = QFileDialog.getOpenFileNames(self, self.选择文件时候的提示, filter=self.选择文件时候的过滤器)[0]
            for 路径 in 路径列表:
                if self.验证文件路径(路径):
                    self.路径列表.append(路径)
        self.刷新列表()

    def 上移条目(self, 条目序号):
        pass

    def 下移条目(self, 条目序号):
        pass

    def 被双击(self):
        result = QMessageBox.warning(self, self.tr('清空列表'), self.tr('是否确认清空列表？'), QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.路径列表 = []
            self.刷新列表()

