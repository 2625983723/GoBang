import socket
import threading

from PyQt5.QtCore import *

class Netclient(QObject):
    msg_signal=pyqtSignal(str)
    def __init__(self, name, ip, port):
        super(Netclient, self).__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def build_connect(self):
        self.client_socket.connect((self.ip, int(self.port)))
        cthread = threading.Thread(target=self.recv_data)
        cthread.start()

    def recv_data(self):
        while 1:
            try:
                data=self.client_socket.recv(4096).decode()
                self.msg_signal.emit(data)
            except Exception as e:
                print(e)
                return None

    def send_data(self, data):
        self.client_socket.send(data.encode())

    def socket_close(self):
        self.client_socket.close()



