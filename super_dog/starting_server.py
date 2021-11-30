# -*- coding:utf-8 -*-
# 都君丨大魔王
import subprocess
from PyQt5 import QtCore


class StartingServer(QtCore.QThread):
    def __init__(self):
        super(StartingServer, self).__init__()

    @staticmethod
    def start_exe():
        subprocess.Popen('./create_v2c_server/create_v2c.exe')

    def run(self) -> None:
        self.start_exe()


if __name__ == '__main__':
    ss = StartingServer()
    ss.start_exe()
