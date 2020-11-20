
import os, threading, time

from PySide2.QtWidgets import *

from moduels.function.getHumanReadableFileSize import 得到便于阅读的文件大小
from moduels.function.downloadFileFromUrl import 下载链接文件
from moduels.function.checkDirectoryPath import 检查路径
from shutil import copy, move, rmtree

from moduels.component.NormalValue import 常量, 离线化线程常量

class TaskContent:
    """
    为了让多个进程共同修改列表，就需要一个实例化的对象，将列表作为对象的属性
    这样，一个进程修改列表后，其它进程在操作列表时，就能看到修改后的列表。
    """
    附件链接列表 = []
    文档 = None
    附件链接列表 = None
    文档内容 = None
    cookie路径 = None
    下载目标路径 = None
    目标相对文件夹路径 = None
    提醒是否要覆盖的信号 = None
    进程 = None

class LocalizeLinkListThread(threading.Thread):
    def __init__(self, 线程锁, 线程序号, 任务内容):
        super().__init__()
        self.线程锁 = 线程锁
        self.线程序号 = 线程序号
        self.任务内容 = 任务内容

    def 得到链接(self):
        """
        从任务内容的链接列表中 pop 出一个链接到 self.链接，如果没链接了，就返回 False
        """
        # print(f'{self.线程序号} 号线程：准备锁住')
        self.线程锁.acquire()
        # print(f'{self.线程序号} 号线程：锁住了')
        列表数量 = len(self.任务内容.附件链接列表)
        # print(f'{self.线程序号} 号线程：列表数量为 {列表数量}')
        if 列表数量 > 0:
            # print('{self.线程序号} 号线程：列表数量大于 0')
            self.附件链接 = self.任务内容.附件链接列表.pop()
        else:
            # print('{self.线程序号} 号线程：列表数量不大于 0，返回 False')
            离线化线程常量.可以开启下一个文件处理线程 = True
            离线化线程常量.正在工作线程数 -= 1
            self.线程锁.release()
            return False
        self.线程锁.release()
        # print('{self.线程序号} 号线程：列表数量大于 0，返回 True')
        return True

    def run(self):
        self.线程锁.acquire()
        离线化线程常量.正在工作线程数 += 1
        self.线程锁.release()
        while self.得到链接():
            附件链接 = self.附件链接
            附件复制的目标路径 = self.任务内容.下载目标路径 + '/' + os.path.basename(self.附件链接)
            转换出的相对链接 = os.path.dirname(self.任务内容.文档) + '/' + self.附件链接
            if os.path.exists(附件链接):  # 如果这个文件是本地绝对路径，就转为相对路径
                print(f'该链接为绝对路径，现将其转为相对路径：{附件链接}')
                if os.path.exists(附件复制的目标路径):
                    if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
                        os.remove(附件复制的目标路径)
                    elif 常量.有重名时的处理方式 == 2:
                        continue
                    else:
                        self.线程锁.acquire()
                        离线化线程常量.进程需要等待 = True
                        self.任务内容.提醒是否要覆盖的信号.emit('冲突',
                                        f'目标附件已存在，是否覆盖？\n\n源文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件链接))}）：\n{附件链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n')
                        while 离线化线程常量.进程需要等待:
                            self.任务内容.进程.sleep(1)
                        self.线程锁.release()
                        是否要覆盖 = 离线化线程常量.进程是否下载文件覆盖本地文件
                        if 是否要覆盖 == QMessageBox.YesToAll:
                            常量.有重名时的处理方式 = 1
                            os.remove(附件复制的目标路径)
                        elif 是否要覆盖 == QMessageBox.Yes:
                            os.remove(附件复制的目标路径)
                        elif 是否要覆盖 == QMessageBox.No:
                            continue
                        elif 是否要覆盖 == QMessageBox.NoToAll:
                            常量.有重名时的处理方式 = 2
                            continue
                copy(附件链接, 附件复制的目标路径)
                self.线程锁.acquire()
                self.任务内容.文档内容 = self.任务内容.文档内容.replace(附件链接, self.任务内容.目标相对文件夹路径 + '/' + os.path.basename(附件链接))
                self.线程锁.release()
            elif os.path.exists(转换出的相对链接):  # 如果这个链接是相对链接
                if 转换出的相对链接 != 附件复制的目标路径:  # 如果这个相对链接不是目标相对文件夹内的文件
                    if os.path.exists(附件复制的目标路径):
                        if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
                            os.remove(附件复制的目标路径)
                        elif 常量.有重名时的处理方式 == 2:
                            continue
                        else:
                            self.线程锁.acquire()
                            离线化线程常量.进程需要等待 = True
                            self.任务内容.提醒是否要覆盖的信号.emit('冲突',
                                            f'目标附件已存在，是否覆盖？\n\n源文件（大小 {得到便于阅读的文件大小(os.path.getsize(转换出的相对链接))}）：\n{转换出的相对链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n')
                            while 离线化线程常量.进程需要等待:
                                self.任务内容.进程.sleep(1)
                            self.线程锁.release()
                            是否要覆盖 = 获取进程状态的常量.进程是否下载文件覆盖本地文件
                            if 是否要覆盖 == QMessageBox.YesToAll:
                                常量.有重名时的处理方式 = 1
                                os.remove(附件复制的目标路径)
                            elif 是否要覆盖 == QMessageBox.Yes:
                                os.remove(附件复制的目标路径)
                            elif 是否要覆盖 == QMessageBox.No:
                                continue
                            elif 是否要覆盖 == QMessageBox.NoToAll:
                                常量.有重名时的处理方式 = 2
                                continue
                    move(转换出的相对链接, 附件复制的目标路径)
                    self.线程锁.acquire()
                    self.任务内容.文档内容 = self.任务内容.文档内容.replace(附件链接, self.任务内容.目标相对文件夹路径 + '/' + os.path.basename(附件链接))
                    self.线程锁.release()
                    # print(文档内容)
                else:  # 如果这个相对链接就是目标相对文件夹内的文件，那就不用复制了
                    continue
            else:  # 如果即不是本地绝对路径，也不是本地相对路径，那就尝试是不是网络路径
                下载的文件名 = 下载链接文件(self.线程序号, 附件链接, self.任务内容.下载目标路径, self.任务内容.cookie路径, self.任务内容.提醒是否要覆盖的信号, self.任务内容.进程, self.线程锁)
                if 下载的文件名 == False:
                    continue
                self.线程锁.acquire()
                self.任务内容.文档内容 = self.任务内容.文档内容.replace(附件链接, self.任务内容.目标相对文件夹路径 + '/' + 下载的文件名)
                self.线程锁.release()
                print(f'现在开始替换\n原始：{附件链接}\n替换成：{self.任务内容.目标相对文件夹路径 + "/" + 下载的文件名}')
                print('')
        # print(f'{self.线程序号} 号线程：while 跑完了')






