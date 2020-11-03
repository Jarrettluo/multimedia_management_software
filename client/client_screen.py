# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: client_screen
@time: 2020/11/3 22:16
"""


from http.server import BaseHTTPRequestHandler, HTTPServer
import pyautogui
import socket
# for windows, screenshot.py
# 家长监控地址: http://192.168.1.3:8009/
PORT = 8008
# 获取学生机局域网地址
IP = socket.gethostbyname(socket.gethostname())
#windows
class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        img = pyautogui.screenshot() #屏幕截图
        if img:
            self.send_response(200) #HTTP 状态码
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            img.save(self.wfile, 'PNG') # 写入HTTP 响应流文件


def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #判断当前端口是否已经打开
        result = sock.connect_ex((IP, PORT))
        portopen = result == 0
        sock.close()
        if not portopen:
            #启动web服务器，用自定义的响应处理类
            server = HTTPServer((IP, PORT), myHandler)
            server.serve_forever() # 服务器持续监听
    except:
        pass

if __name__ == '__main__':
    main()