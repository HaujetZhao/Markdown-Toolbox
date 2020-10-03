import sqlite3
import platform
import subprocess

class NormalValue():
    styleFile = './style.css'
    version = 'V0.0.01'
    mainWindow = None
    状态栏 = None
    系统平台 = platform.system()
    有重名时的处理方式 = 0
    复制功能标签页 = None
    离线化功能标签页 = None
    离线化进程是否要覆盖 = None
    离线化进程需要等待 = False

class LocalizeThreadNormalValue():
    进程是否要覆盖 = None
    进程需要等待 = False
    黑名单域名列表 = []


常量 = NormalValue()
离线化进程常量 = LocalizeThreadNormalValue()