def 将文档索引的链接本地化(文档, 附件链接列表, cookie路径, 目标相对文件夹路径, 提醒是否要覆盖的信号, 进程, 下载线程锁):
    下载目标路径 = os.path.dirname(文档) + '/' + 目标相对文件夹路径
    if not 检查路径(下载目标路径): # 先确保下载附件的文件夹存在
        return False
    任务内容 = TaskContent() # 准备好传递给线程的实例化对象
    任务内容.文档 = 文档
    任务内容.附件链接列表 = 附件链接列表
    任务内容.文档内容 = 读内容(文档)
    任务内容.cookie路径 = cookie路径
    任务内容.下载目标路径 = 下载目标路径
    任务内容.目标相对文件夹路径 = 目标相对文件夹路径
    任务内容.提醒是否要覆盖的信号 = 提醒是否要覆盖的信号
    任务内容.进程 = 进程
    线程数 = 离线化线程常量.下载附件线程数
    线程锁 = 下载线程锁
    链接列表本地化线程 = []
    print(f'下载附件线程数：{线程数}')
    for i in range(线程数):
        链接列表本地化线程.append(LocalizeLinkListThread(线程锁=线程锁, 线程序号=i, 任务内容=任务内容))
        链接列表本地化线程[i].start()
    有线程还活着 = True
    while 有线程还活着:
        for i in range(线程数):
            if 链接列表本地化线程[i].isAlive():
                有线程还活着 = True
                print(f'进程 {i} 还在工作，它正处理的链接是：{链接列表本地化线程[i].附件链接}')
                break # 只要有一个线程还在工作，就继续 sleep
            else:
                有线程还活着 = False
        if 有线程还活着:
            # print('继续等待')
            time.sleep(1)
    # print('所有线程结束')
    写内容(文档, 任务内容.文档内容)
    离线化线程常量.黑名单域名列表 = []
    return True


