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
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QCursor, QImage, QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMenu, QAction, QTreeWidgetItem, QHeaderView, QDirModel, \
    QTreeView, QFileDialog, QTableWidgetItem, QGraphicsPixmapItem, QGraphicsScene

import cv2
import requests  # 导入requests包


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

        import requests  # 导入requests包

        url = 'http://192.168.124.6:8008/'
        response = requests.get(url)
        data = response.content

        img = cv2.imread("xx.png")  # 读取图像
        # img = cv2.imread(data)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 转换图像通道
        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        self.zoomscale = 0.5  # 图片放缩尺度
        frame = QImage(img, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)  # 创建像素图元
        self.item.setScale(self.zoomscale)
        self.scene = QGraphicsScene()  # 创建场景
        self.scene.addItem(self.item)
        self.graphicsView.setScene(self.scene)  # 将场景添加至视图

        # 图片路径
        img_path = "xx.png"
        # 设置展示控件
        pic_show_label = QLabel()
        # 设置窗口尺寸
        pic_show_label.resize(300, 200)
        # 加载图片,并自定义图片展示尺寸
        image = QPixmap(img_path).scaled(300, 200)
        # 显示图片
        self.label_9.setPixmap(image)

        # url = "http://192.168.124.6:8008/"
        # res = requests.get(url)
        # img = QImage.fromData(res.content)
        # image = QPixmap.fromImage(img)
        # image = image.scaled(300,200)
        # self.label_9.setPixmap(image)

        # self.xxx()


        # 图片路径
        img_path = "xx.png"
        # 通过cv读取图片
        img = cv2.imread(img_path)
        # 通道转化
        RGBImg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 将图片转化成Qt可读格式
        image = QImage(RGBImg, RGBImg.shape[1], RGBImg.shape[0], QImage.Format_RGB888)

        # 加载图片,并自定义图片展示尺寸
        image = QPixmap(image).scaled(300, 200)
        # 显示图片
        self.label_10.setPixmap(image)

        self.setup_ui()

    def setup_ui(self):
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.close_device)  # 每次计时到时间时发出信号
        self.timer.start(500)  # 设置计时间隔并启动；单位毫秒

    # def xxx(self):
    #     while True:
    #         url = "http://192.168.124.6:8008/"
    #         res = requests.get(url)
    #         img = QImage.fromData(res.content)
    #         image = QPixmap.fromImage(img)
    #         image = image.scaled(300, 200)
    #         self.label_9.setPixmap(image)
    #         time.sleep(10)

    def choose_client(self, i):
        current_client = self.comboBox.currentText()
        print(current_client)

    def device_info(self):
        print("设备信息")

    def reboot_device(self):
        print("重启设备")

    def close_device(self):
        print("关闭设备")
        args_list = [1,2]
        self.check_thread = CheckFiles(args_list)
        self.check_thread.signal.connect(self.check_callback)
        self.check_thread.start()  # 启动线程

    # 检查后执行的回调函数
    def check_callback(self, value):
        image = value[0]
        self.label_9.setPixmap(image)

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




class CheckFiles(QThread):
    signal = pyqtSignal(list)  # 括号里填写信号传递的参数

    def __init__(self, args_list):
        super().__init__()
        self.args_data = args_list

    def __del__(self):
        self.wait()

    def run(self):
        # 进行任务操作
        try:
            url = "http://192.168.124.6:8008/"
            res = requests.get(url)
            img = QImage.fromData(res.content)
            image = QPixmap.fromImage(img)
            image = image.scaled(300, 200)
            value = [image]
            self.signal.emit(value)  # 发射信号
        except Exception as e:
            print(e)





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