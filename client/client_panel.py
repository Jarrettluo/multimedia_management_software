# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: client_panel
@time: 2020/11/3 19:04
"""
import datetime
import os
import socket
import sys
import threading
import time

"""
以下引用是由于使用PyInstaller进行软件打包时出现bug。
参考链接：https://bbs.csdn.net/topics/392428917
"""
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMenu, QAction, QTreeWidgetItem, QHeaderView, QDirModel, \
    QTreeView, QFileDialog, QTableWidgetItem

INITIAL_HOST = '20.20.20'
INITIAL_PORT = '444'

buffsize=1024
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 9999
socket_server.connect_ex((host, port))

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source_client/client_panel.ui", self)  # 加载面板文件，使用qt designer开发

        self.setWindowTitle("学生端控制软件 -樱桃智库")

        self.lineEdit.setText(INITIAL_HOST)  # 设置初始化
        self.lineEdit_2.setText(INITIAL_PORT)

        self.stu_file = ''  # 学生文件为空
        self.file_name = ''  # 准备上传的文件名

        self.server_host = self.lineEdit.text()  # 用户输入的主机地址
        self.server_port = self.lineEdit_2.text()  # 用户输入的主机端口
        self.pushButton.clicked.connect(self.connect_server)  # 点击链接服务器的操作
        self.toolButton.clicked.connect(self.file_dialog)  # 点击选择文件的操作
        self.pushButton_2.clicked.connect(self.send_file)  # 点击发送文件的操作
        self.pushButton_3.clicked.connect(self.hands_up)  # 学生举手操作

        # # 创建一个socket对象
        # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #
        # host = "127.0.0.1"
        # port = 9999
        # # 连接服务端
        # rec_code = client.connect_ex((host, port))
        # print(rec_code)

        # connect_ex函数执行成功返回0，失败返回非0
        # if rec_code == 0:
        #     print('hjkhkhk')
            # send_msg = "username: 151s, admin: 115s, command: 15s"
            # client.send(send_msg.encode("utf-8"))
            # time.sleep(0.5)
            # recdata = sockethandle.recv(65535)
            # tran_recdata = recdata.decode('utf-8')
            # print(tran_recdata)

        # 10061 – Connection refused //连接被拒绝

        self.check_thread = Client([1])  # 多线程去获取
        self.check_thread.signal.connect(self.tcp_callback)
        self.check_thread.start()  # 启动线程

    def connect_server(self):
        self.server_host = self.lineEdit.text()  # 用户输入的主机地址
        self.server_port = self.lineEdit_2.text()  # 用户输入的主机端口
        if self.server_host and self.server_port:
            current_time = NowTime().now_time()
            # TODO 这里应该设置多线程后台连接，设置超时10次
            self.textBrowser.append("" + current_time + ": 正在连接"
                                    + self.server_host + ":" + self.server_port)
        else:
            pass

    # 导入文件窗口
    def file_dialog(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                          "Text Files ();;All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔
        if fileName1:
            self.file_name = fileName1.split('/')[-1]
            self.stu_file = fileName1
            self.lineEdit_3.setText(self.file_name)
        else:
            pass

    # 发送文件的按钮函数
    def send_file(self):
        filename = self.file_name
        if self.stu_file and filename:
            current_time = NowTime().now_time()
            # TODO 这里应该设置多线程后台连接，设置超时10次
            self.textBrowser.append(current_time + ": 正在发送" + str(filename))
            # TODO 发送成功的回调函数应该在反馈并清空
        else:
            pass

    def hands_up(self):
        current_time = NowTime().now_time()
        # TODO 这里应该设置多线程后台连接，设置超时10次
        self.textBrowser.append(current_time + ": 举手一次")

        msg = "这是举手信息"
        socket_server.send(msg.encode())

    # 回调函数
    def tcp_callback(self, value):
        msg = eval(value[0])
        broadcast = msg.get('broadcast')
        reboot = msg.get('reboot')
        turn_off = msg.get('turn_off')
        current_time = NowTime().now_time()
        if broadcast:
            self.textBrowser.append(current_time + "  老师广播:" + str(broadcast))
        elif reboot:
            self.textBrowser.append(current_time + "  老师重启计算机！")
        elif turn_off:
            self.textBrowser.append(current_time + "  老师关闭计算机！")



class Client(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.args_data = args_list

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            recvdata = socket_server.recv(buffsize).decode('utf-8')
            value = [recvdata]
            self.signal.emit(value)  # 发射信号



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
    with open('style_source_client/app_style.qss', encoding='utf-8') as f:
        qss_style = f.read()
    window.setStyleSheet(qss_style)
    window.show()
    sys.exit(app.exec_())