# def 将文档索引的链接本地化(文档, 附件链接列表, cookie路径, 目标相对文件夹路径, 提醒是否要覆盖的信号, 进程, 获取进程状态的常量):
#     下载目标路径 = os.path.dirname(文档) + '/' + 目标相对文件夹路径
#     if not 检查路径(下载目标路径):
#         return False
#     try:
#         with open(文档, 'r', encoding='utf-8') as f:
#             文档内容 = f.read()
#     except:
#         with open(文档, 'r', encoding='gbk') as f:
#             文档内容 = f.read()
#     # global 线程状态列表
#     #
#     # 线程数 = 5
#     # 线程状态列表 = [1] * 线程数
#     # 线程列表 = []
#     for 附件链接 in 附件链接列表:
#         # 下一个 = False
#         # while not 下一个:
#         #     for i in range(线程数):
#         #         if 线程状态列表[i] == 1:
#         #             continue
#         #         线程列表[] =
#         附件复制的目标路径 = 下载目标路径 + '/' + os.path.basename(附件链接)
#         转换出的相对链接 = os.path.dirname(文档) + '/' + 附件链接
#
#         if os.path.exists(附件链接):  # 如果这个文件是本地绝对路径，就转为相对路径
#             print(f'该链接为绝对路径，现将其转为相对路径：{附件链接}')
#             if os.path.exists(附件复制的目标路径):
#                 if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
#                     os.remove(附件复制的目标路径)
#                 elif 常量.有重名时的处理方式 == 2:
#                     continue
#                 else:
#                     获取进程状态的常量.进程需要等待 = True
#                     提醒是否要覆盖的信号.emit('冲突',
#                                          f'目标附件已存在，是否覆盖？\n\n源文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件链接))}）：\n{附件链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n')
#                     while 获取进程状态的常量.进程需要等待:
#                         进程.sleep(1)
#                     是否要覆盖 = 获取进程状态的常量.进程是否下载文件覆盖本地文件
#                     if 是否要覆盖 == QMessageBox.YesToAll:
#                         常量.有重名时的处理方式 = 1
#                         os.remove(附件复制的目标路径)
#                     elif 是否要覆盖 == QMessageBox.Yes:
#                         os.remove(附件复制的目标路径)
#                     elif 是否要覆盖 == QMessageBox.No:
#                         continue
#                     elif 是否要覆盖 == QMessageBox.NoToAll:
#                         常量.有重名时的处理方式 = 2
#                         continue
#             copy(附件链接, 附件复制的目标路径)
#             文档内容 = 文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + os.path.basename(附件链接))
#         elif os.path.exists(转换出的相对链接):  # 如果这个链接是相对链接
#             if 转换出的相对链接 != 附件复制的目标路径: # 如果这个相对链接不是目标相对文件夹内的文件
#                 if os.path.exists(附件复制的目标路径):
#                     if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
#                         os.remove(附件复制的目标路径)
#                     elif 常量.有重名时的处理方式 == 2:
#                         continue
#                     else:
#                         获取进程状态的常量.进程需要等待 = True
#                         提醒是否要覆盖的信号.emit('冲突',
#                                         f'目标附件已存在，是否覆盖？\n\n源文件（大小 {得到便于阅读的文件大小(os.path.getsize(转换出的相对链接))}）：\n{转换出的相对链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n')
#                         while 获取进程状态的常量.进程需要等待:
#                             进程.sleep(1)
#                         是否要覆盖 = 获取进程状态的常量.进程是否下载文件覆盖本地文件
#                         if 是否要覆盖 == QMessageBox.YesToAll:
#                             常量.有重名时的处理方式 = 1
#                             os.remove(附件复制的目标路径)
#                         elif 是否要覆盖 == QMessageBox.Yes:
#                             os.remove(附件复制的目标路径)
#                         elif 是否要覆盖 == QMessageBox.No:
#                             continue
#                         elif 是否要覆盖 == QMessageBox.NoToAll:
#                             常量.有重名时的处理方式 = 2
#                             continue
#                 move(转换出的相对链接, 附件复制的目标路径)
#                 文档内容 = 文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + os.path.basename(附件链接))
#                 # print(文档内容)
#             else: # 如果这个相对链接就是目标相对文件夹内的文件，那就不用复制了
#                 continue
#         else:  # 如果即不是本地绝对路径，也不是本地相对路径，那就尝试是不是网络路径
#             下载的文件名 = 下载链接文件(附件链接, 下载目标路径, cookie路径, 提醒是否要覆盖的信号, 进程, 获取进程状态的常量)
#             if 下载的文件名 == False:
#                 continue
#             文档内容 = 文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + 下载的文件名)
#             print(f'现在开始替换\n原始：{附件链接}\n替换成：{目标相对文件夹路径 + "/" + 下载的文件名}')
#             print('')
#     try:
#         with open(文档, 'w', encoding='utf-8') as f:
#             f.write(文档内容)
#     except:
#         with open(文档, 'w', encoding='gbk') as f:
#             f.write(文档内容)
#     离线化线程常量.黑名单域名列表 = []
#     return True

