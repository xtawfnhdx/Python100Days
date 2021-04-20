from socket import socket, SOCK_STREAM, AF_INET
from base64 import b64encode, b64decode
from json import dumps, loads


def main04():
    client = socket()
    client.connect(('192.168.1.132', 5566))
    in_data = bytes()
    data = client.recv(1024)
    while data:
        in_data += data
        data = client.recv(1024)
    my_dict = loads(in_data.decode('utf-8'))
    ffilename = my_dict["filename"]
    filedata = my_dict["filedata"].encode('utf-8')
    with open('part14_ex03.jpg', 'wb') as f:
        f.write(b64decode(filedata))
    print('图片已保存')


if __name__ == "__main__":
    main04()
