# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: client_panel
@time: 2020/11/3 19:04
"""
import copy
import datetime
import json
import os
import socket
import struct
import sys
import threading
import time

"""
以下引用是由于使用PyInstaller进行软件打包时出现bug。
参考链接：https://bbs.csdn.net/topics/392428917
"""
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRegExp
from PyQt5.QtGui import QIcon, QCursor, QIntValidator, QRegExpValidator
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMenu, QAction, QTreeWidgetItem, QHeaderView, QDirModel, \
    QTreeView, QFileDialog, QTableWidgetItem, QCompleter
from client.screen_monitor import MonitorScreen

buffsize = 1024
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 9999


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source_client/client_panel.ui", self)  # 加载面板文件，使用qt designer开发
        self.setWindowTitle("学生端控制软件 -樱桃智库")

        self.stu_file = ''  # 学生文件为空
        self.file_name = ''  # 准备上传的文件名

        self.server_host = self.lineEdit.text()  # 用户输入的主机地址
        self.server_port = self.lineEdit_2.text()  # 用户输入的主机端口
        self.pushButton.clicked.connect(self.connect_server)  # 点击链接服务器的操作
        self.toolButton.clicked.connect(self.file_dialog)  # 点击选择文件的操作
        self.pushButton_2.clicked.connect(self.send_file)  # 点击发送文件的操作
        self.pushButton_3.clicked.connect(self.hands_up)  # 学生举手操作

        self.ip_init_lst = ['127.0.0.1', '192.168.1.1', '172.16.1.1']
        self.port_init_lst = ['19869', '8008', '88888']
        self.init_lineedit(self.lineEdit, self.ip_init_lst)  # ip 输入位置自动补全
        self.init_lineedit(self.lineEdit_2, self.port_init_lst)  # port位置自动补全
        ip_regex = QRegExp(
            "\\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b")  # ip的正则表达式
        ip_validator = QRegExpValidator(ip_regex, self.lineEdit)
        self.lineEdit.setValidator(ip_validator)
        self.lineEdit_2.setValidator(QIntValidator())

    def init_lineedit(self, lineedit, item_list):
        """
        用户自动补全功能
        :param lineedit:
        :param item_list:
        :return:
        """
        # 增加自动补全
        self.completer = QCompleter(item_list)
        # 设置匹配模式  有三种： Qt.MatchStartsWith 开头匹配（默认）  Qt.MatchContains 内容匹配  Qt.MatchEndsWith 结尾匹配
        self.completer.setFilterMode(Qt.MatchContains)
        # 设置补全模式  有三种： QCompleter.PopupCompletion（默认）  QCompleter.InlineCompletion   QCompleter.UnfilteredPopupCompletion
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        # 给lineedit设置补全器
        lineedit.setCompleter(self.completer)
        # 设置默认值
        lineedit.setPlaceholderText(item_list[0])

    def connect_server(self):
        """
        学生端点击连接的操作
        :return:
        """
        self.server_host = self.lineEdit.text()  # 用户输入的主机地址
        self.server_port = self.lineEdit_2.text()  # 用户输入的主机端口,必须转换为整型
        if self.server_host and self.server_port:
            current_time = NowTime().now_time()

            # TODO 这里应该设置多线程后台连接，设置超时10次
            self.textBrowser.append("" + current_time + ": 正在连接"
                                    + self.server_host + ":" + self.server_port)
            res = socket_server.connect_ex((self.server_host, int(self.server_port)))
            if res == 0:
                self.check_thread = Client([1])  # 多线程去获取
                self.check_thread.signal.connect(self.tcp_callback)
                self.check_thread.start()  # 启动线程
                self.textBrowser.append("连接成功！")
                # 启动多线程的屏幕监控
                self.screen_thread = MonitorScreen([1])  # 多线程去获取
                self.screen_thread.signal.connect(self.screen_callback)
                self.screen_thread.start()  # 启动线程

                # 给服务器发送给本机名和ip
                send_client_ip(socket_server)
            else:
                self.textBrowser.append("连接失败！")

        else:
            pass

    # 导入文件窗口
    def file_dialog(self):
        filepath, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                         "Text Files ();;All Files (*)")  # 设置文件扩展名过滤,注意用双分号间隔
        if filepath:
            self.stu_file = copy.deepcopy(filepath)
            print(self.stu_file)
            self.file_name = filepath.split('/')[-1]
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
            dic = {'filename': filename,
                   'filesize': os.path.getsize(self.stu_file)}
            str_dic = json.dumps(dic).encode('utf-8')  # 把字典转换成json然后转成byes
            dic_len = struct.pack('i', len(str_dic))  # 把长度byes加上int标识 4个长度
            socket_server.send(str(dic).encode())  # conn.send(str_dic)
            with open(self.stu_file, 'rb')as f:
                content = f.read()
                socket_server.send(content)
        else:
            pass

    # @debug
    def hands_up(self):
        current_time = NowTime().now_time()
        # TODO 这里应该设置多线程后台连接，设置超时10次
        self.textBrowser.append(current_time + ": 举手一次")
        msg = {'hands_up': True}
        socket_server.send(str(msg).encode())

    # 回调函数
    def tcp_callback(self, value):
        msg = eval(value[0])
        broadcast = msg.get('broadcast')
        reboot = msg.get('reboot')
        turn_off = msg.get('turn_off')
        lock_screen = msg.get('lock_screen')
        current_time = NowTime().now_time()
        if broadcast:
            self.textBrowser.append(current_time + "  老师广播:" + str(broadcast))
        elif reboot:
            self.textBrowser.append(current_time + "  老师重启计算机！")
        elif turn_off:
            self.textBrowser.append(current_time + "  老师关闭计算机！")
        elif lock_screen:
            self.textBrowser.append(current_time + "  老师锁定计算机！")

    def screen_callback(self, value):
        """
        屏幕监控的回调函数
        :param value:
        :return:
        """
        print(value)
        # 这里没有回调！


def send_client_ip(socket_server):
    """
    往已经连接的ip发送客户端的ip和主机名
    :param socket_server:
    :return:
    """
    # 获取本机电脑名
    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    myaddr = socket.gethostbyname(myname)
    msg = {'stu_name': myname, 'stu_addr': myaddr}
    socket_server.send(str(msg).encode())


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
