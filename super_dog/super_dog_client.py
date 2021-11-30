# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
import datetime
import subprocess
from configparser import ConfigParser
from dateutil.relativedelta import relativedelta
from PyQt5 import QtWidgets, QtGui, QtCore
from create_v2c import CreateV2C
from starting_server import StartingServer
from read_setting import system_info_list, system_info_json


subprocess.Popen('./create_v2c_server/create_v2c.exe')
config_parser = ConfigParser()
ini_path = r'./config/config.ini'
config_parser.read(ini_path, encoding='utf-8')
level_1_dir = config_parser.get('一级目录', 'level_1_dir')


class AuthorizationClient(QtWidgets.QWidget):
    def __init__(self):
        super(AuthorizationClient, self).__init__()
        self.setFixedSize(900, 600)
        self.setWindowTitle('硬件加密狗授权工具_20211108')
        self.setWindowIcon(QtGui.QIcon('./icon/auth.ico'))
        client_grid = QtWidgets.QGridLayout(self)
        # 选择授权系统相关元素
        select_system_gb = QtWidgets.QGroupBox('【请选择要授权的系统】：')
        # 选择授权系统框元素布局
        client_grid.addWidget(select_system_gb, 0, 0, 9, 4)
        select_system_grid = QtWidgets.QGridLayout(select_system_gb)
        # 动态增加可授权系统
        abscissa = 0
        for x in system_info_list:
            system_name, _ = x
            self.system_qcb = QtWidgets.QCheckBox(system_name)
            self.system_qcb.stateChanged.connect(self.get_features)
            select_system_grid.addWidget(self.system_qcb, abscissa, 0, 1, 1)
            abscissa += 1
        # 使用须知
        usage_notice_qgb = QtWidgets.QGroupBox('【使用须知】')
        msg = '<font color=black size=4>本工具可实现硬加密狗批量授权，使用时需要注意以下事项：<br>' \
              '1、每个加密狗的"硬件信息.txt"和"license.c2v"单独存放一个文件夹，文件夹命名规则为<br>“单位名称+加密狗编号”。' \
              '例如：广东省厅正888号。<br>' \
              '2、所有加密狗文件夹存放到同一个"一级目录"下。<br>' \
              '3、一定一定一定要告诉客户，使用软硬锁升级助手【导入升级文件】时，"license.v2c"文件<br>只能存放在纯英文路径下，否则会出现“该加密狗与此电脑硬件信息不匹配”的问题。<br>' \
              '4、一定不要授权所有系统的权限，加密狗硬件不支持，建议最多授权6-7个系统。</font>'
        usage_notice_show = QtWidgets.QLabel(msg)

        # 其他元素
        select_level_1_dir_ql = QtWidgets.QLabel('* 请选择一级目录：')
        self.level_1_dir_path_qle = QtWidgets.QLineEdit()
        self.level_1_dir_path_qle.setText(level_1_dir)
        self.select_level_1_dir_button = QtWidgets.QPushButton('选择目录')
        self.select_level_1_dir_button.clicked.connect(self.select_level_1_dir)
        expire_date_ql = QtWidgets.QLabel('设置硬狗过期日期：')
        self.expire_data_qde = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        one_month_button = QtWidgets.QPushButton('一个月')
        one_month_button.clicked.connect(self.set_one_month_expire)
        three_month_button = QtWidgets.QPushButton('三个月')
        three_month_button.clicked.connect(self.set_three_month_expire)
        half_year_button = QtWidgets.QPushButton('半年')
        half_year_button.clicked.connect(self.set_half_year_expire)
        one_year_button = QtWidgets.QPushButton('一年')
        one_year_button.clicked.connect(self.set_one_year_expire)
        perpetual_button = QtWidgets.QPushButton('永久')
        perpetual_button.clicked.connect(self.set_perpetual_expire)
        execute_button = QtWidgets.QPushButton('开始授权(F10)')
        execute_button.setShortcut('F10')
        execute_button.setFixedSize(160, 80)
        execute_button.clicked.connect(self.execute_action)
        reset_button = QtWidgets.QPushButton('重置(F11)')
        reset_button.setFixedSize(160, 80)
        reset_button.setShortcut("F11")
        reset_button.clicked.connect(self.reset_ui)
        start_service_button = QtWidgets.QPushButton('启动服务(F12)')
        start_service_button.setFixedSize(160, 80)
        start_service_button.setShortcut('F12')
        start_service_button.clicked.connect(self.start_service)
        self.msg_qlb = QtWidgets.QLabel()  # 打印信息

        # 使用须知布局
        client_grid.addWidget(usage_notice_qgb, 0, 4, 2, 8)
        usage_notice_grid = QtWidgets.QGridLayout(usage_notice_qgb)
        usage_notice_grid.addWidget(usage_notice_show, 0, 0, 2, 1)

        # 其他元素布局
        client_grid.addWidget(select_level_1_dir_ql, 2, 4, 1, 1)
        select_level_1_dir_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        client_grid.addWidget(self.level_1_dir_path_qle, 2, 5, 1, 4)
        client_grid.addWidget(self.select_level_1_dir_button, 2, 9, 1, 1)
        client_grid.addWidget(expire_date_ql, 3, 4, 1, 1)
        expire_date_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        client_grid.addWidget(self.expire_data_qde, 3, 5, 1, 1)
        client_grid.addWidget(one_month_button, 3, 6, 1, 1)
        client_grid.addWidget(three_month_button, 3, 7, 1, 1)
        client_grid.addWidget(half_year_button, 3, 8, 1, 1)
        client_grid.addWidget(one_year_button, 3, 9, 1, 1)
        client_grid.addWidget(perpetual_button, 3, 10, 1, 1)
        client_grid.addWidget(execute_button, 4, 4, 1, 2)
        client_grid.addWidget(reset_button, 4, 6, 1, 2)
        client_grid.addWidget(start_service_button, 4, 9, 1, 2)
        client_grid.addWidget(self.msg_qlb, 8, 4, 1, 12)

    feature_list = list()

    def get_features(self):
        sender = self.sender()
        check_state = sender.isChecked()
        check_box_name = sender.text()
        system_feature = system_info_json.get(check_box_name)
        if check_state:
            self.feature_list.extend(system_feature)
        else:
            for x in system_feature:
                self.feature_list.remove(x)
        feature_set = set(self.feature_list)  # 特征去重
        feature_list = list(feature_set)
        feature_list.sort(reverse=False)

    def get_all_value(self):
        all_value = dict()
        # 获取特征值
        if self.feature_list:
            all_value['feature_list'] = self.feature_list
        else:
            all_value['feature_list'] = []
            self.print_msg('请至少选择一个需要授权的系统！！！')
        # 获取一级目录
        if self.level_1_dir_path_qle.text():
            all_value['level_1_dir'] = self.level_1_dir_path_qle.text()
        else:
            all_value['level_1_dir'] = ''
            self.print_msg('请先选择一级目录！！！')
        # 获取过期时间
        all_value['expire_date'] = self.expire_data_qde.date().toString('yyyy-MM-dd')
        return all_value

    def reset_ui(self):
        """重置界面，取消复选框勾选，过期日期设置为今天"""
        self.expire_data_qde.setDate(QtCore.QDate.currentDate())
        for simple_check_box in self.findChildren(QtWidgets.QCheckBox):
            simple_check_box.setChecked(False)

    def select_level_1_dir(self):
        """选择一级目录"""
        level_1_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, './')
        if level_1_dir_path:
            self.level_1_dir_path_qle.setText(level_1_dir_path)
            config_parser.set('一级目录', 'level_1_dir', level_1_dir_path)
            config_parser.write(open(ini_path, 'r+', encoding='utf-8'))
        else:
            self.level_1_dir_path_qle.setText(r'D:\加密狗授权')

    def set_one_month_expire(self):
        """设置过期时间为一个月"""
        expire_data = datetime.date.today() + relativedelta(months=+1)
        self.expire_data_qde.setDate(expire_data)

    def set_three_month_expire(self):
        """设置过期时间为三个月"""
        expire_data = datetime.date.today() + relativedelta(months=+3)
        self.expire_data_qde.setDate(expire_data)

    def set_half_year_expire(self):
        """设置过期时间为半年"""
        expire_data = datetime.date.today() + relativedelta(months=+6)
        self.expire_data_qde.setDate(expire_data)

    def set_one_year_expire(self):
        """设置过期时间为一年"""
        expire_data = datetime.date.today() + relativedelta(months=+12)
        self.expire_data_qde.setDate(expire_data)

    def set_perpetual_expire(self):
        """设置过期时间为永久（2099年）"""
        expire_data = datetime.date(year=2099, month=12, day=31)
        self.expire_data_qde.setDate(expire_data)

    def execute_action(self, t):
        """开始生成v2c文件"""
        self.print_msg('')
        client_info = self.get_all_value()
        values = client_info.values()
        values_bool = all(values)
        if values_bool:
            self.create_v2c = CreateV2C(client_info)
            self.create_v2c.msg.connect(self.print_msg)
            self.create_v2c.start()

    def print_msg(self, msg):
        self.msg_qlb.setText(f"<font color=blue size=4>{msg}</font>")

    def start_service(self):
        self.start = StartingServer()
        self.start.start()

    def reset(self):
        """界面重置"""
        ...


def main():
    # 设置高分辨率显示器自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    client = AuthorizationClient()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
