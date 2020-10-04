from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtSql import *
from PySide2.QtWidgets import *
from moduels.component.NormalValue import 常量


class Tab_Config(QWidget):
    def __init__(self, parent=None):
        super(Tab_Config, self).__init__(parent)
        self.initElement()  # 先初始化各个控件
        self.initSlots()  # 再将各个控件连接到信号槽
        self.initLayout()  # 然后布局
        self.initValue()  # 再定义各个控件的值

    def initElement(self):
        self.hideToSystemTraySwitch = QCheckBox(self.tr('点击关闭按钮时隐藏到托盘'))
        self.preferenceGroupLayout = QHBoxLayout()
        self.preferenceGroup = QGroupBox(self.tr('偏好设置'))
        self.masterLayout = QVBoxLayout()

    def initSlots(self):
        self.hideToSystemTraySwitch.clicked.connect(self.隐藏到状态栏开关被点击)

    def initLayout(self):
        self.preferenceGroupLayout.addWidget(self.hideToSystemTraySwitch)
        self.preferenceGroup.setLayout(self.preferenceGroupLayout)
        self.masterLayout.addWidget(self.preferenceGroup)
        self.masterLayout.addStretch(1)
        self.setLayout(self.masterLayout)

    def initValue(self):
        self.检查数据库()


    def 检查数据库(self):
        cursor = 常量.数据库连接.cursor()
        hideToSystemTrayResult = cursor.execute(f'''select value from {常量.数据库偏好设置表单名} where item = '{'hideToTrayWhenHitCloseButton'}'; ''').fetchone()
        if hideToSystemTrayResult == None: # 如果关闭窗口最小化到状态栏这个选项还没有在数据库创建，那就创建一个
            cursor.execute(f'''insert into {常量.数据库偏好设置表单名} (item, value) values ('hideToTrayWhenHitCloseButton', 'False') ''')
            常量.数据库连接.commit()
        else:
            hideToSystemTrayValue = hideToSystemTrayResult[0]
            if hideToSystemTrayValue == 'True':
                self.hideToSystemTraySwitch.setChecked(True)
            else:
                self.hideToSystemTraySwitch.setChecked(False)

    def 隐藏到状态栏开关被点击(self):
        cursor = 常量.数据库连接.cursor()
        cursor.execute(f'''update {常量.数据库偏好设置表单名} set value='{str(self.hideToSystemTraySwitch.isChecked())}' where item = '{'hideToTrayWhenHitCloseButton'}';''')
        常量.数据库连接.commit()