def 读内容(文件路径):
    try:
        with open(文件路径, 'r', encoding='utf-8') as f:
            文档内容 = f.read()
    except:
        with open(文件路径, 'r', encoding='gbk') as f:
            文档内容 = f.read()
    return 文档内容

def 写内容(文件路径, 内容):
    try:
        with open(文件路径, 'w', encoding='utf-8') as f:
            f.write(内容)
    except:
        with open(文件路径, 'w', encoding='gbk') as f:
            f.write(内容)

# def 本地化附件(序号, 链接, 下载目标路径):
#     global 线程状态列表
#     if os.path.exists(附件链接):  # 如果这个文件是本地绝对路径，就转为相对路径
#         附件复制的目标路径 = 下载目标路径 + '/' + os.path.basename(附件链接)
#         if os.path.exists(附件复制的目标路径):
#             if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
#                 os.remove(附件复制的目标路径)
#             elif 常量.有重名时的处理方式 == 2:
#                 线程状态列表[序号] = 1
#                 return
#             else:
#                 获取进程状态的常量.进程需要等待 = True
#                 提醒是否要覆盖的信号.emit('冲突',
#                                 f'目标附件已存在，是否覆盖？\n\n源文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件链接))}）：\n{附件链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n')
#                 while 获取进程状态的常量.进程需要等待:
#                     进程.sleep(1)
#                 是否要覆盖 = 获取进程状态的常量.进程是否要覆盖
#                 if 是否要覆盖 == QMessageBox.YesToAll:
#                     常量.有重名时的处理方式 = 1
#                     os.remove(附件复制的目标路径)
#                 elif 是否要覆盖 == QMessageBox.Yes:
#                     os.remove(附件复制的目标路径)
#                 elif 是否要覆盖 == QMessageBox.No:
#                     线程状态列表[序号] = 1
#                     return
#                 elif 是否要覆盖 == QMessageBox.NoToAll:
#                     常量.有重名时的处理方式 = 2
#                     线程状态列表[序号] = 1
#                     return
#         move(附件链接, 附件复制的目标路径)
#         文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + os.path.basename(附件链接))
#     elif os.path.exists(os.path.dirname(文档) + '/' + 附件链接):  # 如果这个链接是相对链接，那就跳过
#         线程状态列表[序号] = 1
#         return
#     else:  # 如果即不是本地绝对路径，也不是本地相对路径，那就尝试是不是网络路径
#         下载的文件名 = 下载链接文件(附件链接, 下载目标路径, cookie路径, 提醒是否要覆盖的信号, 进程, 获取进程状态的常量)
#         if 下载的文件名 == False:
#             线程状态列表[序号] = 1
#             return
#         文档内容 = 文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + 下载的文件名)
#         print(f'现在开始替换\n原始：{附件链接}\n替换成：{目标相对文件夹路径 + "/" + 下载的文件名}')
#         print('')
#         线程状态列表[序号] = 1
#         return