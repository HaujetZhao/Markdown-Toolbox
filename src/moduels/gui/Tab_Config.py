from PySide2.QtCore import *
from PySide2.QtWidgets import *

from moduels.component.NormalValue import 常量
from moduels.gui.HBox_RBtnContainer import HBox_RBtnContainer
from moduels.gui.VBox_RBtnContainer import VBox_RBtnContainer


class Tab_Config(QWidget):
    状态栏消息 = Signal(str, int)
    def __init__(self, parent=None):
        super(Tab_Config, self).__init__(parent)
        self.initElements()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayouts()  # 然后布局
        self.initValues()  # 再定义各个控件的值

    def initElements(self):
        self.程序设置Box = QGroupBox(self.tr('偏好设置'))
        self.开关_关闭窗口时隐藏到托盘 = QCheckBox(self.tr('点击关闭按钮时隐藏到托盘'))
        self.程序设置Box横向布局 = QHBoxLayout()

        self.判断同名文件是否相同的方法Box = QGroupBox(self.tr('如何判断同名文件是否相同'))
        self.只看大小大小方法单选按钮 = QRadioButton('只比较文件大小')
        self.比较大小和哈希值方法单选按钮 = QRadioButton('比较大小和哈希值')
        self.判断同名文件是否相同的方法Box纵向布局 = HBox_RBtnContainer()

        self.同名文件冲突时的处理Box = QGroupBox(self.tr('新文件冲突时默认处理方式'))
        self.弹窗询问单选按钮 = QRadioButton('弹窗询问')
        self.全部覆盖单选按钮 = QRadioButton('全部覆盖')
        self.全部跳过单选按钮 = QRadioButton('全部跳过')
        self.全部保留二者单选按钮 = QRadioButton('全部保留二者')
        self.同名文件冲突时的处理Box纵向布局 = VBox_RBtnContainer()

        self.页面布局 = QVBoxLayout()

    def initSlots(self):
        self.开关_关闭窗口时隐藏到托盘.toggled.connect(self.设置_关闭时最小化)

        self.只看大小大小方法单选按钮.setProperty('id', 0)
        self.只看大小大小方法单选按钮.toggled.connect(lambda e: self.设置_判断文件是否相同的方式(0) if e else 0)
        self.比较大小和哈希值方法单选按钮.setProperty('id', 1)
        self.比较大小和哈希值方法单选按钮.toggled.connect(lambda e: self.设置_判断文件是否相同的方式(1) if e else 0)

        self.弹窗询问单选按钮.setProperty('id', 0)
        self.弹窗询问单选按钮.toggled.connect(lambda e: self.设置_文件冲突默认处理方式(0) if e else 0)
        self.全部覆盖单选按钮.setProperty('id', 1)
        self.全部覆盖单选按钮.toggled.connect(lambda e: self.设置_文件冲突默认处理方式(1) if e else 0)
        self.全部跳过单选按钮.setProperty('id', 2)
        self.全部跳过单选按钮.toggled.connect(lambda e: self.设置_文件冲突默认处理方式(2) if e else 0)
        self.全部保留二者单选按钮.setProperty('id', 3)
        self.全部保留二者单选按钮.toggled.connect(lambda e: self.设置_文件冲突默认处理方式(3) if e else 0)

    def initLayouts(self):
        self.程序设置Box横向布局.addWidget(self.开关_关闭窗口时隐藏到托盘)
        self.程序设置Box.setLayout(self.程序设置Box横向布局)

        self.判断同名文件是否相同的方法Box纵向布局.addWidget(self.只看大小大小方法单选按钮)
        self.判断同名文件是否相同的方法Box纵向布局.addWidget(self.比较大小和哈希值方法单选按钮)
        self.判断同名文件是否相同的方法Box.setLayout(self.判断同名文件是否相同的方法Box纵向布局)

        self.同名文件冲突时的处理Box纵向布局.addWidget(self.弹窗询问单选按钮)
        self.同名文件冲突时的处理Box纵向布局.addWidget(self.全部覆盖单选按钮)
        self.同名文件冲突时的处理Box纵向布局.addWidget(self.全部跳过单选按钮)
        self.同名文件冲突时的处理Box纵向布局.addWidget(self.全部保留二者单选按钮)
        self.同名文件冲突时的处理Box.setLayout(self.同名文件冲突时的处理Box纵向布局)

        self.页面布局.addWidget(self.程序设置Box)
        self.页面布局.addWidget(self.判断同名文件是否相同的方法Box)
        self.页面布局.addWidget(self.同名文件冲突时的处理Box)
        self.页面布局.addStretch(1)

        self.setLayout(self.页面布局)

    def initValues(self):
        self.检查数据库()



    def 检查数据库(self):
        数据库连接 = 常量.数据库连接
        self.检查数据库_关闭时最小化(数据库连接)
        self.检查数据库_判断文件是否相同的方式(数据库连接)
        self.检查数据库_文件冲突默认处理方式(数据库连接)

    def 检查数据库_关闭时最小化(self, 数据库连接):
        result = 数据库连接.cursor().execute(f'''select value from {常量.偏好设置表单名} where item = :item''',
                                {'item': 'hideToTrayWhenHitCloseButton'}).fetchone()
        if result == None: # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
            初始值 = 'False'
            数据库连接.cursor().execute(f'''insert into {常量.偏好设置表单名} (item, value) values (:item, :value) ''',
                           {'item': 'hideToTrayWhenHitCloseButton',
                            'value':初始值})
            数据库连接.commit()
            self.开关_关闭窗口时隐藏到托盘.setChecked(初始值 == 'True')
        else:
            self.开关_关闭窗口时隐藏到托盘.setChecked(result[0] == 'True')

    def 设置_关闭时最小化(self):
        数据库连接 = 常量.数据库连接
        数据库连接.cursor().execute(f'''update {常量.偏好设置表单名} set value = :value where item = :item''',
                               {'item': 'hideToTrayWhenHitCloseButton',
                                'value': str(self.开关_关闭窗口时隐藏到托盘.isChecked())})
        数据库连接.commit()
        常量.关闭时隐藏到托盘 = self.开关_关闭窗口时隐藏到托盘.isChecked()

    def 检查数据库_判断文件是否相同的方式(self, 数据库连接):
        result = 数据库连接.cursor().execute(f'''select value from {常量.偏好设置表单名} where item = :item''',
                                {'item': '判断文件是否相同的方式'}).fetchone()
        if result == None: # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
            初始值 = '1'
            数据库连接.cursor().execute(f'''insert into {常量.偏好设置表单名} (item, value) values (:item, :value) ''',
                           {'item': '判断文件是否相同的方式',
                            'value':初始值})
            数据库连接.commit()
            self.判断同名文件是否相同的方法Box纵向布局.通过id勾选单选按钮(int(初始值))
        else:
            self.判断同名文件是否相同的方法Box纵向布局.通过id勾选单选按钮(int(result[0]))

    def 设置_判断文件是否相同的方式(self, 值):
        常量.判断文件是否相同的方式 = 值
        conn = 常量.数据库连接
        cursor = conn.cursor()
        cursor.execute(f'''update {常量.偏好设置表单名} set value = :判断文件是否相同的方式
                                                where item = :item ''',
                       {'判断文件是否相同的方式': 值,
                        'item': '判断文件是否相同的方式'})
        conn.commit()

    def 检查数据库_文件冲突默认处理方式(self, 数据库连接):
        result = 数据库连接.cursor().execute(f'''select value from {常量.偏好设置表单名} where item = :item''',
                                {'item': '文件冲突默认处理方式'}).fetchone()
        if result == None: # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
            初始值 = '0'
            数据库连接.cursor().execute(f'''insert into {常量.偏好设置表单名} (item, value) values (:item, :value) ''',
                           {'item': '文件冲突默认处理方式',
                            'value':初始值})
            数据库连接.commit()
            self.同名文件冲突时的处理Box纵向布局.通过id勾选单选按钮(int(初始值))
        else:
            self.同名文件冲突时的处理Box纵向布局.通过id勾选单选按钮(int(result[0]))

    def 设置_文件冲突默认处理方式(self, 值):
        常量.文件冲突处理方式 = 值
        conn = 常量.数据库连接
        cursor = conn.cursor()
        cursor.execute(f'''update {常量.偏好设置表单名} set value = :文件冲突默认处理方式
                                                        where item = :item ''',
                       {'文件冲突默认处理方式': 值,
                        'item': '文件冲突默认处理方式'})
        conn.commit()

