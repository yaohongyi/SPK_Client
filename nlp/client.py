# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
import base64
import os
from icon.icon import img
from nlp.create_content import CreateContent
from file_generation import FileGeneration
from PyQt5 import QtWidgets, QtGui, QtCore
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

# 生成LOGO
with open('temp.ico', 'wb') as file:
    file.write(base64.b64decode(img))


class NlpClient(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(1100, 700)
        self.setWindowTitle('NLP内容生成器_20210429')
        self.setWindowIcon(QtGui.QIcon('temp.ico'))
        client_grid = QtWidgets.QGridLayout(self)
        # 文件属性的控件
        people_num_ql = QtWidgets.QLabel('人员数：')
        self.people_num_qsb = QtWidgets.QSpinBox()
        self.people_num_qsb.setMinimum(1)
        self.people_num_qsb.setMaximum(10000)
        people_relation_ql = QtWidgets.QLabel('人员关系：')
        self.people_relation_qcb = QtWidgets.QComboBox()
        self.people_relation_qcb.addItems(['无', '相对关系', '相互关系', '普通关系'])
        self.people_relation_qcb.currentTextChanged.connect(self.people_relation_change)
        create_way_ql = QtWidgets.QLabel('生成方式：')
        self.create_way_qsb = QtWidgets.QComboBox()
        self.create_way_qsb.addItems(['在线预览', '文档保存'])
        self.create_way_qsb.currentTextChanged.connect(self.create_way_change)
        fixed_documents_ql = QtWidgets.QLabel('固定证件：')
        self.fixed_documents_qcb = QtWidgets.QComboBox()
        self.fixed_documents_qcb.addItems(['不固定', '固定'])
        self.fixed_documents_qcb.setEnabled(False)
        self.fixed_documents_qcb.currentTextChanged.connect(self.fixed_documents_change)
        file_num_ql = QtWidgets.QLabel('文件数：')
        self.file_num_qsb = QtWidgets.QSpinBox()
        self.file_num_qsb.setMinimum(1)
        self.file_num_qsb.setMaximum(1000000)
        self.file_num_qsb.setEnabled(False)
        file_type_ql = QtWidgets.QLabel('文件类型：')
        self.file_type_qcb = QtWidgets.QComboBox()
        self.file_type_qcb.addItems(['txt', 'docx'])
        self.file_type_qcb.setEnabled(False)
        save_path_ql = QtWidgets.QLabel('保存路径：')
        self.save_path_qte = QtWidgets.QLineEdit()
        self.save_path_qte.setEnabled(False)
        self.choose_dir_button = QtWidgets.QPushButton('选择目录')
        self.choose_dir_button.setEnabled(False)
        self.choose_dir_button.clicked.connect(self.choose_dir)
        # 文件属性区域控件的布局
        top_gb = QtWidgets.QGroupBox('【文件属性】')
        client_grid.addWidget(top_gb, 0, 1, 1, 1)
        top_grid = QtWidgets.QGridLayout(top_gb)
        top_grid.addWidget(people_num_ql, 0, 1, 1, 1)
        people_num_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        top_grid.addWidget(self.people_num_qsb, 0, 2, 1, 1)
        top_grid.addWidget(people_relation_ql, 0, 3, 1, 1)
        people_relation_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        top_grid.addWidget(self.people_relation_qcb, 0, 4, 1, 1)
        top_grid.addWidget(create_way_ql, 0, 5, 1, 1)
        create_way_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        top_grid.addWidget(self.create_way_qsb, 0, 6, 1, 1)
        top_grid.addWidget(fixed_documents_ql, 1, 1, 1, 1)
        fixed_documents_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        top_grid.addWidget(self.fixed_documents_qcb, 1, 2, 1, 1)
        top_grid.addWidget(file_num_ql, 1, 3, 1, 1)
        file_num_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        top_grid.addWidget(self.file_num_qsb, 1, 4, 1, 1)
        top_grid.addWidget(file_type_ql, 1, 5, 1, 1)
        file_type_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        top_grid.addWidget(self.file_type_qcb, 1, 6, 1, 1)
        top_grid.addWidget(save_path_ql, 2, 1, 1, 1)
        save_path_ql.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        top_grid.addWidget(self.save_path_qte, 2, 2, 1, 4)
        top_grid.addWidget(self.choose_dir_button, 2, 6, 1, 1)
        # 人员信息区域的控件
        self.people_info_gb = QtWidgets.QGroupBox('【请选择人员基本信息】：')
        self.check_all_people_info_qcb = QtWidgets.QCheckBox('全选')
        self.check_all_people_info_qcb.setTristate()
        self.check_all_people_info_qcb.setCheckState(QtCore.Qt.PartiallyChecked)  # 设置默认半全选
        self.name_qcb = QtWidgets.QCheckBox('中文名')
        self.name_qcb.setChecked(True)
        self.gender_qcb = QtWidgets.QCheckBox('性别')
        self.nickname_qcb = QtWidgets.QCheckBox('绰号')
        self.phone_number_qcb = QtWidgets.QCheckBox('手机号')
        self.phone_number_qcb.setChecked(True)
        self.english_name_qcb = QtWidgets.QCheckBox('英文名')
        self.nation_qcb = QtWidgets.QCheckBox('民族')
        self.education_qcb = QtWidgets.QCheckBox('文化程度')
        self.political_status_qcb = QtWidgets.QCheckBox('政治面貌')
        self.job_qcb = QtWidgets.QCheckBox('职业')
        self.email_qcb = QtWidgets.QCheckBox('邮箱')
        self.native_place_qcb = QtWidgets.QCheckBox('籍贯')
        self.domicile_qcb = QtWidgets.QCheckBox('户籍地')
        self.residence_qcb = QtWidgets.QCheckBox('居住地')
        self.qq_qcb = QtWidgets.QCheckBox('QQ号')
        self.wechat_qcb = QtWidgets.QCheckBox('微信号')
        self.wechat_nickname_qcb = QtWidgets.QCheckBox('微信昵称')
        self.twitter_qcb = QtWidgets.QCheckBox('推特')
        self.bank_card_qcb = QtWidgets.QCheckBox('银行卡')
        # 人员信息区域控件布局
        client_grid.addWidget(self.people_info_gb, 1, 1, 1, 1)
        people_info_grid = QtWidgets.QGridLayout(self.people_info_gb)
        people_info_grid.addWidget(self.check_all_people_info_qcb, 0, 1, 1, 1)
        people_info_grid.addWidget(self.name_qcb, 1, 1, 1, 1)
        people_info_grid.addWidget(self.gender_qcb, 1, 2, 1, 1)
        people_info_grid.addWidget(self.nickname_qcb, 1, 3, 1, 1)
        people_info_grid.addWidget(self.phone_number_qcb, 1, 4, 1, 1)
        people_info_grid.addWidget(self.english_name_qcb, 2, 1, 1, 1)
        people_info_grid.addWidget(self.nation_qcb, 2, 2, 1, 1)
        people_info_grid.addWidget(self.education_qcb, 2, 3, 1, 1)
        people_info_grid.addWidget(self.political_status_qcb, 2, 4, 1, 1)
        people_info_grid.addWidget(self.job_qcb, 3, 1, 1, 1)
        people_info_grid.addWidget(self.email_qcb, 3, 2, 1, 1)
        people_info_grid.addWidget(self.native_place_qcb, 3, 3, 1, 1)
        people_info_grid.addWidget(self.domicile_qcb, 3, 4, 1, 1)
        people_info_grid.addWidget(self.residence_qcb, 4, 1, 1, 1)
        people_info_grid.addWidget(self.qq_qcb, 4, 2, 1, 1)
        people_info_grid.addWidget(self.wechat_qcb, 4, 3, 1, 1)
        people_info_grid.addWidget(self.wechat_nickname_qcb, 4, 4, 1, 1)
        people_info_grid.addWidget(self.twitter_qcb, 5, 1, 1, 1)
        people_info_grid.addWidget(self.bank_card_qcb, 5, 2, 1, 1)
        # 人员信息复选框动作
        self.check_all_people_info_qcb.stateChanged.connect(self.check_all_people_info_change)
        self.name_qcb.stateChanged.connect(self.people_check_box_change)
        self.phone_number_qcb.stateChanged.connect(self.people_check_box_change)
        self.gender_qcb.stateChanged.connect(self.people_check_box_change)
        self.nickname_qcb.stateChanged.connect(self.people_check_box_change)
        self.english_name_qcb.stateChanged.connect(self.people_check_box_change)
        self.nation_qcb.stateChanged.connect(self.people_check_box_change)
        self.education_qcb.stateChanged.connect(self.people_check_box_change)
        self.political_status_qcb.stateChanged.connect(self.people_check_box_change)
        self.job_qcb.stateChanged.connect(self.people_check_box_change)
        self.email_qcb.stateChanged.connect(self.people_check_box_change)
        self.native_place_qcb.stateChanged.connect(self.people_check_box_change)
        self.domicile_qcb.stateChanged.connect(self.people_check_box_change)
        self.residence_qcb.stateChanged.connect(self.people_check_box_change)
        self.qq_qcb.stateChanged.connect(self.people_check_box_change)
        self.wechat_qcb.stateChanged.connect(self.people_check_box_change)
        self.wechat_nickname_qcb.stateChanged.connect(self.people_check_box_change)
        self.twitter_qcb.stateChanged.connect(self.people_check_box_change)
        self.bank_card_qcb.stateChanged.connect(self.people_check_box_change)
        # 证件区域的控件
        document_gb = QtWidgets.QGroupBox('【请选择人员证件信息】：')
        self.check_all_document_qcb = QtWidgets.QCheckBox('全选')
        self.check_all_document_qcb.setTristate()
        self.check_all_document_qcb.setCheckState(QtCore.Qt.PartiallyChecked)  # 设置默认半全选
        self.id_card_qcb = QtWidgets.QCheckBox('大陆身份证')
        self.id_card_qcb.setChecked(True)
        self.hk_mc_pass_qcb = QtWidgets.QCheckBox('港澳通行证')
        self.passport_qcb = QtWidgets.QCheckBox('护照')
        self.hk_id_card_qcb = QtWidgets.QCheckBox('香港身份证')
        self.hk_homecoming_permit_qcb = QtWidgets.QCheckBox('香港回乡证')
        self.mc_id_card_qcb = QtWidgets.QCheckBox('澳门身份证')
        self.mc_homecoming_permit_qcb = QtWidgets.QCheckBox('澳门回乡证')
        self.tw_id_card_qcb = QtWidgets.QCheckBox('台湾身份证')
        self.tw_homecoming_permit_qcb = QtWidgets.QCheckBox('台湾回乡证')
        self.tw_pass_qcb = QtWidgets.QCheckBox('台湾通行证')
        self.foreign_passport_qcb = QtWidgets.QCheckBox('外国人护照')
        # 证件区域的控件布局
        client_grid.addWidget(document_gb, 2, 1, 1, 1)
        center_grid = QtWidgets.QGridLayout(document_gb)
        center_grid.addWidget(self.check_all_document_qcb, 0, 1, 1, 1)
        center_grid.addWidget(self.id_card_qcb, 1, 1, 1, 1)
        center_grid.addWidget(self.hk_mc_pass_qcb, 1, 2, 1, 1)
        center_grid.addWidget(self.tw_pass_qcb, 1, 3, 1, 1)
        center_grid.addWidget(self.passport_qcb, 1, 4, 1, 1)
        center_grid.addWidget(self.hk_id_card_qcb, 2, 1, 1, 1)
        center_grid.addWidget(self.hk_homecoming_permit_qcb, 2, 2, 1, 1)
        center_grid.addWidget(self.mc_id_card_qcb, 3, 1, 1, 1)
        center_grid.addWidget(self.mc_homecoming_permit_qcb, 3, 2, 1, 1)
        center_grid.addWidget(self.tw_id_card_qcb, 4, 1, 1, 1)
        center_grid.addWidget(self.tw_homecoming_permit_qcb, 4, 2, 1, 1)
        center_grid.addWidget(self.foreign_passport_qcb, 5, 1, 1, 1)
        # 证件号复选框动作
        self.check_all_document_qcb.stateChanged.connect(self.check_all_document_change)
        self.id_card_qcb.stateChanged.connect(self.document_check_box_change)
        self.hk_mc_pass_qcb.stateChanged.connect(self.document_check_box_change)
        self.tw_pass_qcb.stateChanged.connect(self.document_check_box_change)
        self.passport_qcb.stateChanged.connect(self.document_check_box_change)
        self.hk_id_card_qcb.stateChanged.connect(self.document_check_box_change)
        self.hk_homecoming_permit_qcb.stateChanged.connect(self.document_check_box_change)
        self.mc_id_card_qcb.stateChanged.connect(self.document_check_box_change)
        self.mc_homecoming_permit_qcb.stateChanged.connect(self.document_check_box_change)
        self.tw_id_card_qcb.stateChanged.connect(self.document_check_box_change)
        self.tw_homecoming_permit_qcb.stateChanged.connect(self.document_check_box_change)
        self.foreign_passport_qcb.stateChanged.connect(self.document_check_box_change)
        # 按钮区域的控件
        bottom_qgb = QtWidgets.QGroupBox()
        create_button = QtWidgets.QPushButton('生成内容(F10)')
        create_button.setShortcut('F10')
        create_button.clicked.connect(self.create_content)
        self.clipboard = QtWidgets.QApplication.clipboard()
        clear_button = QtWidgets.QPushButton('清空内容(Ctrl+L)')
        clear_button.setShortcut('Ctrl+L')
        clear_button.clicked.connect(self.clear_log)
        # 按钮区域控件布局
        client_grid.addWidget(bottom_qgb, 3, 1, 1, 1)
        bottom_grid = QtWidgets.QGridLayout(bottom_qgb)
        bottom_grid.addWidget(create_button, 0, 1, 1, 1)
        bottom_grid.addWidget(clear_button, 0, 2, 1, 1)
        # 提示信息
        prompt_ql = QtWidgets.QLabel('<font color=blue size=4>友情提示：在线预览模式下，生成的内容将会自动复制到粘贴板！</font>')
        client_grid.addWidget(prompt_ql, 4, 1, 1, 2)
        # 内容预览区域控件
        content_gb = QtWidgets.QGroupBox('【内容预览】')
        self.content_preview = QtWidgets.QTextEdit()
        content_grid = QtWidgets.QGridLayout(content_gb)
        # 内容预览区域控件布局
        client_grid.addWidget(content_gb, 0, 2, 10, 1)
        content_grid.addWidget(self.content_preview)

    def people_relation_change(self):
        """人员关系改变时的交互"""
        relation = self.people_relation_qcb.currentText()
        if relation in ('相对关系', '相互关系', '普通关系'):
            self.people_num_qsb.setValue(2)
            self.people_num_qsb.setEnabled(False)
            self.name_qcb.setChecked(True)
            self.name_qcb.setEnabled(False)
        else:
            self.people_num_qsb.setEnabled(True)
            self.name_qcb.setEnabled(True)

    def create_way_change(self):
        """内容生成方式改变时的交互"""
        if self.create_way_qsb.currentText() == '在线预览':
            self.people_num_qsb.setEnabled(True)
            self.fixed_documents_qcb.setEnabled(False)
            self.file_num_qsb.setEnabled(False)
            self.file_type_qcb.setEnabled(False)
            self.save_path_qte.setEnabled(False)
            self.choose_dir_button.setEnabled(False)
        else:
            self.fixed_documents_qcb.setEnabled(True)
            self.file_num_qsb.setEnabled(True)
            self.file_type_qcb.setEnabled(True)
            self.save_path_qte.setEnabled(True)
            self.choose_dir_button.setEnabled(True)

    def fixed_documents_change(self):
        """"""
        if self.fixed_documents_qcb.currentText() == '固定':
            self.people_num_qsb.setValue(1)
            self.people_num_qsb.setEnabled(False)
            self.people_relation_qcb.setCurrentText('无')
            self.people_relation_qcb.setEnabled(False)
        else:
            self.people_num_qsb.setEnabled(True)
            self.people_relation_qcb.setEnabled(True)

    def choose_dir(self):
        """选择文件保存目录"""
        dir_path = QtWidgets.QFileDialog.getExistingDirectory(self, './')
        self.save_path_qte.setText(dir_path)

    def get_all_value(self) -> dict:
        """获取窗口所有字段的值"""
        all_value = dict()
        all_value['people_num'] = int(self.people_num_qsb.text())
        all_value['people_relation'] = self.people_relation_qcb.currentText()
        all_value['fixed_documents'] = self.fixed_documents_qcb.currentText()
        all_value['create_way'] = self.create_way_qsb.currentText()
        all_value['file_num'] = int(self.file_num_qsb.text())
        all_value['file_type'] = self.file_type_qcb.currentText()
        all_value['save_path'] = self.save_path_qte.text()
        all_value['name'] = self.name_qcb.isChecked()
        all_value['gender'] = self.gender_qcb.isChecked()
        all_value['nickname'] = self.nickname_qcb.isChecked()
        all_value['phone_number'] = self.phone_number_qcb.isChecked()
        all_value['english_name'] = self.english_name_qcb.isChecked()
        all_value['nation'] = self.nation_qcb.isChecked()
        all_value['education'] = self.education_qcb.isChecked()
        all_value['political_status'] = self.political_status_qcb.isChecked()
        all_value['job'] = self.job_qcb.isChecked()
        all_value['email'] = self.email_qcb.isChecked()
        all_value['native_place'] = self.native_place_qcb.isChecked()  # 籍贯
        all_value['domicile'] = self.domicile_qcb.isChecked()
        all_value['residence'] = self.residence_qcb.isChecked()
        all_value['qq'] = self.qq_qcb.isChecked()
        all_value['wechat'] = self.wechat_qcb.isChecked()
        all_value['wechat_nickname'] = self.wechat_nickname_qcb.isChecked()
        all_value['twitter'] = self.twitter_qcb.isChecked()
        all_value['bank_card'] = self.bank_card_qcb.isChecked()
        all_value['id_card'] = self.id_card_qcb.isChecked()
        all_value['hk_mc_pass'] = self.hk_mc_pass_qcb.isChecked()
        all_value['tw_pass'] = self.tw_pass_qcb.isChecked()
        all_value['passport'] = self.passport_qcb.isChecked()
        all_value['hk_id_card'] = self.hk_id_card_qcb.isChecked()
        all_value['hk_homecoming_permit'] = self.hk_homecoming_permit_qcb.isChecked()
        all_value['mc_id_card'] = self.mc_id_card_qcb.isChecked()
        all_value['mc_homecoming_permit'] = self.mc_homecoming_permit_qcb.isChecked()
        all_value['tw_id_card'] = self.tw_id_card_qcb.isChecked()
        all_value['tw_homecoming_permit'] = self.tw_homecoming_permit_qcb.isChecked()
        all_value['foreign_passport'] = self.foreign_passport_qcb.isChecked()
        # 查看数据
        # print(all_value)
        return all_value

    def create_content(self):
        """"""
        all_value = self.get_all_value()
        if all_value.get('create_way') == '在线预览':
            self.create_content = CreateContent(all_value)
            self.create_content.text.connect(self.content_copy)
            self.create_content.text.connect(self.content_print)
            self.create_content.start()
        else:
            if self.save_path_qte.text() == '':
                msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, '警告', '请选择文件保存路径！')
                msg_box.setWindowIcon(QtGui.QIcon('temp.ico'))
                msg_box.exec_()
            else:
                self.file_generation = FileGeneration(all_value)
                self.file_generation.text.connect(self.content_print)
                self.file_generation.start()

    def content_print(self, content):
        """"""
        self.content_preview.append(f'<font size=4>{content}</font>')
        self.content_preview.append('')

    def content_copy(self, content):
        """生成的内容复制到剪切板"""
        self.clipboard.setText(content)

    def clear_log(self):
        """清除内容预览窗口"""
        self.content_preview.clear()

    def check_all_people_info_change(self):
        if self.check_all_people_info_qcb.checkState() == QtCore.Qt.Checked:
            self.name_qcb.setChecked(True)
            self.gender_qcb.setChecked(True)
            self.nickname_qcb.setChecked(True)
            self.phone_number_qcb.setChecked(True)
            self.english_name_qcb.setChecked(True)
            self.nation_qcb.setChecked(True)
            self.education_qcb.setChecked(True)
            self.political_status_qcb.setChecked(True)
            self.job_qcb.setChecked(True)
            self.email_qcb.setChecked(True)
            self.domicile_qcb.setChecked(True)
            self.native_place_qcb.setChecked(True)
            self.residence_qcb.setChecked(True)
            self.qq_qcb.setChecked(True)
            self.wechat_qcb.setChecked(True)
            self.wechat_nickname_qcb.setChecked(True)
            self.twitter_qcb.setChecked(True)
            self.bank_card_qcb.setChecked(True)
        elif self.check_all_people_info_qcb.checkState() == QtCore.Qt.Unchecked:
            if self.people_relation_qcb.currentText() in ('相对关系', '相互关系', '普通关系'):
                self.name_qcb.setChecked(True)
            else:
                self.name_qcb.setChecked(False)
            self.phone_number_qcb.setChecked(False)
            self.gender_qcb.setChecked(False)
            self.nickname_qcb.setChecked(False)
            self.english_name_qcb.setChecked(False)
            self.nation_qcb.setChecked(False)
            self.education_qcb.setChecked(False)
            self.political_status_qcb.setChecked(False)
            self.job_qcb.setChecked(False)
            self.email_qcb.setChecked(False)
            self.native_place_qcb.setChecked(False)
            self.domicile_qcb.setChecked(False)
            self.residence_qcb.setChecked(False)
            self.qq_qcb.setChecked(False)
            self.wechat_qcb.setChecked(False)
            self.wechat_nickname_qcb.setChecked(False)
            self.twitter_qcb.setChecked(False)
            self.bank_card_qcb.setChecked(False)

    def get_all_people_info_check_box_state_list(self):
        """获取人员信息所有复选框选中状态"""
        all_check_state_list = list()
        all_check_state_list.append(self.name_qcb.isChecked())
        all_check_state_list.append(self.phone_number_qcb.isChecked())
        all_check_state_list.append(self.gender_qcb.isChecked())
        all_check_state_list.append(self.nickname_qcb.isChecked())
        all_check_state_list.append(self.english_name_qcb.isChecked())
        all_check_state_list.append(self.nation_qcb.isChecked())
        all_check_state_list.append(self.education_qcb.isChecked())
        all_check_state_list.append(self.political_status_qcb.isChecked())
        all_check_state_list.append(self.job_qcb.isChecked())
        all_check_state_list.append(self.email_qcb.isChecked())
        all_check_state_list.append(self.native_place_qcb.isChecked())
        all_check_state_list.append(self.domicile_qcb.isChecked())
        all_check_state_list.append(self.residence_qcb.isChecked())
        all_check_state_list.append(self.qq_qcb.isChecked())
        all_check_state_list.append(self.wechat_qcb.isChecked())
        all_check_state_list.append(self.wechat_nickname_qcb.isChecked())
        all_check_state_list.append(self.twitter_qcb.isChecked())
        all_check_state_list.append(self.bank_card_qcb.isChecked())
        return all_check_state_list

    def people_check_box_change(self):
        """根据复选框是否全部勾选，判定【全选】是否需要勾选"""
        all_check_state_list = self.get_all_people_info_check_box_state_list()
        if all(all_check_state_list):
            self.check_all_people_info_qcb.setCheckState(QtCore.Qt.Checked)
        elif any(all_check_state_list):
            self.check_all_people_info_qcb.setTristate()
            self.check_all_people_info_qcb.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            self.check_all_people_info_qcb.setTristate(False)
            self.check_all_people_info_qcb.setCheckState(QtCore.Qt.Unchecked)

    def check_all_document_change(self):
        """证件号【全选】按钮动作处理"""
        if self.check_all_document_qcb.checkState() == QtCore.Qt.Checked:
            self.id_card_qcb.setChecked(True)
            self.hk_mc_pass_qcb.setChecked(True)
            self.tw_pass_qcb.setChecked(True)
            self.passport_qcb.setChecked(True)
            self.hk_id_card_qcb.setChecked(True)
            self.hk_homecoming_permit_qcb.setChecked(True)
            self.mc_id_card_qcb.setChecked(True)
            self.mc_homecoming_permit_qcb.setChecked(True)
            self.tw_id_card_qcb.setChecked(True)
            self.tw_homecoming_permit_qcb.setChecked(True)
            self.foreign_passport_qcb.setChecked(True)
        elif self.check_all_document_qcb.checkState() == QtCore.Qt.Unchecked:
            self.id_card_qcb.setChecked(False)
            self.hk_mc_pass_qcb.setChecked(False)
            self.tw_pass_qcb.setChecked(False)
            self.passport_qcb.setChecked(False)
            self.hk_id_card_qcb.setChecked(False)
            self.hk_homecoming_permit_qcb.setChecked(False)
            self.mc_id_card_qcb.setChecked(False)
            self.mc_homecoming_permit_qcb.setChecked(False)
            self.tw_id_card_qcb.setChecked(False)
            self.tw_homecoming_permit_qcb.setChecked(False)
            self.foreign_passport_qcb.setChecked(False)

    def get_all_document_check_state_list(self) -> list:
        """获取每一个复选框的选中状态"""
        id_card_check_state = self.id_card_qcb.isChecked()
        hk_mc_pass_check_state = self.hk_mc_pass_qcb.isChecked()
        tw_pass_check_state = self.tw_pass_qcb.isChecked()
        passport_check_state = self.passport_qcb.isChecked()
        hk_id_card_check_state = self.hk_id_card_qcb.isChecked()
        hk_homecoming_permit_check_state = self.hk_homecoming_permit_qcb.isChecked()
        mc_id_card_check_state = self.mc_id_card_qcb.isChecked()
        mc_homecoming_permit_check_state = self.mc_homecoming_permit_qcb.isChecked()
        tw_id_card_check_state = self.tw_id_card_qcb.isChecked()
        tw_homecoming_permit_check_state = self.tw_homecoming_permit_qcb.isChecked()
        foreign_passport_check_state = self.foreign_passport_qcb.isChecked()
        all_check_state_list = [id_card_check_state, hk_mc_pass_check_state, tw_pass_check_state, passport_check_state,
                                hk_id_card_check_state, hk_homecoming_permit_check_state, mc_id_card_check_state,
                                mc_homecoming_permit_check_state, tw_id_card_check_state,
                                tw_homecoming_permit_check_state, foreign_passport_check_state]
        return all_check_state_list

    def document_check_box_change(self):
        """根据复选框是否全部勾选，判定【全选】是否需要勾选"""
        all_check_state_list = self.get_all_document_check_state_list()
        if all(all_check_state_list):
            self.check_all_document_qcb.setCheckState(QtCore.Qt.Checked)
        elif any(all_check_state_list):
            self.check_all_document_qcb.setTristate()
            self.check_all_document_qcb.setCheckState(QtCore.Qt.PartiallyChecked)
        else:
            self.check_all_document_qcb.setTristate(False)
            self.check_all_document_qcb.setCheckState(QtCore.Qt.Unchecked)


def main():
    app = QtWidgets.QApplication(sys.argv)
    client = NlpClient()
    client.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
