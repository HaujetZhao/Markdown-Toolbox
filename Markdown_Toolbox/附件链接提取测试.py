'''
(?=e)   正前瞻
(?!e)   负前瞻

(?<=e)  正回顾
(?<!e)  负回顾
'''

import re
from pprint import pprint



def 从字符串搜索到所有附件路径(字符串):
    print('开始从字符串中查找所有附件路径\n\n\n')
    # 先清空行内代码
    匹配规则 = r'`[^`\r\n]+?`'  
    字符串 = re.sub(匹配规则, '', 字符串)
    # 再清空块代码
    for i in range(10, 4, -1):
        匹配规则 = '^`{%s}.*?\n.*?\n`{%s}' % (i, i)
        字符串 = re.sub(匹配规则, '', 字符串, flags=re.MULTILINE|re.DOTALL)

    # 这里通过多个不同规则，提取出含有链接的字符串
    链接列表 = []
    匹配规则 = r'''\[.*?\]\(<.+?>\)'''   # [link](<url>)
    初步筛查列表 = re.findall(匹配规则, 字符串)
    字符串 = re.sub(匹配规则, '', 字符串)
    for 粗链接 in 初步筛查列表: 
        匹配规则 = r'''(?<=\]\(<).+?(?=>\))'''
        搜索结果 = re.search(匹配规则, 粗链接)
        if 搜索结果:
            链接列表.append(搜索结果.group())
            print(搜索结果.group())
    匹配规则 = r'''\[.*?\]\(<.+?>\s*?".*?"\)'''   # [link](<ur>l2> "text")
    初步筛查列表 = re.findall(匹配规则, 字符串)
    字符串 = re.sub(匹配规则, '', 字符串)
    for 粗链接 in 初步筛查列表: 
        匹配规则 = r'''(?<=\]\(<).+(?=>\))'''
        粗链接 = re.sub(r'''>\s*".*?"\s*\)$''', '', 粗链接)
        搜索结果 = re.sub(r'''^\[.*?\]\(<''', '', 粗链接)
        链接列表.append(搜索结果)
        print(搜索结果)
    匹配规则 = r'''\[[^\[]*?\]\(.*?\s+".*?"\)'''  # [abc](def "123")
    while re.search(匹配规则, 字符串):
        粗匹配 = re.search(匹配规则, 字符串)
        if 粗匹配: 
            字符串 = 字符串.replace(粗匹配.group(), '')
            链接 = re.search(r'(?<=\]\().+(?=\s)', 粗匹配.group())
            if 链接:
                print(链接.group())
                链接列表.append(链接.group())
    匹配规则 = r'''\[[^\[]*?\]\((\\\)|.)+?\)'''  # [123](\)123\)45) 123)      # [[icon](icon.ico)](\)123\)45) 123)
    while re.search(匹配规则, 字符串):
        粗匹配 = re.search(匹配规则, 字符串)
        if 粗匹配: 
            字符串 = 字符串.replace(粗匹配.group(), '')
            链接 = re.search(r'(?<=\]\().+(?=\))', 粗匹配.group())
            if 链接:
                print(链接.group())
                链接列表.append(链接.group())
    # 匹配规则 = r'''\[[^\[]*?\]\(.+?\)'''  # [[icon](icon.ico)](site)  >  [icon](icon.ico)
    # while re.search(匹配规则, 字符串):
    #     粗匹配 = re.search(匹配规则, 字符串).group()
    #     字符串 = 字符串.replace(粗匹配, '')
    #     链接 = re.search(r'(?<=\]\().+(?=\))', 粗匹配).group()
    #     print(链接)
    #     # print(字符串)
    #     链接列表.append(链接)


    # 这里从含有链接的粗字符串中，掐头去尾，提取出链接，放到另一个列表

    return 链接列表



文本 = open('D:/Users/Haujet/Code/Markdown工具箱/Markdown_Toolbox/附件链接提取测试.md', encoding='utf-8').read()
文本 = r"""
[link](<ur>l>)
[link](<ur>l2> "text")
[abc](def "123")
[abc](def 123)
[123](\)123 123)
[[icon](icon.ico)](12 123)  
"""
print(文本)
从字符串搜索到所有附件路径(文本)
# pprint(从字符串搜索到所有附件路径(文本))

# print(re.search('[(12)]',  '121212 and 121212'))

# def 从字符串搜索到所有附件路径(字符串):
#     print('开始从字符串中查找所有附件路径')
#     搜索到的粗糙路径列表 = re.findall(r'\]\(.*?\)', 字符串) + re.findall('src=[\'"][^\'"]+["\']', 字符串)
#     搜索到的路径列表 = []
#     if 搜索到的粗糙路径列表 != []:
#         for 索引, 粗附件路径 in enumerate(搜索到的粗糙路径列表):
#             附件路径 = re.search(r'(?<=\]\()[^ \)]+?(?=[ \)])', 粗附件路径)
#             if 附件路径 == None:
#                 附件路径 = re.search('(?<=src=[\'"])[^ \'"]+?(?=[\'"])', 粗附件路径)
#                 if 附件路径 == None: continue
#             附件路径 = 附件路径.group()
#             print(f'找到一个附件路径：{附件路径}')
#             if 附件路径 not in 搜索到的路径列表:
#                 搜索到的路径列表.append(附件路径)
#     搜索到的粗糙路径列表 = re.findall(r'src=".+?"', 字符串)
#     if 搜索到的粗糙路径列表 != []:
#         for 索引, 附件路径 in enumerate(搜索到的粗糙路径列表):
#             附件路径 = re.search(r'(?<=src=").+?(?=")', 附件路径)
#             if 附件路径 == None: continue
#             附件路径 = 附件路径.group()
#             print(f'找到一个附件路径：{附件路径}')
#             if 附件路径 not in 搜索到的路径列表:
#                 搜索到的路径列表.append(附件路径)
#     print('返回找到的所有附件路径')
#     return 搜索到的路径列表
