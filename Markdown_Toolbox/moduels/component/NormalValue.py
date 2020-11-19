import sqlite3
import platform
import subprocess

class NormalValue():
    styleFile = './style.css'
    version = 'V0.0.7'
    mainWindow = None
    tray = None
    数据库路径 = 'misc/database.db'
    数据库连接 = sqlite3.connect(数据库路径)
    数据库偏好设置表单名 = 'Preference'
    状态栏 = None
    系统平台 = platform.system()
    有重名时的处理方式 = 0
    复制功能标签页 = None
    离线化功能标签页 = None

class ThreadNormalValue():
    # 进程常量
    有重名时的处理方式 = 0
    进程需要等待 = False
    主进程提示框回复值 = 0 # 0 表示


class TransportThreadNormalValue():
    有重名时的处理方式 = 0
    进程需要等待 = False
    回复数值 = 0 # 0 表示

class LocalizeThreadNormalValue():
    进程是否下载文件覆盖本地文件 = None
    进程需要等待 = False
    黑名单域名列表 = []
    检查链接超时时长 = 10

class ClearThreadNormalValue():
    是否确认要删除找到的无用文件 = False
    进程需要等待 = False


常量 = NormalValue()
转移线程常量 = TransportThreadNormalValue()
离线化线程常量 = LocalizeThreadNormalValue()
清理化线程常量 = ClearThreadNormalValue()

def 初始化数据库():
    cursor = 常量.数据库连接.cursor()
    result = cursor.execute(f'select * from sqlite_master where name = "{常量.数据库偏好设置表单名}";')  # 检查初始偏好设置表在不在数据库
    if result.fetchone() == None:
        cursor.execute(f'''create table {常量.数据库偏好设置表单名} (
                                                id integer primary key autoincrement,
                                                item text,
                                                value text
                                                )''')
        常量.数据库连接.commit()
    else:
        print('偏好设置表单已存在')

初始化数据库()
