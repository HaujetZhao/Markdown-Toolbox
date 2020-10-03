import re

def 从字符串搜索到所有附件路径(字符串):
    搜索到的粗糙路径列表 = re.findall(r'\]\(.*?\)', 字符串)
    搜索到的路径列表 = []
    if 搜索到的粗糙路径列表 != []:
        for 索引, 附件路径 in enumerate(搜索到的粗糙路径列表):
            附件路径 = re.search(r'(?<=\]\()[^ \)]+?(?=[ \)])', 附件路径)
            if 附件路径 == None: continue
            附件路径 = 附件路径.group()
            print(f'附件路径：{附件路径}')
            搜索到的路径列表.append(附件路径)
    return 搜索到的路径列表