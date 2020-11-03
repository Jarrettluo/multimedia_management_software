# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: panel
@time: 2020/11/3 19:02
"""
import datetime
import os
import sys
import time
"""
以下引用是由于使用PyInstaller进行软件打包时出现bug。
参考链接：https://bbs.csdn.net/topics/392428917
"""
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMenu, QAction, QTreeWidgetItem, QHeaderView, QDirModel, \
    QTreeView, QFileDialog, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source_server/server_panel.ui", self) # 加载面板文件，使用qt designer开发

        self.setWindowTitle("多媒体管理软件 -樱桃智库")


        self.clients_list = ['1' , '3']
        self.comboBox.addItems(self.clients_list)

        self.comboBox.currentIndexChanged.connect(self.choose_client) # 选中一个客户端


        # self.server_host = self.lineEdit.text()  # 用户输入的主机地址
        # self.server_port = self.lineEdit_2.text()  # 用户输入的主机端口
        self.pushButton_5.clicked.connect(self.device_info)  # 点击设备信息以后的操作
        self.pushButton.clicked.connect(self.reboot_device)  # 点击重启设备的操作
        self.pushButton_2.clicked.connect(self.close_device)  # 点击关闭设备的操作
        self.pushButton_3.clicked.connect(self.lock_screen)  # 锁屏操作
        self.pushButton_4.clicked.connect(self.broadcast)  # 广播操作



    def choose_client(self, i):
        current_client = self.comboBox.currentText()
        print(current_client)

    def device_info(self):
        print("设备信息")

    def reboot_device(self):
        print("重启设备")

    def close_device(self):
        print("关闭设备")

    def lock_screen(self):
        print("锁屏")
        current_time = NowTime().now_time()
        # TODO 这里应该设置多线程后台连接，设置超时10次
        self.textBrowser.append("" + current_time + ": 正在连接"
                                + "锁屏")

    def broadcast(self):
        broadcast_content = self.plainTextEdit.toPlainText()
        if broadcast_content:
            current_time = NowTime().now_time()
            # TODO 这里应该设置多线程后台连接，设置超时10次
            self.textBrowser.append("" + current_time + ": 广播一次"
                                    + broadcast_content)
        else:
            pass
            pass






class NowTime():
    """
    定义当前时间
    """

    def __init__(self):
        pass

    def now_time(self):
        curr_time = datetime.datetime.now()
        time_str = datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
        return time_str


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    with open('style_source_server/app_style.qss', encoding='utf-8') as f:
        qss_style = f.read()
    window.setStyleSheet(qss_style)
    window.show()
    sys.exit(app.exec_())