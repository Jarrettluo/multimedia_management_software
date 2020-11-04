# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: panel
@time: 2020/11/3 19:02
"""
import datetime
import os
import socket
import sys
import threading
import time

from sever.get_client_screen import AutoPollScreen
from sever.system_time import NowTime

"""
以下引用是由于使用PyInstaller进行软件打包时出现bug。
参考链接：https://bbs.csdn.net/topics/392428917
"""
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QCursor, QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMenu, QAction, QTreeWidgetItem, QHeaderView, QDirModel, \
    QTreeView, QFileDialog, QTableWidgetItem, QGraphicsPixmapItem, QGraphicsScene

buffsize = 1024
socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 9999
# 绑定地址
socket_server.bind((host, port))
socket_server.listen(5)  # 最大连接数
conn_list = []
conn_dt = {}


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("ui_source_server/server_panel.ui", self)  # 加载面板文件，使用qt designer开发
        self.setWindowTitle("多媒体管理软件 -樱桃智库")  # 设置窗口标题

        self.clients_list = []
        self.comboBox.addItems(self.clients_list)
        self.window_initial()  # 窗口初始化
        self.setup_ui()

        self.check_thread = Server([])  # 多线程去获取
        self.check_thread.signal.connect(self.server_callback)
        self.check_thread.start()  # 启动线程

    def window_initial(self):
        if self.clients_list:
            self.current_client = self.clients_list[0]  # 当前客户端是第一个客户端
        else:
            # 如果没有客户端，那么这些按钮不可用
            self.pushButton_5.setEnabled(False)
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
        self.comboBox.currentIndexChanged.connect(self.choose_client)  # 选中一个客户端
        self.pushButton_5.clicked.connect(self.device_info)  # 点击设备信息以后的操作
        self.pushButton.clicked.connect(self.reboot_device)  # 点击重启设备的操作
        self.pushButton_2.clicked.connect(self.close_device)  # 点击关闭设备的操作
        self.pushButton_3.clicked.connect(self.lock_screen)  # 锁屏操作
        self.pushButton_4.clicked.connect(self.broadcast)  # 广播操作
        img_path = "ui_source_server/no_data.png"  # 图片路径
        image = QPixmap(img_path).scaled(300, 180)  # 加载图片,并自定义图片展示尺寸
        self.label_9.setPixmap(image)  # 显示图片
        self.label_10.setPixmap(image)
        self.label_11.setPixmap(image)
        self.label_12.setPixmap(image)
        self.label_13.setPixmap(image)
        self.label_14.setPixmap(image)
        self.label_15.setPixmap(image)
        self.label_16.setPixmap(image)
        self.label_17.setPixmap(image)

    def setup_ui(self):
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.get_client_screen)  # 每次计时到时间时发出信号
        self.timer.start(1000)  # 设置计时间隔并启动；单位毫秒

    def choose_client(self, i):
        self.current_client = self.comboBox.currentText()
        now_client = str(self.current_client)
        current_time = NowTime().now_time()
        self.textBrowser.append("" + current_time + "\n选中" + now_client)
        self.pushButton_5.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)

    def device_info(self):
        """查看设备信息"""
        send_msg = {'device_info': True}
        self.control_client(send_msg)
        current_time = NowTime().now_time()
        self.textBrowser.append("" + current_time + "\n" + "查看设备信息")

    def reboot_device(self):
        """
        教师端重启客户端
        :return:
        """
        send_msg = {'reboot': True}
        self.control_client(send_msg)
        current_time = NowTime().now_time()
        self.textBrowser.append("" + current_time + "\n" + "重启设备")

    def close_device(self):
        """
        教师端关闭学生端计算机
        :return:
        """
        send_msg = {'turn_off': True}
        self.control_client(send_msg)
        current_time = NowTime().now_time()
        self.textBrowser.append("" + current_time + "\n" + "关闭设备")

    def get_client_screen(self):
        args_list = [1, 2]
        self.check_thread = AutoPollScreen(args_list)  # 多线程去获取
        self.check_thread.signal.connect(self.screen_callback)
        self.check_thread.start()  # 启动线程

    # 回调函数
    def screen_callback(self, value):
        if value:
            image = value[0]
            self.label_9.setPixmap(image)
        else:
            pass

    def server_callback(self, value):
        """
        回调函数中新增了连接的client，一方面去保持该client，另一方面是1、连接桌面视频2、增添combox
        :param value:
        :return:
        """
        self.update_clients()
        print(value)
        print('这里是回调函数连接成功！')
        self.check_thread = TcpLink(value)  # 多线程去获取
        self.check_thread.signal.connect(self.tcp_callback)
        self.check_thread.start()  # 启动线程

    def tcp_callback(self, value):
        print("tcp的回调函数")
        print(value)
        client_addr = value[0].get('client_addr')
        receive_msg = value[0].get('receive_msg')
        offline = value[0].get('offline')
        if offline:
            print("已经掉线")
        elif receive_msg:
            print(receive_msg)
            client_name = client_addr[0] + ':' + str(client_addr[1])
            current_time = NowTime().now_time()
            # TODO 这里应该设置多线程后台连接，设置超时10次
            self.textBrowser.append("" + current_time + "\n"
                                    + client_name + " 举手一次")

    def lock_screen(self):
        send_msg = {'lock': True}
        self.control_client(send_msg)
        current_time = NowTime().now_time()
        self.textBrowser.append("" + current_time + "\n" + "锁定计算机")

    def control_client(self, command):
        """
        发送控制指令！
        :param command: dict
        :return: None
        """
        now_client = self.current_client
        client_addr = now_client.split(':')
        conn = (client_addr[0], int(client_addr[1]))
        try:
            conn_dt[conn].sendall((str(command)).encode("utf-8"))
        except Exception as err:
            print(err)

    def broadcast(self):
        broadcast_content = self.plainTextEdit.toPlainText()
        if broadcast_content and conn_list:
            current_time = NowTime().now_time()
            # TODO 这里应该设置多线程后台连接，设置超时10次
            self.textBrowser.append("" + current_time + ": 广播一次"
                                    + broadcast_content)
            # send_msg = "{'broadcast':"+broadcast_content+"}"
            send_msg = {'broadcast': broadcast_content}
            print(conn_list)
            for client in conn_list:
                try:
                    conn_dt[client].sendall((str(send_msg)).encode("utf-8"))
                except Exception as err:
                    print(err)
                    continue
        else:
            pass

    def update_clients(self):
        """
        更新连接设备的下拉菜单
        :return:
        """
        self.comboBox.clear()
        # 从连接的设备中取地址
        connected_clients = [item[0] + ':' + str(item[1]) for item in conn_list]
        self.comboBox.addItems(connected_clients)


class Server(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.args_data = args_list

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            client_socket, client_address = socket_server.accept()
            if client_address not in conn_list:
                conn_list.append(client_address)
                conn_dt[client_address] = client_socket
                print("连接成功" + str(client_address))
            # t = threading.Thread(target=tcplink, args=(client_socket, client_address))
            # t.start()
            self.signal.emit([client_socket, client_address])  # 发射信号


class TcpLink(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.args_data = args_list

    def __del__(self):
        self.wait()

    def run(self):
        [sock, addr] = self.args_data
        callback_info = {'client_addr': addr}
        while True:
            try:
                recvdata = sock.recv(buffsize).decode('utf-8')  # 接收数据
                callback_info['receive_msg'] = recvdata
                self.signal.emit([callback_info])  # 发射信号
                if not recvdata:
                    callback_info['offline'] = addr
                    self.signal.emit([callback_info])  # 发射信号
                    break
            except:
                sock.close()
                # print(addr, 'offline')
                _index = conn_list.index(addr)
                # gui.listBox.delete(_index)
                conn_dt.pop(addr)
                conn_list.pop(_index)
                callback_info['offline'] = addr
                self.signal.emit([callback_info])  # 发射信号
                break


def tcplink(sock, addr):
    while True:
        try:
            recvdata = sock.recv(buffsize).decode('utf-8')
            print(recvdata)
            if not recvdata:
                break
        except:
            sock.close()
            print(addr, 'offline')
            _index = conn_list.index(addr)
            # gui.listBox.delete(_index)
            conn_dt.pop(addr)
            conn_list.pop(_index)
            break


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    with open('style_source_server/app_style.qss', encoding='utf-8') as f:
        qss_style = f.read()
    window.setStyleSheet(qss_style)
    window.show()
    sys.exit(app.exec_())
