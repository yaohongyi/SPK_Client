# -*- coding:utf-8 -*-
# 都君丨大魔王
import win32api
import pywintypes
import os
from PyQt5 import QtCore


class RestartExe(QtCore.QThread):
    def __init__(self, client_value):
        super(RestartExe, self).__init__()
        self.install_path = client_value.get('save_path')

    def get_exe_name(self):
        """"""
        try:
            file_list = os.listdir(self.install_path)
            for file_name in file_list:
                if file_name.startswith('国音智能声纹鉴定专家系统') and file_name.endswith('.exe'):
                    exe_name = file_name
                    return exe_name
        except FileNotFoundError:
            return None

    def restart(self):
        exe_name = self.get_exe_name()
        try:
            # 杀死进程
            os.system(f"taskkill /F /IM {exe_name}")
            # 重启应用
            win32api.ShellExecute(0, 'open', f'{self.install_path}\\{exe_name}', '', '', 1)
        except pywintypes.error:
            ...

    def run(self) -> None:
        self.restart()


if __name__ == '__main__':
    value = {'save_path': r'd:\Program Files\voice-identify'}
    restart_app = RestartExe(value)
    result = restart_app.get_exe_name()
    restart_app.restart()
