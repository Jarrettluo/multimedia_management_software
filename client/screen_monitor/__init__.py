# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: __init__.py
@time: 2020/11/5 10:23
"""
from PyQt5.QtCore import QThread, pyqtSignal
from .client_screen import main

"""
屏幕监控的多线程程序，这里用于启动main函数
"""
class MonitorScreen(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.args_data = args_list

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            try:
                main()
                value = [True]
            except Exception as err:
                value = []
            self.signal.emit(value)  # 发射信号