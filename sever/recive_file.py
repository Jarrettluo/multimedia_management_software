# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: recive_file
@time: 2020/11/2 19:54
"""

import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)
print('Waiting for connection...')

count = 0

while True:
    sock, addr = s.accept()
    print('Accept new connection from %s:%s...' % addr)
    if count == 0:
        data1 = sock.recv(1024)
        print(str(data1))
        file_total_size = int(data1.decode())
        received_size = 0
        sock.send('received'.encode())
        data = sock.recv(1024)
        filepath = str(data.decode())
        f = open(filepath, 'wb')
    while received_size < file_total_size:
        data = sock.recv(1024)
        f.write(data)
        received_size += len(data)
        print('已接收 ', received_size, ' Byte')
    data = sock.recv(1024)
    if data == b'end':
        count += 1
        break

f.close()
s.close()
