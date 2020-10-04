# -*- coding: UTF-8 -*-

from PySide2.QtWidgets import *
from moduels.component.NormalValue import 常量
from moduels.component.SponsorDialog import SponsorDialog

import os, webbrowser


class Tab_Help(QWidget):
    def __init__(self):
        super().__init__()
        self.initElement()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayout()  # 然后布局
        self.initValue()  # 再定义各个控件的值

    def initElement(self):
        self.openHelpFileButton = QPushButton(self.tr('打开帮助文档'))
        self.ffmpegMannualNoteButton = QPushButton(self.tr('查看作者的 FFmpeg 笔记'))
        self.openVideoHelpButtone = QPushButton(self.tr('查看视频教程'))
        self.openGiteePage = QPushButton(self.tr('当前版本是 %s，到 Gitee 检查新版本') % 常量.version)
        self.openGithubPage = QPushButton(self.tr('当前版本是 %s，到 Github 检查新版本') % 常量.version)
        self.linkToDiscussPage = QPushButton(self.tr('加入 QQ 群'))
        self.tipButton = QPushButton(self.tr('打赏作者'))

        self.masterLayout = QVBoxLayout()

    def initSlots(self):
        self.openHelpFileButton.clicked.connect(self.openHelpDocument)
        self.ffmpegMannualNoteButton.clicked.connect(lambda: webbrowser.open(self.tr(r'https://hacpai.com/article/1595480295489')))
        self.openVideoHelpButtone.clicked.connect(lambda: webbrowser.open(self.tr(r'https://www.bilibili.com/video/BV18T4y1E7FF/')))
        self.openGiteePage.clicked.connect(lambda: webbrowser.open(self.tr(r'https://gitee.com/haujet/Markdown-Toolbox/releases')))
        self.openGithubPage.clicked.connect(lambda: webbrowser.open(self.tr(r'https://github.com/HaujetZhao/Markdown-Toolbox/releases')))
        self.linkToDiscussPage.clicked.connect(lambda: webbrowser.open(
            self.tr(r'https://qm.qq.com/cgi-bin/qm/qr?k=DgiFh5cclAElnELH4mOxqWUBxReyEVpm&jump_from=webapi')))
        self.tipButton.clicked.connect(lambda: SponsorDialog())

    def initLayout(self):
        self.setLayout(self.masterLayout)
        self.masterLayout.addWidget(self.openHelpFileButton)
        # self.masterLayout.addWidget(self.ffmpegMannualNoteButton)
        # self.masterLayout.addWidget(self.openVideoHelpButtone)
        self.masterLayout.addWidget(self.openGiteePage)
        self.masterLayout.addWidget(self.openGithubPage)
        self.masterLayout.addWidget(self.linkToDiscussPage)
        self.masterLayout.addWidget(self.tipButton)

    def initValue(self):
        self.openHelpFileButton.setMaximumHeight(100)
        self.ffmpegMannualNoteButton.setMaximumHeight(100)
        self.openVideoHelpButtone.setMaximumHeight(100)
        self.openGiteePage.setMaximumHeight(100)
        self.openGithubPage.setMaximumHeight(100)
        self.linkToDiscussPage.setMaximumHeight(100)
        self.tipButton.setMaximumHeight(100)

    def openHelpDocument(self):
        try:
            if 常量.platfm == 'Darwin':
                import shlex
                os.system("open " + shlex.quote(self.tr("./misc/笔记/README_zh.html")))
            elif 常量.platfm == 'Windows':
                os.startfile(os.path.realpath(self.tr('./misc/笔记/README_zh.html')))
        except:
            print('未能打开帮助文档')
