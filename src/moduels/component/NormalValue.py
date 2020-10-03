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

常量 = NormalValue()
