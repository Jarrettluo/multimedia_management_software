# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: test
@time: 2020/11/3 23:36
"""

import requests  # 导入requests包

url = 'http://192.168.124.6:8008/'
response = requests.get(url)
data = response.content

print(data)
