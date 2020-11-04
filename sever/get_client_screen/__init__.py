# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: __init__.py
@time: 2020/11/4 15:07
"""
import requests  # 导入requests包
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap


class AutoPollScreen(QThread):
    """
    自动轮询客户端的屏幕多线程
    """
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.args_data = args_list

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        url = "http://192.168.124.6:8008/"
        try:
            res = requests.get(url, timeout=1)
        except requests.exceptions.Timeout as err:
            value = []
            print(err)
        else:
            if res.status_code == 200:
                img = QImage.fromData(res.content)
                image = QPixmap.fromImage(img)
                image = image.scaled(300, 200)
                value = [image]
            else:
                value = []
        self.signal.emit(value)  # 发射信号
