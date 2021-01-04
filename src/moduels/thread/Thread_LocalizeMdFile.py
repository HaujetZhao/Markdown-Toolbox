# -*- coding: UTF-8 -*-

import os
import pathlib
import re
import requests
import tempfile
import threading
import time
import urllib.error
from shutil import copy, move, rmtree
from urllib import parse
from urllib.parse import urlparse

from PySide2.QtCore import *

from moduels.component.NormalValue import 常量
from moduels.function.getAllUrlFromString import 从字符串搜索到所有附件路径
from moduels.function.getFileNameFromUrl import 由url返回获得文件名
from moduels.function.getHumanReadableFileSize import 得到便于阅读的文件大小
from moduels.function.processHeaders import 处理Headers


class Document():
    def __init__(self, 文档路径, 相对路径):
        self.文档路径 = 文档路径
        self.相对路径 = 相对路径
        self.文档内容 = self.得到文件内容(self.文档路径)
        self.文档线程锁 = threading.Lock()

        self.全部路径集合 = set(从字符串搜索到所有附件路径(self.文档内容))

        self.绝对路径集合 = self.得到一级绝对路径(self.全部路径集合)
        self.绝对文件夹路径集合 = {路径 for 路径 in self.绝对路径集合 if pathlib.Path(路径).is_dir()}
        self.绝对文件路径集合 = {路径 for 路径 in self.绝对路径集合 if pathlib.Path(路径).is_file()}

        self.相对路径集合 = self.得到一级相对路径(self.全部路径集合 - self.绝对路径集合)
        self.相对文件夹路径集合 = {路径 for 路径 in self.相对路径集合 if (pathlib.Path(self.文档路径).parent / 路径).is_dir()}
        self.相对文件路径集合 = {路径 for 路径 in self.相对路径集合 if (pathlib.Path(self.文档路径).parent / 路径).is_file()}

        self.网络路径集合 = self.全部路径集合 - self.绝对路径集合 - self.相对路径集合
        self.正在工作的线程数 = 0

    def 得到文件内容(self, 输入文件):
        try:
            with open(输入文件, 'r', encoding='utf-8') as f:
                输入文件内容 = f.read()
        except:
            with open(输入文件, 'r', encoding='gbk') as f:
                输入文件内容 = f.read()
        return 输入文件内容

    def 提交(self):
        with open(self.文档路径, 'w', encoding='utf-8') as f:
            f.write(self.文档内容)

    def 得到一级绝对路径(self, 路径集合):
        一级绝对路径集合 = set()
        for 路径 in 路径集合:
            if os.path.exists(路径):
                一级绝对路径集合.add(路径)
        return 一级绝对路径集合

    def 得到一级相对路径(self, 路径集合):
        一级相对路径集合 = set()
        for 路径 in 路径集合:
            if os.path.exists(pathlib.Path(self.文档路径).parent / 路径):
                一级相对路径集合.add(路径)
        return 一级相对路径集合

    # def 迭代所有绝对路径(self, 路径集合):
    #     绝对文件路径集合 = set()
    #     绝对文件夹路径集合 = set()
    #     for 路径 in 路径集合:
    #         if os.path.isfile(路径):
    #             绝对文件路径集合.add(路径)
    #         elif os.path.isdir(路径):
    #             绝对文件夹路径集合.add(路径)
    #             # print('迭代所有绝对路径要递归的：%s' % { str(子路径) for 子路径 in pathlib.Path(路径).iterdir()})
    #             返回 = self.迭代所有绝对路径({ str(子路径) for 子路径 in pathlib.Path(路径).iterdir()})
    #
    #             绝对文件路径集合 |= 返回[0]
    #             绝对文件夹路径集合 |= 返回[1]
    #             # print(f'合并后的结合: {绝对文件夹路径集合}')
    #     return 绝对文件路径集合, 绝对文件夹路径集合
    #
    # def 迭代所有相对路径(self, 路径集合):
    #     相对文件路径集合 = set()
    #     相对文件夹路径集合 = set()
    #     for 路径 in 路径集合:
    #         if os.path.isfile(pathlib.Path(self.文档路径).parent / 路径):
    #             相对文件路径集合.add(路径)
    #         elif os.path.isdir(pathlib.Path(self.文档路径).parent / 路径):
    #             相对文件夹路径集合.add(路径)
    #             返回 = self.迭代所有相对路径({str(子路径.relative_to(os.path.dirname(self.文档路径))) for 子路径 in (pathlib.Path(self.文档路径).parent / 路径).iterdir()})
    #             相对文件路径集合 |= 返回[0]
    #             相对文件夹路径集合 |= 返回[1]
    #     # print(f'相对文件路径集合: {相对文件路径集合} \n相对文件夹路径集合: {相对文件夹路径集合}')
    #     return 相对文件路径集合, 相对文件夹路径集合

    def 跳转链接还原(self):
        for 索引, 链接 in enumerate(self.网络路径集合.copy()):
            if not re.match(r'(http|https|ftp)://.+?(http|https|ftp).+', 链接):
                continue
            原链接的跳转部分 = re.search('((http|https|ftp)(://.+?))((http|https|ftp).+)', 链接).group(4)
            真实链接 = parse.unquote(原链接的跳转部分)
            self.网络路径集合.remove(链接)
            self.网络路径集合.add(真实链接)
            self.文档内容 = self.文档内容.replace(链接, 真实链接)
        self.提交()

    def 带空格路径写法标准化(self):
        while self.正在工作的线程数 > 1:
            time.sleep(0.1)
        self.全部路径集合 = set(从字符串搜索到所有附件路径(self.文档内容))
        for 路径 in self.全部路径集合:
            if ' ' in 路径:
                if f'<{路径}>' not in self.文档内容 and f'"{路径}"' not in self.文档内容 and f"'{路径}'" not in self.文档内容:
                    应替换成的内容 = f'<{路径}>'
                    self.文档线程锁.acquire()
                    self.文档内容 = self.文档内容.replace(str(路径), 应替换成的内容)
                    self.文档线程锁.release()
        self.提交()

