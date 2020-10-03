
import os

from moduels.function.得到便于阅读的文件大小 import 得到便于阅读的文件大小
from moduels.function.下载链接文件 import 下载链接文件
from moduels.function.检查路径 import 检查路径

def 将文档索引的链接本地化(文档, 附件链接列表, cookie路径, 目标相对文件夹路径, 提醒是否要覆盖的信号, 进程, 获取进程状态的常量):
    下载目标路径 = os.path.dirname(文档) + '/' + 目标相对文件夹路径
    if not 检查路径(下载目标路径):
        return False
    try:
        with open(文档, 'r', encoding='utf-8') as f:
            文档内容 = f.read()
    except:
        with open(文档, 'r', encoding='gbk') as f:
            文档内容 = f.read()
    for 附件链接 in 附件链接列表:
        if os.path.exists(附件链接):  # 如果这个文件是本地绝对路径，就转为相对路径
            目标文件完整路径 = 下载目标路径 + '/' + os.path.basename(附件链接)
            if os.path.exists(目标文件完整路径):
                if 常量.有重名时的处理方式 == 1:  # 0 是询问，1 是全部覆盖，2 是全部跳过
                    os.remove(附件复制的目标路径)
                elif 常量.有重名时的处理方式 == 2:
                    continue
                else:
                    获取进程状态的常量.进程需要等待 = True
                    提醒是否要覆盖的信号.emit('冲突',
                                         f'目标附件已存在，是否覆盖？\n\n源文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件链接))}）：\n{附件链接}\n\n目标文件（大小 {得到便于阅读的文件大小(os.path.getsize(附件复制的目标路径))}）：\n{附件复制的目标路径}\n\n')
                    while 获取进程状态的常量.进程需要等待:
                        进程.sleep(1)
                    是否要覆盖 = 获取进程状态的常量.进程是否要覆盖
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
            move(附件链接, 目标文件完整路径)
            文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + os.path.basename(附件链接))
        elif os.path.exists(os.path.dirname(文档) + '/' + 附件链接):  # 如果这个链接是相对链接，那就跳过
            continue
        else:  # 如果即不是本地绝对路径，也不是本地相对路径，那就尝试是不是网络路径
            下载的文件名 = 下载链接文件(附件链接, 下载目标路径, cookie路径, 提醒是否要覆盖的信号, 进程, 获取进程状态的常量)
            if 下载的文件名 == False:
                continue
            文档内容 = 文档内容.replace(附件链接, 目标相对文件夹路径 + '/' + 下载的文件名)
            print(f'现在开始替换\n原始：{附件链接}\n替换成：{目标相对文件夹路径 + "/" + 下载的文件名}')
            print('')
    try:
        with open(文档, 'w', encoding='utf-8') as f:
            f.write(文档内容)
    except:
        with open(文档, 'w', encoding='gbk') as f:
            f.write(文档内容)
    return True