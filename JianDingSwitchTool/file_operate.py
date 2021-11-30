# -*- coding:utf-8 -*-
# 都君丨大魔王
import re
import time
import os
from PyQt5 import QtCore

file_content = "/** -1：教学版, 0: 基础版, 1: 高级版, 2: 高级联网版, 3: 专家版 */\n" \
               "module.exports = {topLevel: 2,debug: 1,devTools: 0};"


class FileOperate(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, client_value):
        super().__init__()
        self.edition = client_value.get('edition')
        self.model = client_value.get('model')
        self.save_path = client_value.get('save_path')

    def remove_conf(self):
        """如果存在鉴定系统自带的版本切换文件，则进行删除"""
        conf_path = f"{self.save_path}/appLevel.conf"
        conf_path_ex = os.path.exists(conf_path)
        if conf_path_ex:
            os.remove(conf_path)

    def create_file(self):
        """生成版本切换文件"""
        # 删除鉴定自带的版本切换文件
        self.remove_conf()
        edition_dict = {'教学版': -1, '基础版': 0, '高级版': 1, '高级联网版': 2, '专家版': 3}
        edition_value = edition_dict.get(self.edition)
        model_list = ['关闭', '打开']
        model_value = model_list[self.model]
        new_content = re.sub(r'topLevel: (.*?),debug: (.*?),',
                             f'topLevel: {edition_value},debug: {self.model},',
                             file_content)
        save_path_ex = os.path.exists(self.save_path)
        if save_path_ex:
            exe_path = f"{self.save_path}/国音智能声纹鉴定专家系统.exe"
            exe_path_ex = os.path.exists(exe_path)
            if exe_path_ex:
                try:
                    with open(f"{self.save_path}\\locConf.js", 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    wait_time = 3
                    while wait_time > 0:
                        info = f"当前版本为【{self.edition}】，开发者模式【{model_value}】，需要重启鉴定系统生效！！！ {wait_time}"
                        self.text.emit(info)
                        time.sleep(1)
                        wait_time = wait_time - 1
                    self.text.emit('')
                except PermissionError:
                    self.text.emit(f'请以管理员身份运行鉴定系统版本切换器！！！')
            else:
                self.text.emit(f'选定目录下未找到鉴定系统运行程序，请重新选择目录！！！')
        else:
            self.text.emit(f'选定目录不存在，请正确选择鉴定系统安装目录！！！')

    def run(self) -> None:
        self.create_file()
