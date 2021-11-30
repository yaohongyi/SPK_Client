# -*- coding:utf-8 -*-
# 都君丨大魔王
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QSizePolicy
from thread_handle import OriginalInfo, CutPageFileInfo, CutBySize, CutByTime, StitchAudios, AudioResample
from thread_handle import FormatConversion
from public_method import read_ini, list_dir_wav_paths, count_format_num, list_dir_media_paths

audio_filter = read_ini('filter', 'audio_filter')
video_filter = read_ini('filter', 'video_filter')
audio_process_filter = read_ini('filter', 'audio_process')
media_filter = audio_filter + video_filter


class FFmpegClient(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.stitch_file_list = list()
        self.conversion_file_list = list()
        self.setWindowTitle('音视频工具箱_20211117')
        self.setWindowIcon(QtGui.QIcon('./icon/tool.ico'))
        self.setFixedSize(900, 550)
        # 多线程
        self.original_info = None
        self.cut_page_file_info = None
        self.cut_by_size = None
        self.cut_by_time = None
        self.stitch_audios = None
        self.audio_resample = None
        self.format_conversion = None
        # loading等待
        # self.loading_gif = QtGui.QMovie('./icon/loading.gif')
        # self.loading_label = QtWidgets.QLabel(self)
        # self.loading_label.setMovie(self.loading_gif)
        # self.loading_gif.start()
        # 多标签页
        tab_widget = QtWidgets.QTabWidget(self)
        tab_widget.setFixedSize(900, 550)
        file_info_widget = QtWidgets.QWidget()
        tab_widget.addTab(file_info_widget, '查看信息')
        audio_process = QtWidgets.QWidget()
        tab_widget.addTab(audio_process, '音频处理')
        # 音频处理tab页
        cut_upload_label = QtWidgets.QLabel('选择文件：')
        cut_upload_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.cut_upload_line_edit = QtWidgets.QLineEdit()
        self.cut_upload_line_edit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cut_upload_line_edit.setReadOnly(True)
        cut_upload_push_button = QtWidgets.QPushButton('选择')
        cut_upload_push_button.clicked.connect(self.choose_cut_file)
        cut_method_label = QtWidgets.QLabel('切割方式：')
        cut_method_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        # 按大小切割
        self.cut_size_radio_button = QtWidgets.QRadioButton('指定大小')
        self.cut_size_radio_button.setChecked(True)
        self.cut_size_line_edit = QtWidgets.QLineEdit()
        self.cut_size_line_edit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.cut_size_line_edit.setValidator(QtGui.QDoubleValidator())
        self.cut_size_unit_combo_box = QtWidgets.QComboBox()
        self.cut_size_unit_combo_box.addItems(['KB', 'MB', 'GB'])
        self.cut_max_size_label = QtWidgets.QLabel()
        # 按时间段切割
        self.cut_time_radio_button = QtWidgets.QRadioButton('指定时间段')
        self.start_time_date_time_edit = QtWidgets.QDateTimeEdit()
        self.start_time_date_time_edit.setFixedSize(80, 20)
        self.start_time_date_time_edit.setDisplayFormat('HH:mm:ss')
        zhi_label = QtWidgets.QLabel('至')
        self.end_time_date_time_edit = QtWidgets.QDateTimeEdit()
        self.end_time_date_time_edit.setDisplayFormat('HH:mm:ss')
        self.cut_max_duration_label = QtWidgets.QLabel()
        cut_save_label = QtWidgets.QLabel('保存目录：')
        cut_save_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.cut_save_line_edit = QtWidgets.QLineEdit()
        self.cut_save_line_edit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.cut_save_line_edit.setReadOnly(True)
        cut_save_push_button = QtWidgets.QPushButton('选择')
        cut_save_push_button.clicked.connect(self.cut_save_file)
        start_cut_button = QtWidgets.QPushButton('开始切割')
        start_cut_button.clicked.connect(self.start_cut)
        # 音频切割布局
        cut_group_box = QtWidgets.QGroupBox('【音频切割】')
        cut_grid_layout = QtWidgets.QGridLayout(cut_group_box)
        cut_grid_layout.addWidget(cut_upload_label, 0, 0, 1, 1)
        cut_grid_layout.addWidget(self.cut_upload_line_edit, 0, 1, 1, 6)
        cut_grid_layout.addWidget(cut_upload_push_button, 0, 7, 1, 1)
        cut_grid_layout.addWidget(cut_method_label, 1, 0, 1, 1)
        cut_grid_layout.addWidget(self.cut_size_radio_button, 1, 1, 1, 1)
        cut_grid_layout.addWidget(self.cut_size_line_edit, 1, 2, 1, 1)
        cut_grid_layout.addWidget(self.cut_size_unit_combo_box, 1, 3, 1, 1)
        cut_grid_layout.addWidget(self.cut_max_size_label, 1, 4, 1, 3)
        cut_grid_layout.addWidget(self.cut_time_radio_button, 2, 1, 1, 1)
        cut_grid_layout.addWidget(self.start_time_date_time_edit, 2, 2, 1, 1)
        cut_grid_layout.addWidget(zhi_label, 2, 3, 1, 1)
        cut_grid_layout.addWidget(self.end_time_date_time_edit, 2, 4, 1, 1)
        cut_grid_layout.addWidget(self.cut_max_duration_label, 2, 5, 1, 3)
        cut_grid_layout.addWidget(cut_save_label, 3, 0, 1, 1)
        cut_grid_layout.addWidget(self.cut_save_line_edit, 3, 1, 1, 6)
        cut_grid_layout.addWidget(cut_save_push_button, 3, 7, 1, 1)
        # 音频拼接
        stitch_method_label = QtWidgets.QLabel('拼接方式：')
        stitch_choose_file_button = QtWidgets.QPushButton('选择文件')
        stitch_choose_file_button.clicked.connect(self.choose_stitch_files)
        stitch_choose_dir_button = QtWidgets.QPushButton('选择目录')
        stitch_choose_dir_button.clicked.connect(self.choose_stitch_dir)
        stitch_save_dir = QtWidgets.QLabel('保存目录：')
        self.stitch_save_dir_line_edit = QtWidgets.QLineEdit()
        self.stitch_save_dir_line_edit.setReadOnly(True)
        stitch_choose_save_dir_button = QtWidgets.QPushButton('选择')
        stitch_choose_save_dir_button.clicked.connect(self.choose_stitch_save_dir)
        start_stitch_button = QtWidgets.QPushButton('开始拼接')
        start_stitch_button.clicked.connect(self.start_stitch_files)
        # 音频拼接布局
        stitch_group_box = QtWidgets.QGroupBox('【音频拼接】')
        stitch_grid_layout = QtWidgets.QGridLayout(stitch_group_box)
        stitch_grid_layout.addWidget(stitch_method_label, 0, 0, 1, 1)
        stitch_grid_layout.addWidget(stitch_choose_file_button, 0, 1, 1, 1)
        stitch_grid_layout.addWidget(stitch_choose_dir_button, 0, 2, 1, 1)
        stitch_grid_layout.addWidget(stitch_save_dir, 1, 0, 1, 1)
        stitch_grid_layout.addWidget(self.stitch_save_dir_line_edit, 1, 1, 1, 6)
        stitch_grid_layout.addWidget(stitch_choose_save_dir_button, 1, 7, 1, 1)
        # 升降采样控件
        resample_group_box = QtWidgets.QGroupBox('【升降采样】')
        resample_choose_file_label = QtWidgets.QLabel('选择文件：')
        self.resample_file_path_line_edit = QtWidgets.QLineEdit()
        self.resample_file_path_line_edit.setReadOnly(True)
        resample_choose_file_button = QtWidgets.QPushButton('选择')
        resample_choose_file_button.clicked.connect(self.choose_resample_file)
        resample_choose_sample_rate_label = QtWidgets.QLabel('采样率：')
        sample_rete_list = ['48000Hz', '32000Hz', '16000Hz', '11025Hz', '8000Hz']
        self.resample_choose_sample_rete_combo_box = QtWidgets.QComboBox()
        self.resample_choose_sample_rete_combo_box.addItems(sample_rete_list)
        self.resample_choose_sample_rete_combo_box.setCurrentIndex(2)
        resample_choose_save_dir_label = QtWidgets.QLabel('保存目录：')
        self.resample_choose_save_dir_line_edit = QtWidgets.QLineEdit()
        self.resample_choose_save_dir_line_edit.setReadOnly(True)
        resample_choose_save_dir_button = QtWidgets.QPushButton('选择')
        resample_choose_save_dir_button.clicked.connect(self.choose_resample_save_dir)
        start_resample_button = QtWidgets.QPushButton('开始处理')
        start_resample_button.clicked.connect(self.start_resample)
        # 升降采样布局
        resample_grid_layout = QtWidgets.QGridLayout(resample_group_box)
        resample_grid_layout.addWidget(resample_choose_file_label, 0, 0, 1, 1)
        resample_grid_layout.addWidget(self.resample_file_path_line_edit, 0, 1, 1, 6)
        resample_grid_layout.addWidget(resample_choose_file_button, 0, 7, 1, 1)
        resample_grid_layout.addWidget(resample_choose_sample_rate_label, 1, 0, 1, 1)
        resample_grid_layout.addWidget(self.resample_choose_sample_rete_combo_box, 1, 1, 1, 1)
        resample_grid_layout.addWidget(resample_choose_save_dir_label, 2, 0, 1, 1)
        resample_grid_layout.addWidget(self.resample_choose_save_dir_line_edit, 2, 1, 1, 6)
        resample_grid_layout.addWidget(resample_choose_save_dir_button, 2, 7, 1, 1)

        # 格式转换tab页
        conversion_upload_method_label = QtWidgets.QLabel('处理方式：')
        conversion_choose_file_button = QtWidgets.QPushButton('选择文件')
        conversion_choose_file_button.clicked.connect(self.choose_conversion_files)
        conversion_choose_dir_button = QtWidgets.QPushButton('选择目录')
        conversion_choose_dir_button.clicked.connect(self.choose_conversion_dir)
        conversion_target_format_label = QtWidgets.QLabel('目标格式：')
        conversion_format_combo_box = QtWidgets.QComboBox()
        conversion_format_combo_box.addItems(['wav', 'mp3', 'flac', 'ogg', 'wma'])
        conversion_format_combo_box.setDisabled(True)
        conversion_save_dir_label = QtWidgets.QLabel('保存目录：')
        self.conversion_save_line_edit = QtWidgets.QLineEdit()
        self.conversion_save_line_edit.setReadOnly(True)
        choose_save_button = QtWidgets.QPushButton('选择')
        choose_save_button.clicked.connect(self.choose_conversion_save_dir)
        conversion_group_box = QtWidgets.QGroupBox('【格式转换】')
        conversion_grid_layout = QtWidgets.QGridLayout(conversion_group_box)
        conversion_grid_layout.addWidget(conversion_upload_method_label, 0, 0, 1, 1)
        conversion_grid_layout.addWidget(conversion_choose_file_button, 0, 1, 1, 1)
        conversion_grid_layout.addWidget(conversion_choose_dir_button, 0, 2, 1, 1)
        conversion_grid_layout.addWidget(conversion_target_format_label, 1, 0, 1, 1)
        conversion_grid_layout.addWidget(conversion_format_combo_box, 1, 1, 1, 1)
        conversion_grid_layout.addWidget(conversion_save_dir_label, 2, 0, 1, 1)
        conversion_grid_layout.addWidget(self.conversion_save_line_edit, 2, 1, 1, 6)
        conversion_grid_layout.addWidget(choose_save_button, 2, 7, 1, 1)
        start_conversion_button = QtWidgets.QPushButton('开始转换')
        start_conversion_button.clicked.connect(self.start_conversion)

        # 信息打印
        audio_process_log_group_box = QtWidgets.QGroupBox('【信息打印】')
        self.audio_process_log_text_browser = QtWidgets.QTextBrowser()
        audio_process_log_grid_layout = QtWidgets.QGridLayout(audio_process_log_group_box)
        audio_process_log_grid_layout.addWidget(self.audio_process_log_text_browser)
        # 音频处理网格布局
        audio_process_grid_layout = QtWidgets.QGridLayout(audio_process)
        prompt_info_label = QtWidgets.QLabel('<font color=red size=4>友情提示：音频切割、音频拼接、升降采样仅支持wav格式音频！</font>')
        audio_process_grid_layout.addWidget(conversion_group_box, 0, 0, 1, 7)
        audio_process_grid_layout.addWidget(start_conversion_button, 0, 8, 1, 1)
        audio_process_grid_layout.addWidget(prompt_info_label, 1, 0, 1, 7)
        audio_process_grid_layout.addWidget(cut_group_box, 2, 0, 1, 7)
        audio_process_grid_layout.addWidget(start_cut_button, 2, 8, 1, 1)
        audio_process_grid_layout.addWidget(stitch_group_box, 3, 0, 1, 7)
        audio_process_grid_layout.addWidget(start_stitch_button, 3, 8, 1, 1)
        audio_process_grid_layout.addWidget(resample_group_box, 4, 0, 1, 7)
        audio_process_grid_layout.addWidget(start_resample_button, 4, 8, 1, 1)
        audio_process_grid_layout.addWidget(audio_process_log_group_box, 0, 9, 5, 8)

        # 文件信息tab页
        file_info_grid_layout = QtWidgets.QGridLayout(file_info_widget)
        # 选择文件
        choose_file_group_box = QtWidgets.QGroupBox('【选择音视频文件】')
        file_info_grid_layout.addWidget(choose_file_group_box, 0, 0, 1, 1)
        choose_file_grid_layout = QtWidgets.QGridLayout(choose_file_group_box)
        self.file_line_edit = QtWidgets.QLineEdit()
        self.file_line_edit.setPlaceholderText('请选择音频或视频文件')
        self.file_line_edit.setReadOnly(True)
        choose_file_grid_layout.addWidget(self.file_line_edit, 0, 0)
        choose_push_button = QtWidgets.QPushButton('选择')
        choose_file_grid_layout.addWidget(choose_push_button, 0, 1)
        choose_push_button.clicked.connect(self.choose_info_file)
        # 关键信息
        key_info_group_box = QtWidgets.QGroupBox('【关键信息】')
        file_info_grid_layout.addWidget(key_info_group_box, 1, 0, 9, 1)
        key_info_grid_layout = QtWidgets.QGridLayout(key_info_group_box)
        self.key_info_text_browser = QtWidgets.QTextBrowser()
        key_info_grid_layout.addWidget(self.key_info_text_browser)
        # 原始信息
        original_info_group_box = QtWidgets.QGroupBox('【原始信息】')
        file_info_grid_layout.addWidget(original_info_group_box, 0, 2, 10, 1)
        original_info_grid_layout = QtWidgets.QGridLayout(original_info_group_box)
        self.original_info_text_browser = QtWidgets.QTextBrowser()
        original_info_grid_layout.addWidget(self.original_info_text_browser)

    def get_original_info(self):
        """获得音视频文件原始全部信息"""
        self.clear_original_info()
        self.clear_key_info()
        self.original_info = OriginalInfo(self.file_line_edit.text())
        self.original_info.original_msg.connect(self.print_original_info)
        self.original_info.key_msg.connect(self.print_key_info)
        self.original_info.start()

    def choose_info_file(self):
        """文件信息tab页的选取文件"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', filter=media_filter)
        if file_path:
            self.file_line_edit.setText(file_path)
            self.get_original_info()

    def choose_conversion_files(self):
        """选择需要格式转换的多个音频文件"""
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, '选择文件', '/', media_filter)
        if file_paths:
            self.conversion_file_list = file_paths
            self.audio_process_log_text_browser.setText("你选择的音频文件是：")
            for file_path in file_paths:
                self.audio_process_log_text_browser.append(file_path)

    def choose_conversion_dir(self):
        """选择需要进行格式转换的音频文件所在目录"""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '选择音频目录', "/")
        if directory:
            file_paths = list_dir_media_paths(directory)  # 过滤出指定音频格式范围的所有音频文件
            if len(file_paths) > 1:
                self.audio_process_log_text_browser.setText('<font color=red>你选择的音频文件是：</font>')
                self.conversion_file_list = file_paths
                for file_path in file_paths:
                    self.audio_process_log_text_browser.append(file_path)
            else:
                self.audio_process_log_text_browser.setText('<font color=red>所选目录下没有音频文件！！！</font>')

    def choose_conversion_save_dir(self):
        """选择格式转换完成后的音频保存目录"""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '选择保存目录', "/")
        if directory:
            self.conversion_save_line_edit.setText(directory)

    def start_conversion(self):
        """音频转换"""
        if self.conversion_file_list:
            save_dir = self.conversion_save_line_edit.text()
            if save_dir:
                self.audio_process_log_text_browser.clear()
                self.format_conversion = FormatConversion(self.conversion_file_list, save_dir)
                self.format_conversion.start()
            else:
                self.audio_process_log_text_browser.append('<font color=red>请先选择转换后音频保存目录！！！</font>')
        else:
            self.audio_process_log_text_browser.setText('<font color=red>请先选择需要转换的音频文件或音频文件所在目录！！！</font>')

    def choose_cut_file(self):
        """选择音频切割文件"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', filter=audio_process_filter)
        if file_path:
            self.cut_upload_line_edit.setText(file_path)
            self.cut_page_file_info = CutPageFileInfo(file_path)
            self.cut_page_file_info.msg_size.connect(self.set_file_size)
            self.cut_page_file_info.msg_duration.connect(self.set_file_duration)
            self.cut_page_file_info.start()

    def set_file_size(self, size):
        self.cut_max_size_label.setText(f"(最大{size})")

    def set_file_duration(self, duration):
        self.cut_max_duration_label.setText(f"(最长{duration}秒)")

    def cut_save_file(self):
        """音频切割tab页的保存文件"""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '选择保存目录', "./")
        if directory:
            self.cut_save_line_edit.setText(directory)

    def cut_info_check(self):
        """"""
        cut_info = dict()
        cut_file_path = self.cut_upload_line_edit.text()
        if cut_file_path:
            cut_info['cut_file_path'] = cut_file_path
        else:
            self.audio_process_log_text_browser.setText('<font color=red>请先选择要切割的音频文件！！！</font>')
            return None
        if self.cut_size_radio_button.isChecked():
            cut_size = self.cut_size_line_edit.text()
            if cut_size:
                cut_info['cut_size'] = int(cut_size)
                cut_info['cut_size_unit'] = self.cut_size_unit_combo_box.currentText()
            else:
                self.audio_process_log_text_browser.setText('<font color=red>请输入切割大小！！！</font>')
                return None
        elif self.cut_time_radio_button.isChecked():
            original_start_time = self.start_time_date_time_edit.time()
            original_end_time = self.end_time_date_time_edit.time()
            if original_end_time <= original_start_time:
                self.audio_process_log_text_browser.setText('<font color=red>指定时间段切割时，截止时间必须大于开始时间！！！</font>')
                return None
            else:
                cut_info['start_time'] = original_start_time.toString(QtCore.Qt.DefaultLocaleLongDate)
                cut_info['end_time'] = original_end_time.toString(QtCore.Qt.DefaultLocaleLongDate)
        cut_save_dir = self.cut_save_line_edit.text()
        if cut_save_dir:
            cut_info['cut_save_dir'] = cut_save_dir
        else:
            self.audio_process_log_text_browser.setText('<font color=red>请选择切割后文件保存目录！！！</font>')
            return None
        return cut_info

    def start_cut(self):
        """音频切割处理"""
        self.audio_process_log_text_browser.clear()
        cut_info = self.cut_info_check()
        if cut_info:
            cut_file_path = cut_info.get('cut_file_path')
            cut_save_dir = cut_info.get('cut_save_dir')
            if self.cut_size_radio_button.isChecked():
                cut_size = cut_info.get('cut_size')
                cut_size_unit = cut_info.get('cut_size_unit')
                self.cut_by_size = CutBySize(cut_file_path, cut_size, cut_size_unit, cut_save_dir)
                self.cut_by_size.msg.connect(self.print_audio_process_log)
                self.cut_by_size.start()
            elif self.cut_time_radio_button.isChecked():
                start_time = cut_info.get('start_time')
                end_time = cut_info.get('end_time')
                self.cut_by_time = CutByTime(cut_file_path, start_time, end_time, cut_save_dir)
                self.cut_by_time.msg.connect(self.print_audio_process_log)
                self.cut_by_time.start()

    def choose_stitch_files(self):
        """选择需要拼接的音频文件"""
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, '选择音频文件', '/', audio_process_filter)
        if len(file_paths) > 1:
            self.audio_process_log_text_browser.setText('您选择的文件是：')
            self.stitch_file_list = file_paths
            for file_path in file_paths:
                self.audio_process_log_text_browser.append(file_path)
        else:
            self.audio_process_log_text_browser.setText('<font color=red>请选择至少2个音频文件进行拼接！！！</font>')

    def choose_stitch_dir(self):
        """选择需要拼接的音频文件所在目录"""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '选择音频目录', "/")
        if directory:
            file_paths = list_dir_wav_paths(directory)  # 过滤出指定音频格式范围的所有音频文件
            if file_paths:
                format_nums, _ = count_format_num(file_paths)
                self.audio_process_log_text_browser.setText('所选目录下的文件如下：')
                for file_path in file_paths:
                    self.audio_process_log_text_browser.append(file_path)
                if format_nums > 1:
                    self.audio_process_log_text_browser.append('<font color=red>抱歉，当前不支持不同格式的音频文件拼接！！！</font>')
                else:
                    self.stitch_file_list = file_paths
                    self.audio_process_log_text_browser.append('<font color=blue>选择保存目录后，点击【开始拼接】按钮开始拼接吧！！！</font>')
            else:
                self.audio_process_log_text_browser.setText('<font color=red>所选目录下没有符合格式的音频文件！！！</font>')

    def choose_stitch_save_dir(self):
        """选择拼接后的音频保存目录"""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '选择音频目录', "/")
        if directory:
            self.stitch_save_dir_line_edit.setText(directory)

    def start_stitch_files(self):
        """"""
        self.audio_process_log_text_browser.clear()
        if self.stitch_file_list:
            save_dir = self.stitch_save_dir_line_edit.text()
            _, save_format = count_format_num(self.stitch_file_list)
            if save_dir:
                self.stitch_audios = StitchAudios(self.stitch_file_list, save_dir, save_format)
                self.stitch_audios.msg.connect(self.print_audio_process_log)
                self.stitch_audios.start()
            else:
                self.audio_process_log_text_browser.append('<font color=red>请选择拼接音频的保存目录！！！</font>')
        else:
            self.audio_process_log_text_browser.append('<font color=red>请先选择需要拼接的音频文件或其所在目录！！！</font>')

    def print_audio_process_log(self, msg):
        """打印音频切割、音频拼接日志"""
        self.audio_process_log_text_browser.append(msg)

    def clear_cut_stitch_info(self):
        """清空音频切割、音频拼接日志"""
        self.audio_process_log_text_browser.clear()

    def choose_resample_file(self):
        """选择需要重采样的音频文件"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', filter=audio_process_filter)
        if file_path:
            self.resample_file_path_line_edit.setText(file_path)

    def choose_resample_save_dir(self):
        """设置重采样文件保存目录"""
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, '选择保存目录', "/")
        if directory:
            self.resample_choose_save_dir_line_edit.setText(directory)

    def start_resample(self):
        """开始对音频进行重采样"""
        self.audio_process_log_text_browser.clear()
        source_file_path = self.resample_file_path_line_edit.text()
        sample_rate = self.resample_choose_sample_rete_combo_box.currentText()
        finally_sample_rate = sample_rate[:-2]
        save_dir = self.resample_choose_save_dir_line_edit.text()
        if source_file_path:
            self.audio_process_log_text_browser.clear()
            if save_dir:
                self.audio_resample = AudioResample(source_file_path, finally_sample_rate, save_dir)
                self.audio_resample.msg.connect(self.print_audio_process_log)
                self.audio_resample.start()
            else:
                self.audio_process_log_text_browser.append('<font color=red>请选择要重采样音频保存目录！！！</font>')
        else:
            self.audio_process_log_text_browser.append('<font color=red>请先选择要重采样的音频！！！</font>')

    def print_original_info(self, msg):
        """打印原始文件信息"""
        self.original_info_text_browser.append(msg)

    def clear_original_info(self):
        """清除原始信息日志"""
        self.original_info_text_browser.clear()

    def print_key_info(self, msg):
        """打印关键文件信息"""
        self.key_info_text_browser.append(msg)

    def clear_key_info(self):
        """清除关键信息日志"""
        self.key_info_text_browser.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    # splash = QtWidgets.QSplashScreen(QtGui.QPixmap('./loading.gif'))
    # splash.show()
    # app.processEvents()
    client = FFmpegClient()
    client.show()
    # splash.finish(client)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
