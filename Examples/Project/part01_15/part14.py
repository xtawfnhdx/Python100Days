from time import time
from threading import Thread
import requests


# ---------------------------------------
#  示例1
# ---------------------------------------
class DownloadHandler01(Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        filename = self.url[self.url.rfind('/') + 1:]
        resp = requests.get(self.url)
        # open 使用wb时，如果有文件夹，并且文件夹不存在，则会报错，不会创建文件夹
        with open('part_14_ex01.jpg', 'wb') as f:
            f.write(resp.content)
            f.close()


def main01():
    # resp = requests.get('https://bing.ioliu.cn/v1/rand ')
    # data_model = resp.json()
    # for mm_dict in data_model['newslist']:
    # url = mm_dict['picUrl']
    DownloadHandler01('https://unsplash.it/1600/900?random').start()


# ---------------------------------------
#  示例2  使用socket
# ---------------------------------------
from socket import socket, SOCK_STREAM, AF_INET
import datetime


def main02():
    server = socket(family=AF_INET, type=SOCK_STREAM)
    # bind时的IP不能乱写，可以不写，也可以写本机IP
    # 否则报错“[WinError 10049] 在其上下文中，该请求的地址无效”
    server.bind(('192.168.1.132', 6789))
    server.listen(512)
    print('服务器开始启动监听')
    while True:
        client, addr = server.accept()
        print(str(addr) + '连接到了服务器')
        client.send(str(datetime.datetime.now()).encode('utf-8'))
        client.close()


# ---------------------------------------
#  示例3  使用socket
# ---------------------------------------
from socket import socket, SOCK_STREAM, AF_INET
from base64 import b64encode, b64decode
from json import dumps, loads
from threading import Thread


def main03():
    class FileTransferHandler(Thread):
        def __init__(self, cclient):
            super().__init__()
            self.cclient = cclient

        def run(self):
            my_dict = {}
            my_dict["filename"] = "part_14_ex01.jpg"
            my_dict["filedata"] = data
            json_str = dumps(my_dict)
            self.cclient.send(json_str.encode('utf-8'))
            self.cclient.close()

    server = socket()
    server.bind(('192.168.1.132', 5566))
    server.listen(512)
    print('服务器开始监听')
    with open('../part_14_ex01.jpg', 'rb') as f:
        data = b64encode(f.read()).decode('utf-8')
    while True:
        client, addr = server.accept()
        FileTransferHandler(client).start()


if __name__=="__main__":
    main03()