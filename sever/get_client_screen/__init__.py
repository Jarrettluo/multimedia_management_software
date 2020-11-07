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
        value = []
        # 进行任务操作, 遍历所有学生端的屏幕
        for client in self.args_data:
            client_url = "http://" + client['stu_addr'] + ":8008/"
            try:
                res = requests.get(client_url, timeout=1)
            except requests.exceptions.Timeout as err:
                image = None
                print(err)
            else:
                if res.status_code == 200:
                    img = QImage.fromData(res.content)
                    image = QPixmap.fromImage(img)
                else:
                    image = None
            value.append(image)
        self.signal.emit(value)  # 发射信号
