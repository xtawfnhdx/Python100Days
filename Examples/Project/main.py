from multiprocessing import Process
from os import getpid
from random import randint
from time import time, sleep


def download_task(filename):
    print('启动%s 文件开始下载,进程号[%d]' % (filename, getpid()))
    time_to_download = randint(5, 10)
    sleep(time_to_download)
    print('%s下载完成，耗费了%d秒' % (filename, time_to_download))


def main():
    start = time()
    #target：执行哪个函数  args:参数
    p1 = Process(target=download_task, args=('文件001.pdf',))
    p1.start()
    p2 = Process(target=download_task, args=('歌曲002.MP3',))
    p2.start()
    p1.join()
    p2.join()
    end = time()
    print('总共耗时%.2f秒' % (end - start))


if __name__ == '__main__':
    main()