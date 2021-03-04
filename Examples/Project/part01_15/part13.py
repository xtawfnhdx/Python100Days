from threading import Thread, Lock
import multiprocessing
import os
from random import randint
from time import time, sleep
import queue


# ---------------------------------------
#  示例1
# ---------------------------------------
def download_task01(filename):
    print('启动%s 文件开始下载,进程号[%d]' % (filename, os.getpid()))
    time_to_download = randint(5, 10)
    sleep(time_to_download)
    print('%s下载完成，耗费了%d秒' % (filename, time_to_download))


def main01():
    start = time()
    # target：执行哪个函数  args:参数
    p1 = multiprocessing.Process(target=download_task01, args=('文件001.pdf',))
    # 启动
    p1.start()
    p2 = multiprocessing.Process(target=download_task01, args=('歌曲002.MP3',))
    p2.start()
    # 等待执行结果
    p1.join()
    p2.join()
    end = time()
    print('总共耗时%.2f秒' % (end - start))


# ---------------------------------------
#  示例2
# ---------------------------------------
def download_task02(filename):
    print('%s 开始下载' % filename)
    time_to_download = randint(5, 10)
    sleep(time_to_download)
    print('%s 下载完成，用时 %d' % (filename, time_to_download))


def main02():
    start = time()
    t1 = Thread(target=download_task02, args=('Python从入门到精通',))
    t2 = Thread(target=download_task02, args=('文件下载2.ppt',))
    t1.start()
    t2.start()
    t1.join()

    t2.join()
    end = time()
    print('总共耗时 %d ' % (end - start))


# ---------------------------------------
#  示例3
# ---------------------------------------
def show_info03(title):
    print(title)
    print('model name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print('\n\n')


def f03(name):
    show_info03('function f')
    print(name)


def main03():
    show_info03('main process line')
    p = multiprocessing.Process(target=f03, args=('children process',))
    p.start()
    print('p start')
    p.join()


# ---------------------------------------
#  示例4
# ---------------------------------------


def p_put04(*args):
    q04.put(args)
    print('Has put %s' % args)


def p_get04(*args):
    print('%s wait to get...' % args)
    print(q04.get())
    print('%s got it' % args)


q04 = queue.Queue()


def main04():
    p041 = multiprocessing.Process(target=p_put04, args=('p1',))
    p042 = multiprocessing.Process(target=p_get04, args=('p2',))
    p041.start()
    p042.start()


# ---------------------------------------
#  示例5  使用管道
# ---------------------------------------

def f05(conn):
    conn.send('send by child')
    print('child recv:', conn.recv())
    conn.close()


# Pipe 管道
parent_conn, child_conn = multiprocessing.Pipe()


def main05():
    p05 = multiprocessing.Process(target=f05, args=(child_conn,))
    p05.start()
    print('parent recv:', parent_conn.recv())
    parent_conn.send('send by parent')
    p05.join()


# ---------------------------------------
#  示例6  临界资源 没有锁
# ---------------------------------------
class Account06(object):
    def __init__(self):
        self._balance = 0

    def deposit(self, money):
        new_balance = self._balance + money
        sleep(0.01)
        self._balance = new_balance

    # 标记为属性(该标记叫做装饰器)
    @property
    def balance(self):
        return self._balance


class AddMoneyThread06(Thread):
    def __init__(self, account, money):
        super().__init__()
        self._account = account
        self._money = money

    def run(self):
        self._account.deposit(self._money)


def main06():
    account = Account06()
    threads06 = []
    # 创建100个线程向同一账户中存入1元
    for _ in range(100):
        t = AddMoneyThread06(account, 1)
        threads06.append(t)
        t.start()
    # 等所有的线程都执行完成
    for t in threads06:
        t.join()
    print('账户里的钱为：￥%d元' % account.balance)


# ---------------------------------------
#  示例7  临界资源 加锁
# ---------------------------------------
class Account07(object):
    def __init__(self):
        self._balance = 0
        self._lock = Lock()

    def deposit(self, money):
        self._lock.acquire()
        try:

            new_balance = self._balance + money
            sleep(0.01)
            self._balance = new_balance
        finally:
            self._lock.release()

    # 标记为属性(该标记叫做装饰器)
    @property
    def balance(self):
        return self._balance


class AddMoneyThread07(Thread):
    def __init__(self, account, money):
        super().__init__()
        self._account = account
        self._money = money

    def run(self):
        self._account.deposit(self._money)


def main07():
    account = Account07()
    threads07 = []
    # 创建100个线程向同一账户中存入1元
    for _ in range(100):
        t = AddMoneyThread07(account, 1)
        threads07.append(t)
        t.start()
    # 等所有的线程都执行完成
    for t in threads07:
        t.join()
    print('账户里的钱为：￥%d元' % account.balance)


# ---------------------------------------
#  示例8  单线程异步I/O  协程模式
# ---------------------------------------
import time
# tkinter 是python的标准TK GUI工具包接口
import tkinter
import tkinter.messagebox


def main08():
    class DownloadTaskHandler(Thread):
        def run(self):
            time.sleep(10)
            tkinter.messagebox.showinfo('提示', '下载完成！')
            button1.config(state=tkinter.NORMAL)

    def download():
        button1.config(state=tkinter.DISABLED)
        DownloadTaskHandler(daemon=True).start()

    def show_about():
        tkinter.messagebox.showinfo('关于', '作者：XXX')

    top = tkinter.Tk()
    top.title('单线程')
    top.geometry('200x150')
    top.wm_attributes('-topmost', 1)

    panel = tkinter.Frame(top)
    button1 = tkinter.Button(panel, text='下载', command=download)
    button1.pack(side='left')
    button2 = tkinter.Button(panel, text='关于', command=show_about)
    button2.pack(side='right')
    panel.pack(side='bottom')

    tkinter.mainloop()