class ConflictReply():
    '''
    当发现目标文件已存在，需要使用弹窗提示如何处理
    先构造一个实例，
    将这个实例用信号发出去，
    图形界面通过弹窗得到回馈后，将获得的内容写入这个实例
    '''
    def __init__(self):
        self.已回复 = False
        self.新旧文件相同 = None
        self.处理手段 = None
        self.目标绝对路径Path = None

class Thread_LocalizeMdFile(QThread):
    完成 = Signal()
    状态栏消息 = Signal(str, int)
    提醒是否要覆盖的信号 = Signal(str, str)
    文件冲突信号 = Signal(ConflictReply, pathlib.Path, pathlib.Path)

    def __init__(self, parent=None):
        super(Thread_LocalizeMdFile, self).__init__(parent)
        self.判断文件是否相同的方式 = 0
        self.文件冲突处理方式 = 0

        self.离线网络路径 = True
        self.检查链接超时时长 = 常量.检查链接超时时长

        self.输入文件列表 = None
        self.cookie路径 = None
        self.目标相对路径 = None
        # self.

        self.离线化子线程数 = 常量.离线化子线程数
        self.正在工作子线程数 = 0
        self.可以开启下一个文件处理线程 = True
        self.子线程锁 = threading.Lock()

    def run(self):
        输入文件列表 = self.输入文件列表
        目标相对文件夹路径 = self.目标相对路径.rstrip('/').lstrip('/')

        self.状态栏消息.emit('正在离线化中，到控制台页面可以查看进度', 5000)

        print(f'\n开始执行离线化任务 {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
        self.黑名单域名列表 = set()

        下载线程锁 = threading.Lock()
        for 文件序号, 输入文件 in enumerate(输入文件列表):
            # 提示正在处理第几个文件
            self.状态栏消息.emit(f'总任务数：{len(输入文件列表)}, 正在处理第 {文件序号 + 1} 个，文件路径：“{输入文件}”', 10000)
            print(f'\n\n\n\n\n\n离线化任务数：{len(输入文件列表)}，正在处理第 {文件序号 + 1} 个，文件路径：“{输入文件}”\n')

            # 如果文件不存在，则继续下一个
            if not os.path.exists(输入文件):
                continue

            # 新建一个文档实例
            文档 = Document(输入文件, self.目标相对路径)

            # 如果文档中没有搜索到链接，就继续处理下一个文档
            if len(文档.全部路径集合) == 0: continue

            # 先备份原来的文档
            self.备份文档(文档)

            # 对本地链接进行处理
            while  self.正在工作子线程数 > self.离线化子线程数:
                time.sleep(0.1)
            self.线程数更新(文档, 1)
            threading.Thread(target=self.本地路径相对化线程, args=[文档]).start()

            文档.文档线程锁.acquire()
            文档.提交()
            文档.文档线程锁.release()


            if self.离线网络路径:

                # 将跳转链接还原
                while self.正在工作子线程数 > self.离线化子线程数:
                    time.sleep(0.1)
                文档.跳转链接还原()
            #
                # 下载文件
                for 网络路径 in 文档.网络路径集合:
                    while self.正在工作子线程数 > self.离线化子线程数:
                        time.sleep(0.1)
                    self.线程数更新(文档, 1)
                    threading.Thread(target=self.网络路径相对化线程, args=[文档, 网络路径]).start()

            while  self.正在工作子线程数 > self.离线化子线程数:
                time.sleep(0.1)
            self.线程数更新(文档, 1)
            threading.Thread(target=self.文档带空格路径写法标准化线程, args=[文档]).start()


        while self.正在工作子线程数 > 0:
            print(f'还有 {self.正在工作子线程数} 个线程在工作')
            time.sleep(1)

        文档.文档线程锁.acquire()
        文档.提交()
        文档.文档线程锁.release()

        # 发送完成信息
        print(f'\n\n\n\n离线化任务完成 {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
        self.状态栏消息.emit('离线化任务完成', 5000)
        self.完成.emit()

    def 备份文档(self, 文档):
        文档Path = pathlib.Path(文档.文档路径)
        self.检查文件夹路径(文档Path.parent / '离线化的文档备份')
        with open(文档Path.parent / '离线化的文档备份' / 文档Path.name, 'w', encoding='utf-8') as f:
            f.write(文档.文档内容)

    def 检查文件夹路径(self, 文件夹路径Path):
        '''
        确保一个文件夹路径存在
        '''
        if not 文件夹路径Path.exists():
            try:
                文件夹路径Path.mkdir(parents=True)
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return True

    def 本地路径相对化线程(self, 文档:Document):
        '''
        为了确保线程开始和结束的时候，都能正确更新线程数量
        使用多线程开启这个函数
        由这个函数调用相应功能
        '''
        self.本地路径相对化(文档)
        # try:
        #     self.本地路径相对化(文档)
        # except Exception as e:
        #     print(e)
        self.线程数更新(文档, -1)
    def 本地路径相对化(self, 文档:Document):

        绝对文件路径列表 = list(文档.绝对文件路径集合)
        绝对文件路径列表.sort(key=len, reverse=True)
        for 源 in 绝对文件路径列表:
            print(f'\n\n处理绝对路径: {源}\n\n')
            目标 = str(pathlib.Path(文档.文档路径).parent / 文档.相对路径 / os.path.basename(源))
            self.复制或移动文件到相对路径(文档=文档, 查找的链接=源, 源=源, 目标=目标)

        绝对文件夹路径列表 = list(文档.绝对文件夹路径集合)
        绝对文件夹路径列表.sort(key=len, reverse=True)
        for 源 in 绝对文件夹路径列表:
            print(f'\n\n处理绝对路径: {源}\n\n')
            目标 = str(pathlib.Path(文档.文档路径).parent / 文档.相对路径 / os.path.basename(源))
            self.复制或移动文件夹到相对路径(文档=文档, 查找的链接=源, 源=源, 目标=目标)

        相对文件路径列表 = list(文档.相对文件路径集合)
        相对文件路径列表.sort(key=len, reverse=True)
        for 相对路径 in 相对文件路径列表:
            print(f'\n\n处理相对路径: {相对路径}\n\n')
            源 = str((pathlib.Path(文档.文档路径).parent / 相对路径).resolve())
            目标 = str(pathlib.Path(文档.文档路径).parent / 文档.相对路径 / os.path.basename(相对路径))
            if str(pathlib.Path(文档.文档路径).parent / 文档.相对路径) in str(pathlib.Path(文档.文档路径).parent / 相对路径):
                print(f'跳过处理：\n    无需处理：{相对路径}')
                continue
            self.复制或移动文件到相对路径(文档=文档, 查找的链接=相对路径, 源=源, 目标=目标)

        相对文件夹路径列表 = list(文档.相对文件夹路径集合)
        相对文件夹路径列表.sort(key=len, reverse=True)
        for 相对路径 in 相对文件夹路径列表:
            print(f'\n\n处理相对路径: {相对路径}\n\n')
            源 = str((pathlib.Path(文档.文档路径).parent / 相对路径).resolve())
            目标 = str(pathlib.Path(文档.文档路径).parent / 文档.相对路径 / os.path.basename(相对路径))
            if str(pathlib.Path(文档.文档路径).parent / 文档.相对路径) in str(pathlib.Path(文档.文档路径).parent / 相对路径):
                print(f'跳过处理：\n    无需处理：{相对路径}')
                continue
            self.复制或移动文件夹到相对路径(文档=文档, 查找的链接=相对路径, 源=源, 目标=目标)

    def 网络路径相对化线程(self, 文档:Document, 网络路径:str):
        '''
        为了确保线程开始和结束的时候，都能正确更新线程数量
        使用多线程开启这个函数
        由这个函数调用相应功能
        '''
        self.网络路径相对化(文档, 网络路径)
        # try:
        #     self.网络路径相对化(文档, 网络路径)
        # except Exception as e:
        #     print(e)
        self.线程数更新(文档, -1)
        # print(f'一个网络离线化进程结束，线程数：{self.正在工作子线程数}')

    def 网络路径相对化(self, 文档:Document, 网络路径:str):
        字典 = {}
        query = urllib.parse.urlparse(网络路径).query
        items = [urllib.parse.unquote_plus(item) for item in query.split('&')]
        for item in items:
            splits = item.split('=')
            if len(splits) > 1:
                字典[item.split('=')[0]] = item.split('=')[1]

        # 针对 zhihu 的 latex 解析
        if 'tex' in 字典:
            latex = f'${字典["tex"]}$'
            文档.文档内容 = 文档.文档内容.replace(f'![]({网络路径})', latex)
            print(f'匹配到 latex: {latex}')

        # 如果没有找到链接里的其他可转换的解析信息，那就尝试下载它
        else:
            self.网络路径文件下载(文档, 网络路径)

    def 网络路径文件下载(self, 文档:Document, 网络路径:str):
        '''
        使用 threading.Thread 开启
        将文档中的网络路径转为相对路径
        '''


        # 如果这个网址在黑名单里，就暂时不访问
        if urlparse(网络路径).netloc in self.黑名单域名列表:
            print(f'该网址的域名已认为暂时不可访问：\n    {网络路径}\n')
            return False

        # 初始化cookie
        if os.path.exists(self.cookie路径):
            cookies = self.解析Cookie文件(self.cookie路径)
        else:
            cookies = {}

        # 初始化header
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4272.0 Safari/537.36 Edg/87.0.654.0"}
        HEADERS = 处理Headers(HEADERS, 网络路径)  # 有的网站可能需要在 Header 中加入 referencer

        # 查看链接类型
        try:
            print(f'开始请求网址，查看其类型：\n    {网络路径}\n')
            返回 = requests.request('head', 网络路径, headers=HEADERS, cookies=cookies, timeout=self.检查链接超时时长)
            页面返回类型 = 返回.headers['content-type']
            print(f'得到网页类型：\n    链接：{网络路径}\n    页面类型：    {页面返回类型}\n')
            if 'text/html' in 页面返回类型:
                print(f'链接跳过：\n    链接：{网络路径}\n    原因：链接页面类型是 text/html，他是一个网页\n')
                return False
            if 'status' in 返回.headers:
                页面状态 = 返回.headers['status']
                if '404' in 页面状态:
                    print(f'链接跳过：\n    链接：{网络路径}\n    原因：404 错误，网页未找到\n')
                    return False
        except requests.Timeout as error:
            print(f'链接跳过：\n    链接：{网络路径}\n    原因：访问超时，认为此网址因网络因素暂时不可访问\n')
            self.黑名单域名列表.add(urlparse(网络路径).netloc)
            return False
        except requests.exceptions.ConnectionError:
            print(f'链接跳过：\n    链接：{网络路径}\n    原因：连接错误\n')
            return False
        except requests.exceptions.ConnectTimeout:
            print(f'链接跳过：\n    链接：{网络路径}\n    原因：访问超时，认为此网址因网络因素暂时不可访问\n')
            self.黑名单域名列表.add(urlparse(网络路径).netloc)
            return False
        except Exception as e:
            print(f'链接跳过：\n    链接：{网络路径}\n    原因：用 HEAD 方法获取页面类型失败了，放弃下载\n    详情：{e}\n')
            return False

        try:
            返回 = requests.request('get', 网络路径, headers=HEADERS, cookies=cookies, stream=True, timeout=self.检查链接超时时长)
        except Exception as e:
            print(f'链接跳过：\n    链接：{网络路径}\n    原因：下载失败\n    详情：{e}\n')
            return False

        if 'content-length' in 返回.headers:
            页面返回内容大小 = 得到便于阅读的文件大小(int(返回.headers['content-length']))
        else:
            页面返回内容大小 = '未知'

        输出文件名 = 由url返回获得文件名(网络路径, 返回)

        if 输出文件名 == False:
            print(f'链接跳过：\n    链接：{网络路径}\n    原因：未能获得文件名\n')
            return False

        目标绝对路径Path = pathlib.Path(pathlib.Path(文档.文档路径).parent) / 文档.相对路径 / 输出文件名
        目标相对路径Path = pathlib.Path(文档.相对路径) / 输出文件名
        print(f'链接正常，可下载：\n    链接：{网络路径}\n    文件大小：{页面返回内容大小}\n    目标下载路径：{目标绝对路径Path}\n')

        # 先创建一个临时文件，把网络资源下载下来
        self.检查文件夹路径(目标绝对路径Path.parent)
        临时文件 = tempfile.mkstemp(prefix=目标绝对路径Path.stem + '_', dir=目标绝对路径Path.parent)
        try:
            with os.fdopen(临时文件[0], 'wb') as f:
                f.write(返回.content)
        except Exception as e:
            print(f'下载文件出错：\n    文档：{文档.文档路径}\n    链接：{网络路径}\n    原因：{e}\n')
            return
        #     os.close(临时文件[0])
        # os.close(临时文件[0])

        # 冲突处理
        self.复制或移动文件到相对路径(文档=文档, 查找的链接=网络路径, 源=临时文件[1], 目标=str(目标绝对路径Path), 清理=True)

        # 修改文档内容
        文档.文档线程锁.acquire()
        文档.文档内容 = 文档.文档内容.replace(str(网络路径), str(目标相对路径Path))
        文档.文档线程锁.release()

        # 确认修改文档

    def 文档带空格路径写法标准化线程(self, 文档:Document):
        文档.带空格路径写法标准化()
        self.线程数更新(文档, -1)


    def 复制或移动文件到相对路径(self, 文档:Document, 查找的链接:str, 源:str, 目标:str, 需要替换文档内容=True, 清理=False):
        # print(f'\n\n查找的链接: {查找的链接}\n源：{源}\n目标：{目标}\n\n')
        目标相对路径Path = pathlib.Path(目标).relative_to(os.path.dirname(文档.文档路径))
        源存在 = os.path.exists(源)
        目标存在 = os.path.exists(目标)
        目标是文件 = os.path.isfile(目标)
        源是文件 = os.path.isfile(源)
        移动源到目标 = True
        if 源存在 and 目标存在:
            # 通过弹窗得知新旧文件是否相同
            self.子线程锁.acquire()
            回复 = ConflictReply()
            self.文件冲突信号.emit(回复, pathlib.Path(源), pathlib.Path(目标))
            while not 回复.已回复:
                time.sleep(0.1)
            self.子线程锁.release()

            # 处理弹窗回复内容
            新旧文件相同, 处理手段, 目标Path = 回复.新旧文件相同, 回复.处理手段, 回复.目标绝对路径Path
            目标相对路径Path = 目标Path.relative_to(os.path.dirname(文档.文档路径))

            # 如果文件不同，进行处理
            if not 新旧文件相同:
                if 处理手段 == '保留二者':
                    ...
                elif 处理手段 == '跳过':
                    if 清理:
                        os.remove(源)
                    return False
                elif 处理手段 == '覆盖':
                    if pathlib.Path(目标).is_dir():
                        rmtree(目标)
                    else:
                        os.remove(目标)

            # 如果新旧文件相同，则跳过
            else:
                print(f'''遇到同名相同文件，跳过：
    源文件：{pathlib.Path(源)}
    目标文件：{pathlib.Path(目标)}\n''')
                if 清理:
                    os.remove(源)
                移动源到目标 = False

        if not 源存在:
            移动源到目标 = False

        if 移动源到目标 and os.path.exists(源):
            self.检查文件夹路径(pathlib.Path(目标).parent)
            if pathlib.Path(源).parent == pathlib.Path(文档.文档路径).parent or pathlib.Path(源).parent == pathlib.Path(目标).parent: # 文件和文档同级
                print(f'移动文件：\n      源：{源}\n    目标：{目标}\n')
                move(源, 目标)
            else: # 文件和文档不同级
                print(f'复制文件：\n      源：{源}\n    目标：{目标}\n')
                copy(源, 目标)
        else:
            print(f'跳过处理：\n      源：{源}\n    目标：{目标}\n')
        if 需要替换文档内容:
            文档.文档线程锁.acquire()
            print(f'目标相对路径：{目标相对路径Path}')
            文档.文档内容 = 文档.文档内容.replace(查找的链接, 目标相对路径Path.as_posix())
            文档.文档线程锁.release()
    def 复制或移动文件夹到相对路径(self, 文档:Document, 查找的链接:str, 源:str, 目标:str):
        # print(f'\n\n查找的链接: {查找的链接}\n源：{源}\n目标：{目标}\n\n')
        目标相对路径Path = pathlib.Path(目标).relative_to(os.path.dirname(文档.文档路径))
        源存在 = os.path.exists(源)
        if not 源存在: return
        目标存在 = os.path.exists(目标)
        if 目标存在:
            for 子文件 in pathlib.Path(源).iterdir():
                子文件目标 = (pathlib.Path(目标) / 子文件.relative_to(源)).as_posix()
                self.复制或移动文件到相对路径(文档, '', 子文件, 子文件目标, 需要替换文档内容=False)
        else:
            if pathlib.Path(源).parent == pathlib.Path(文档.文档路径).parent: # 文件和文档同级
                print(f'移动文件：\n      源：{源}\n    目标：{目标}\n')
                move(源, 目标)
            else: # 文件和文档不同级
                print(f'复制文件：\n      源：{源}\n    目标：{目标}\n')
                copy(源, 目标)
        文档.文档线程锁.acquire()
        目标相对路径Path = pathlib.Path(目标).relative_to(pathlib.Path(文档.文档路径).parent)
        print(f'目标相对路径：{目标相对路径Path}')
        文档.文档内容 = 文档.文档内容.replace(查找的链接, 目标相对路径Path.as_posix())
        文档.文档线程锁.release()


    def 线程数更新(self, 文档:Document, 数量:int):
        self.子线程锁.acquire()
        self.正在工作子线程数 += 数量
        self.子线程锁.release()

        文档.文档线程锁.acquire()
        文档.正在工作的线程数 += 数量
        文档.文档线程锁.release()

    def 解析Cookie文件(self, cookiefile):
        """Parse a cookies.txt file and return a dictionary of key value pairs
        compatible with requests."""

        cookies = {}
        with open(cookiefile, 'r') as fp:
            for line in fp:
                if not re.match(r'^[#\r\n ]', line):
                    lineFields = line.strip().split('\t')
                    cookies[lineFields[5]] = lineFields[6]
        return cookies



