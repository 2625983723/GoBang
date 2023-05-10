import socket
from PyQt5.QtCore import *
import threading

class Netserver(QObject):
    msg_signal=pyqtSignal(str)
    def __init__(self,name,ip,port):
        super(Netserver, self).__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client_socket = None

    def build_connect(self):
        self.server_socket.bind((self.ip,int(self.port)))
        self.server_socket.listen(1)
        #创建线程链接客户端
        sthread=threading.Thread(target=self.accept_connect)
        sthread.start()


    def accept_connect(self):
        try:
            self.client_socket,cli_addr=self.server_socket.accept()
        except Exception as e:
            print("异常",e)
        while True:
            try:
                data=self.client_socket.recv(4096).decode()
                self.msg_signal.emit(data)
            except Exception as e:
                print(e)
                return

    def server_send(self,data):
        if self.client_socket is None:
            return
        self.client_socket.send(data.encode())

    def socket_close(self):
        self.server_socket.close()