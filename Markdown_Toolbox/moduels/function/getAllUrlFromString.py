import re

def 从字符串搜索到所有附件路径(字符串):
    print('\n开始从字符串中查找所有附件路径\n')
    # 先清空行内代码
    匹配规则 = r'`[^`\r\n]+?`'  
    字符串 = re.sub(匹配规则, '', 字符串)
    # 再清空块代码
    for i in range(10, 4, -1):
        匹配规则 = '^`{%s}.*?\n.*?\n`{%s}' % (i, i)
        字符串 = re.sub(匹配规则, '', 字符串, flags=re.MULTILINE|re.DOTALL)
    
    # 这里通过多个不同规则，提取出含有链接的字符串
    链接列表 = []
    匹配规则 = r'''\[[^\n\[]*?\]\(<.+?>\)'''   # [link](<url>)
    while re.search(匹配规则, 字符串):
        粗匹配 = re.search(匹配规则, 字符串)
        if 粗匹配: 
            字符串 = 字符串.replace(粗匹配.group(), '')
            链接 = re.search(r'''(?<=\]\(<).+?(?=>\))''', 粗匹配.group())
            if 链接:
                print(f'1:   粗匹配：{粗匹配.group()}\n     链接：{链接.group()}\n')
                if 链接.group() not in 链接列表:
                    链接列表.append(链接.group())
    匹配规则 = r'''\[[^\[]*?\]\(<.+?>\s*?".*?"\)'''   # [link](<ur>l2> "text")
    while re.search(匹配规则, 字符串):
        粗匹配 = re.search(匹配规则, 字符串)
        字符串 = 字符串.replace(粗匹配.group(), '')
        链接 = re.sub(r'''>\s*".*?"\s*\)$''', '', 粗匹配.group())
        链接 = re.sub(r'''^\[.*?\]\(<''', '', 链接)
        if 链接.group() not in 链接列表:
            链接列表.append(链接)
        print(f'2:   粗匹配：{粗匹配.group()}\n     链接：{链接}\n')
        # print(字符串)
    匹配规则 = r'''\[[^\[]*?\]\(.*?\s+('.*?'|".*?")\s*\)'''  # [abc](def "123")
    while re.search(匹配规则, 字符串):
        粗匹配 = re.search(匹配规则, 字符串)
        if 粗匹配: 
            字符串 = 字符串.replace(粗匹配.group(), '')
            链接 = re.search(r'(?<=\]\()\s*[^\s]+?(?=\s)', 粗匹配.group())
            链接 = re.sub(r'^\s*', '', 链接.group())
            if 链接:
                print(f'3:   粗匹配：{粗匹配.group()}\n     链接：{链接}\n')
                if 链接.group() not in 链接列表:
                    链接列表.append(链接)
    匹配规则 = r'''\[[^\[]*?\]\((\\\)|.)+?\)'''  # [123](\)123\)45) 123)      # [[icon](icon.ico)](\)123\)45) 123)
    while re.search(匹配规则, 字符串):
        粗匹配 = re.search(匹配规则, 字符串)
        if 粗匹配: 
            字符串 = 字符串.replace(粗匹配.group(), '')
            链接 = re.search(r'(?<=\]\().+(?=\))', 粗匹配.group())
            if 链接:
                print(f'4:   粗匹配：{粗匹配.group()}\n     链接：{链接.group()}\n')
                if 链接.group() not in 链接列表:
                    链接列表.append(链接.group())
    匹配规则 = r'''<.+?src\s*=\s*".+?".+/>'''  # src = "123"
    while re.search(匹配规则, 字符串):
        粗匹配 = re.search(匹配规则, 字符串)
        if 粗匹配: 
            字符串 = 字符串.replace(粗匹配.group(), '')
            链接 = re.sub(r'''<.+?src\s*=\s*"''', '', 粗匹配.group())
            链接 = re.sub(r'''".+?/>''', '', 链接)
            if 链接:
                print(f'5:   粗匹配：{粗匹配.group()}\n     链接：{链接}\n')
                if 链接.group() not in 链接列表:
                    链接列表.append(链接)
    匹配规则 = r"""<.+?src\s*=\s*'.+?'.+/>"""  # src = '123'
    while re.search(匹配规则, 字符串):
        粗匹配 = re.search(匹配规则, 字符串)
        if 粗匹配: 
            字符串 = 字符串.replace(粗匹配.group(), '')
            链接 = re.sub(r"""<.+?src\s*=\s*'""", '', 粗匹配.group())
            链接 = re.sub(r"""'.+?/>""", '', 链接)
            if 链接:
                print(f'6:  粗匹配：{粗匹配.group()}\n     链接：{链接}\n')
                if 链接.group() not in 链接列表:
                    链接列表.append(链接)
    return 链接列表