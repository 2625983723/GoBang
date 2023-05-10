from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mybutton import MyButton
import sys
#菜单界面类
class MenuWidget(QWidget):
    single_clicked=pyqtSignal()
    double_clicked=pyqtSignal()
    network_clicked=pyqtSignal()
    def __init__(self, parent = None):
        super().__init__(parent)
        self.initui()
    def initui(self):
        #设置窗口大小
        self.setFixedSize(760,650)
        #设置标题
        self.setWindowTitle('五子棋游戏')
        #窗口图标
        self.setWindowIcon(QIcon('source/黑子.jpg'))
        #设置背景图
        #获取当前窗口调色板
        p=QPalette(self.palette())
        #上传图片
        brush=QBrush(QImage('source/五子棋界面.png'))
        #设置调色板
        p.setBrush(QPalette.Background,brush)
        #给窗口设置新的调色板
        self.setPalette(p)
        #定义按钮
        self.duble_button=MyButton('source/双人对战_hover.png',
                                   'source/双人对战_normal.png',
                                   'source/双人对战_press.png',
                                   parent=self)
        self.duble_button.move(250,450)
        self.duble_button.clinck_singal.connect(self.double_clicked)
        self.single_button = MyButton('source/人机对战_hover.png',
                                     'source/人机对战_normal.png',
                                     'source/人机对战_press.png',
                                     parent=self)
        self.single_button.move(250, 550)
        self.single_button.clinck_singal.connect(self.single_clicked)
        #人机对战
        #联机对战
        self.network_button=MyButton('source/联机对战_hover.png',
                                     'source/联机对战_normal.png',
                                     'source/联机对战_press.png',
                                     parent=self)
        self.network_button.move(250,350)
        self.network_button.clinck_singal.connect(self.network_clicked)

if __name__=='__main__':
    app=QApplication(sys.argv)
    w=MenuWidget()
    l=QLabel('已经被点击！')
    w.double_clicked.connect(l.show)
    w.show()
    sys.exit(app.exec_())
