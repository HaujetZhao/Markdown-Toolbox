import os

def 检查路径(路径):
    # print(f'要检查的路径：{路径}')
    if not os.path.exists(路径):
        try:
            os.makedirs(路径)
            return True
        except:
            # print('创建文件夹失败，有可能是权限问题')
            return False
    else:
        return True