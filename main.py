#五子棋启动类
import sys
from netplayer import Netplayer
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from menuwidget import MenuWidget
from doubleplayer import Doubleplayer
from singleplayer import singleplayer
from PyQt5.QtMultimedia import QSound
class Main(QObject):
    def __init__(self):
        super(Main, self).__init__()
        self.menu_widget=MenuWidget()
        self.double_player=Doubleplayer()
        self.singleplayer=singleplayer()
        self.net_player = Netplayer()
        self.a1=QSound('source/luozisheng.wav')

        #信号来来连接槽函数
        self.menu_widget.double_clicked.connect(self.start_double)
        self.double_player.exit_clicked.connect(self.menu_widget.show)

        #人机对战
        self.menu_widget.single_clicked.connect(self.start_single)
        self.singleplayer.exit_clicked.connect(self.menu_widget.show)
        self.menu_widget.network_clicked.connect(self.start_net)
        self.net_player.close_clicked.connect(self.menu_widget.show)


    def start_net(self):
        self.net_player.start_game()
        self.menu_widget.hide()

    #游戏启动
    def start_game(self):
        self.menu_widget.show()

    #启动双人对战
    def start_double(self):
        self.double_player.start_game()
        # 隐藏菜单界面
        self.menu_widget.hide()
    #启动人机对战方法
    def start_single(self):
        self.singleplayer.start_game()
        self.menu_widget.hide()

if __name__=='__main__':
    app=QApplication(sys.argv)
    main=Main()
    main.start_game()
    sys.exit(app.exec_())




