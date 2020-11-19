import re

def 从字符串搜索到所有附件路径(字符串):
    print('开始从字符串中查找所有附件路径')
    搜索到的粗糙路径列表 = re.findall(r'\]\(.*?\)', 字符串) + re.findall('src=[\'"][^\'"]+["\']', 字符串)
    搜索到的路径列表 = []
    if 搜索到的粗糙路径列表 != []:
        for 索引, 粗附件路径 in enumerate(搜索到的粗糙路径列表):
            附件路径 = re.search(r'(?<=\]\()[^ \)]+?(?=[ \)])', 粗附件路径)
            if 附件路径 == None:
                附件路径 = re.search('(?<=src=[\'"])[^ \'"]+?(?=[\'"])', 粗附件路径)
                if 附件路径 == None: continue
            附件路径 = 附件路径.group()
            print(f'找到一个附件路径：{附件路径}')
            if 附件路径 not in 搜索到的路径列表:
                搜索到的路径列表.append(附件路径)
    搜索到的粗糙路径列表 = re.findall(r'src=".+?"', 字符串)
    if 搜索到的粗糙路径列表 != []:
        for 索引, 附件路径 in enumerate(搜索到的粗糙路径列表):
            附件路径 = re.search(r'(?<=src=").+?(?=")', 附件路径)
            if 附件路径 == None: continue
            附件路径 = 附件路径.group()
            print(f'找到一个附件路径：{附件路径}')
            if 附件路径 not in 搜索到的路径列表:
                搜索到的路径列表.append(附件路径)
    print('返回找到的所有附件路径')
    return 搜索到的路径列表