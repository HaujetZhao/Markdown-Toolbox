import re
from urllib import parse

def 跳转链接还原(输入文件, 链接列表):
    try:
        输入文件内容 = open(输入文件, 'r', encoding='utf-8').read()
    except:
        输入文件内容 = open(输入文件, 'r', encoding='gbk').read()
    for 索引, 链接 in enumerate(链接列表):
        if not re.match(r'(http|https|ftp)://.+?(http|https|ftp).+', 链接):
            continue
        原链接的跳转部分 = re.search('((http|https|ftp)(://.+?))((http|https|ftp).+)', 链接).group(4)
        真实链接 = parse.unquote(原链接的跳转部分)
        链接列表[索引] = 真实链接
        输入文件内容 = 输入文件内容.replace(链接, 真实链接)
    try:
        open(输入文件, 'w', encoding='utf-8').write(输入文件内容)
    except:
        open(输入文件, 'w', encoding='gbk').write(输入文件内容)
    print('跳转链接还原完毕')
    return True, 链接列表;