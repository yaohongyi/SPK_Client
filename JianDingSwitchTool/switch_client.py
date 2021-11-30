# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
import os
import base64
from PyQt5 import QtGui, QtCore, QtWidgets
from icon.icon import img
from file_operate import FileOperate
from restart_exe import RestartExe

# 生成LOGO
with open('temp.ico', 'wb') as file:
    file.write(base64.b64decode(img))


class SwitchClient(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(630, 200)
        self.setWindowTitle('鉴定系统版本切换器_20211027（仅限SpeakIn内部使用）')
        self.setWindowIcon(QtGui.QIcon('temp.ico'))
        os.remove('temp.ico')
        # 使用须知
        prompt_info_1 = QtWidgets.QLabel('<font color=red>使用须知：</font>')
        prompt_info_2 = QtWidgets.QLabel('<font color=red>1、加密狗必须有“专家版”授权才可以使用版本切换器</font>')
        prompt_info_3 = QtWidgets.QLabel('<font color=red>2、版本切换器必须以管理员身份运行，右键【属性】—>【兼容性】下勾选“以管理员身份运行此程序”进行设置</font>')
        # 版本
        self.edition_label = QtWidgets.QLabel('请选择版本：')
        self.teaching_edition_radio_button = QtWidgets.QRadioButton('教学版', self)
        self.base_edition_radio_button = QtWidgets.QRadioButton('基础版', self)
        self.premium_edition_radio_button = QtWidgets.QRadioButton('高级版', self)
        self.premium_edition_radio_button.setChecked(True)
        self.premium_network_edition_radio_button = QtWidgets.QRadioButton('高级联网版', self)
        self.expert_edition_radio_button = QtWidgets.QRadioButton('专家版', self)
        self.edition_button_group = QtWidgets.QButtonGroup()
        self.edition_button_group.addButton(self.teaching_edition_radio_button, 0)
        self.edition_button_group.addButton(self.base_edition_radio_button, 1)
        self.edition_button_group.addButton(self.premium_edition_radio_button, 2)
        self.edition_button_group.addButton(self.premium_network_edition_radio_button, 3)
        self.edition_button_group.addButton(self.expert_edition_radio_button, 4)
        # 开发者模式
        self.model_label = QtWidgets.QLabel('开发者模式：')
        self.off_radio_button = QtWidgets.QRadioButton('关闭', self)
        self.on_radio_button = QtWidgets.QRadioButton('打开', self)
        self.on_radio_button.setChecked(True)
        self.model_button_group = QtWidgets.QButtonGroup()
        self.model_button_group.addButton(self.off_radio_button, 0)
        self.model_button_group.addButton(self.on_radio_button, 1)
        # 目录选择
        self.install_dir_label = QtWidgets.QLabel('鉴定安装目录：')
        self.install_dir_qle = QtWidgets.QLineEdit()
        self.install_dir_qle.setReadOnly(True)
        self.install_dir_qle.setText(r'C:\Program Files\voice-identify')
        self.choose_path_button = QtWidgets.QPushButton('选择')
        self.choose_path_button.clicked.connect(self.choose_dir)
        # 提示文字
        self.prompt_label = QtWidgets.QLabel('')
        # 【切换版本】按钮，大小自适应
        self.button_Adaptive = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.switch_button = QtWidgets.QPushButton('切换版本\n(F10)')
        self.switch_button.setShortcut('F10')
        self.switch_button.setSizePolicy(self.button_Adaptive)
        self.switch_button.clicked.connect(self.switch_edition)
        # 【自动重启】按钮，大小自适应
        self.restart_button = QtWidgets.QPushButton('重启鉴定\n(F11)')
        self.restart_button.setShortcut('F11')
        self.restart_button.setSizePolicy(self.button_Adaptive)
        self.restart_button.clicked.connect(self.restart_app)
        # 窗口布局
        grid_layout = QtWidgets.QGridLayout(self)  # 主网格
        grid_layout.addWidget(prompt_info_1, 0, 0, 1, 6)
        grid_layout.addWidget(prompt_info_2, 1, 0, 1, 6)
        grid_layout.addWidget(prompt_info_3, 2, 0, 1, 6)
        left_group_box = QtWidgets.QGroupBox()  # 左侧分组框
        grid_layout.addWidget(left_group_box, 3, 0, 5, 5)
        left_layout = QtWidgets.QGridLayout(left_group_box)
        left_layout.addWidget(self.edition_label, 1, 0, 1, 1)
        self.edition_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        left_layout.addWidget(self.teaching_edition_radio_button, 1, 1, 1, 1)
        left_layout.addWidget(self.base_edition_radio_button, 1, 2, 1, 1)
        left_layout.addWidget(self.premium_edition_radio_button, 1, 3, 1, 1)
        left_layout.addWidget(self.premium_network_edition_radio_button, 1, 4, 1, 1)
        left_layout.addWidget(self.expert_edition_radio_button, 1, 5, 1, 1)
        left_layout.addWidget(self.model_label, 2, 0, 1, 1)
        self.model_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        left_layout.addWidget(self.off_radio_button, 2, 1, 1, 1)
        left_layout.addWidget(self.on_radio_button, 2, 2, 1, 1)
        left_layout.addWidget(self.install_dir_label, 3, 0, 1, 1)
        left_layout.addWidget(self.install_dir_qle, 3, 1, 1, 4)
        left_layout.addWidget(self.choose_path_button, 3, 5, 1, 1)
        left_layout.addWidget(self.prompt_label, 4, 0, 1, 6)
        grid_layout.addWidget(self.switch_button, 3, 5, 1, 1)  # 【切换版本】按钮
        grid_layout.addWidget(self.restart_button, 6, 5, 1, 1)  # 【重启鉴定】按钮

    def choose_dir(self):
        """选择鉴定系统安装目录"""
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, './')
        if dir_path:
            self.install_dir_qle.setText(dir_path)
        else:
            self.install_dir_qle.setText(r'C:\Program Files\voice-identify')

    def get_value(self):
        """获取界面字段值"""
        value = {}
        edition = self.edition_button_group.checkedId()
        if edition == 0:
            edition = "教学版"
        elif edition == 1:
            edition = "基础版"
        elif edition == 2:
            edition = "高级版"
        elif edition == 3:
            edition = "高级联网版"
        elif edition == 4:
            edition = "专家版"
        model = self.model_button_group.checkedId()
        save_path = self.install_dir_qle.text()
        value['edition'] = edition
        value['model'] = model
        value['save_path'] = save_path
        return value

    def print_prompt_info(self, text):
        """"""
        self.prompt_label.setText(text)
        self.prompt_label.setStyleSheet("color:blue")

    def switch_edition(self):
        """切换版本"""
        value = self.get_value()
        self.file_operate = FileOperate(value)
        self.file_operate.text.connect(self.print_prompt_info)
        self.file_operate.start()

    def restart_app(self):
        value = self.get_value()
        self.restart_exe = RestartExe(value)
        self.restart_exe.start()


def main():
    # 设置高分辨率显示器自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    client = SwitchClient()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
