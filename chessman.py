import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

#棋子类  color :black  white
class Chessman(QLabel):
    def __init__(self,color='black',parent=None):
        super(Chessman, self).__init__(parent)
        self.color=color
        self.pic=None
        if self.color=='black':
            self.pic=QPixmap('source/黑子.png')
        else:
            self.pic=QPixmap('source/白子.png')
        self.setPixmap(self.pic)
        self.setFixedSize(self.pic.size())
        self.x=0
        self.y=0

    #移动棋子
    def move(self, a0: QtCore.QPoint):
        super().move(a0.x()-15,a0.y()-15)

    #设置点位
    def setindex(self,x,y):
        self.x=x
        self.y=y

if __name__=='__main__':
    app=QApplication(sys.argv)
    chessman=Chessman()
    chessman.show()
    chessman.move(QPoint(1000,500))
    sys.exit(app.exec_())