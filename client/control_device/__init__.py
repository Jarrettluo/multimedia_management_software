# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: __init__
@time: 2020/11/7 9:10
"""
import os
from ctypes import *

def command_turn_off():
    """
    关闭计算机
    """
    os.system('shutdown /s /t 5')
    pass

def command_reboot_device():
    """
    重启计算机
    :return:
    """
    os.system('shutdown /r /t 5')
    pass

def command_lock_device():
    """
    睡眠计算机
    :return:
    """
    os.system('shutdown /h')
    pass

def command_lock_screen():
    """
    计算机锁屏
    :return:
    """
    user32 = windll.LoadLibrary('user32.dll')
    user32.LockWorkStation()

if __name__ == '__main__':
    command_turn_off()
    command_lock_device()
    command_lock_screen()