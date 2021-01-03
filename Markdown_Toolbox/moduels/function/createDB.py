# -*- coding: UTF-8 -*-

from moduels.component.NormalValue import 常量

def 准备数据库():

    数据库连接 = 常量.数据库连接
    偏好设置表单名 = 常量.偏好设置表单名
    cursor = 数据库连接.cursor()
    result = cursor.execute(f'select * from sqlite_master where name = "{偏好设置表单名}";')
    if result.fetchone() == None:
        cursor.execute(f'''create table {偏好设置表单名} (
                                            id integer primary key autoincrement,
                                            item text,
                                            value text
                                            )''')
    else:
        ...

    数据库连接.commit() # 最后要提交更改
