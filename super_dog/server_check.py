# -*- coding:utf-8 -*-
# 都君丨大魔王
import socket
from PyQt5 import QtCore


class ServerCheck(QtCore.QThread):
    msg = QtCore.pyqtSignal(str)

    def __init__(self):
        super(ServerCheck, self).__init__()

    def check(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(('localhost', 7777))
            return True
        except ConnectionRefusedError:
            self.msg.emit('<font color=red>请先启动服务！！！</font>')
            return False
        finally:
            s.close()

    def run(self) -> None:
        self.check()


if __name__ == '__main__':
    sc = ServerCheck()
    print(sc.check())
