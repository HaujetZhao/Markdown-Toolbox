import sqlite3
import platform
import subprocess

class NormalValue():
    styleFile = './style.css'
    version = 'V0.0.01'
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
    离线化进程是否要覆盖 = None
    离线化进程需要等待 = False

class LocalizeThreadNormalValue():
    进程是否要覆盖 = None
    进程需要等待 = False
    黑名单域名列表 = []

class ClearThreadNormalValue():
    是否确认要删除找到的无用文件 = False
    进程需要等待 = False


常量 = NormalValue()
离线化进程常量 = LocalizeThreadNormalValue()
清理化进程常量 = ClearThreadNormalValue()

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
