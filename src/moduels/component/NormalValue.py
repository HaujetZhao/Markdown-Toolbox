import platform
import sqlite3


class NormalValue():
    样式文件 = 'misc/style.css'
    软件版本 = '1.0.0'

    主窗口 = None
    托盘 = None
    状态栏 = None

    数据库路径 = 'misc/database.db'
    数据库连接 = sqlite3.connect(数据库路径)

    偏好设置表单名 = 'Preference'

    关闭时隐藏到托盘 = False

    系统平台 = platform.system()
    图标路径 = 'misc/icon.icns' if 系统平台 == 'Darwin' else 'misc/icon.ico'

    离线化子线程数 = 30
    检查链接超时时长 = 10

    判断文件是否相同的方式 = 0
    文件冲突默认处理方式 = 0

    复制功能标签页 = None
    离线化功能标签页 = None

#
# class CopyAndMoveThreadNormalValue():
#     '''
#     复制和移动文档线程中的常量
#     '''
#     有重名但不同的文件时的处理方式 = 0
#     进程需要等待 = False
#     回复数值 = 0 # 0 表示
#
# class LocalizeThreadNormalValue():
#     '''
#     离线化线程中的常量
#     '''
#     有重名但不同的文件时的处理方式 = 0
#     进程需要等待 = False
#     回复数值 = 0
#
#     黑名单域名列表 = []
#
#     检查链接超时时长 = 5
#
#     下载附件线程数 = 30
#     正在工作线程数 = 0
#     可以开启下一个文件处理线程 = False


class ClearThreadNormalValue():
    '''
    清理线程中的常量
    '''
    是否确认要删除找到的无用文件 = False
    进程需要等待 = False


常量 = NormalValue()
# 复制和移动文档线程常量 = CopyAndMoveThreadNormalValue()
# 离线化线程常量 = LocalizeThreadNormalValue()
清理化线程常量 = ClearThreadNormalValue()



