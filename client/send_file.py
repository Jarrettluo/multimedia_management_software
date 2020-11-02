# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: send_file
@time: 2020/11/2 19:54
"""

"""
参考资料： https://blog.csdn.net/wf134/article/details/78516148?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.pc_relevant_is_cache&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-2.pc_relevant_is_cache
https://blog.csdn.net/weixin_44649870/article/details/87367670
"""

import socket
import os
import time


filename = input('please enter the filename you want to send:\n')
filesize = str(os.path.getsize(filename))
fname1, fname2 = os.path.split(filename)
client_addr = ('127.0.0.1',9999)
f = open(filename,'rb')
count = 0
flag = 1
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#建立连接:
s.connect(('127.0.0.1', 9999))
while True:
    if count == 0:
        s.send(filesize.encode())
        start = time.time()
        s.recv(1024)
        s.send(fname2.encode())
    for line in f:
        s.send(line)
        print('sending...')
    s.send(b'end')
    break

s.close
end = time.time()
print('cost' + str(round(end - start, 2)) + 's')
