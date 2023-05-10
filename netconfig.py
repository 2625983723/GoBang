"""配置网络联机窗口"""
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import socket

#网络配置窗口
class Netconfig(QWidget):
    #自定退出信号
    exit_signal=pyqtSignal()
    #自定义配置信号   我是主机  server   连接主机 client
    config_signal=pyqtSignal(str,str,str,str)
    def __init__(self,parent=None):
        super(Netconfig, self).__init__(parent)
        self.initUi()
    def initUi(self):
        self.setWindowTitle('网络配置')
        #构建控件 玩家姓名
        self.name_label=QLabel('姓名：',self)
        self.name_input=QLineEdit('玩家1',self)

        self.ip_label = QLabel('ip:',self)
        self.ip_input = QLineEdit('127.0.0.1',self)
        self.port_label= QLabel('port:',self)
        self.port_input = QLineEdit('8888',self)

        self.client_button=QPushButton('我是客户',self)
        self.sever_button=QPushButton('我是主机',self)


        #构造网格布局
        gridlayout=QGridLayout()
        gridlayout.addWidget(self.name_label,0,0)
        gridlayout.addWidget(self.name_input,0,1)
        gridlayout.addWidget(self.ip_label,1,0)
        gridlayout.addWidget(self.ip_input,1,1)
        gridlayout.addWidget(self.port_input,2,1)
        gridlayout.addWidget(self.port_label,2,0)
        gridlayout.addWidget(self.client_button,3,0)
        gridlayout.addWidget(self.sever_button,3,1)
        #设置窗口布局
        self.setLayout(gridlayout)

        self.client_button.clicked.connect(self.client_btn_func)
        self.sever_button.clicked.connect(self.sever_btn_func)

    def client_btn_func(self):          #发射四个信号
        self.config_signal.emit('client',self.name_input.text(),self.ip_input.text(),self.port_input.text())

    def sever_btn_func(self):          #发射四个信号
        self.config_signal.emit('server',self.name_input.text(),self.ip_input.text(),self.port_input.text())

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.close()
        self.exit_signal.emit()





if __name__=='__main__':
    app=QApplication(sys.argv)
    w=Netconfig()
    w.show()
    sys.exit(app.exec_())