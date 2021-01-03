# -*- coding: UTF-8 -*-

import os, hashlib

# 后面可以改成 filecmp 的方法

def 文件大小比较新旧文件是否相同(新文件, 旧文件):
    if os.path.isdir(新文件):
        新文件大小 = 得到文件夹大小(新文件)
    else:
        新文件大小 = 得到文件大小(新文件)
    if os.path.isdir(旧文件):
        旧文件大小 = 得到文件夹大小(旧文件)
    else:
        旧文件大小 = 得到文件大小(旧文件)
    if 新文件大小 == 旧文件大小:
        return True, 新文件大小, 旧文件大小
    else:
        return False, 新文件大小, 旧文件大小

def MD5比较新旧文件是否相同(新文件, 旧文件):

    if os.path.isdir(新文件):
        新文件MD5 = 得到文件夹MD5哈希值(新文件)
    else:
        新文件MD5 = 得到文件MD5哈希值(新文件)
    if os.path.isdir(旧文件):
        旧文件MD5 = 得到文件夹MD5哈希值(旧文件)
    else:
        旧文件MD5 = 得到文件MD5哈希值(旧文件)
    if 新文件MD5 == 旧文件MD5:
        return True, 新文件MD5, 旧文件MD5
    else:
        return False, 新文件MD5, 旧文件MD5





def 得到文件MD5哈希值(文件):
    m = hashlib.md5()
    with open(文件, 'rb') as f:
        while True:
            # 如果不用二进制打开文件，则需要先编码
            # data = f.read(1024).encode('utf-8')
            data = f.read(1024)  # 将文件分块读取
            if not data:
                break
            m.update(data)
    return m.hexdigest()

def 得到文件夹MD5哈希值(文件夹):
    m = hashlib.md5()
    for dirpath, dirnames, filenames in os.walk(文件夹):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                with open(fp, 'rb') as f:
                    while True:
                        # 如果不用二进制打开文件，则需要先编码
                        # data = f.read(1024).encode('utf-8')
                        data = f.read(1024)  # 将文件分块读取
                        if not data:
                            break
                        m.update(data)
    return m.hexdigest()

def 得到文件大小(文件):
    return os.path.getsize(文件)

def 得到文件夹大小(文件夹):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(文件夹):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size
