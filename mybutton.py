import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui,QtCore

#自定义按钮类
class MyButton(QLabel):
    clinck_singal=pyqtSignal()#自定义信号
    def __init__(self,*args,parent=None):
        super(MyButton, self).__init__(parent)
        self.hoverPixmap=QPixmap(args[0])#加载图片
        self.normalPixmap=QPixmap(args[1])
        self.pressPixmap=QPixmap(args[2])
        #标记鼠标位置 按钮上方：True   按钮外面：False
        self.enterState=False
        self.setPixmap(self.normalPixmap)
        self.setFixedSize(self.normalPixmap.size())

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        print('鼠标释放')
        if self.enterState:
            #True  悬浮状态
            self.setPixmap(self.hoverPixmap)
        else:
            #false  正常状态
            self.setPixmap(self.normalPixmap)
        self.clinck_singal.emit()
    def mousePressEvent(self,event):
        print('鼠标按压')
        self.setPixmap(self.pressPixmap)
    def enterEvent(self, a0: QtCore.QEvent):
        print('鼠标进入')
        self.setPixmap(self.hoverPixmap)
        self.enterState=True
    def leaveEvent(self, a0: QtCore.QEvent):
        print('鼠标离开')
        self.setPixmap(self.normalPixmap)
        self.enterState=False
if __name__ == '__main__':
    a=QApplication(sys.argv)
    w=QWidget()
    btn=MyButton('source/人机对战_hover.png',
                 'source/人机对战_normal.png',
                 'source/人机对战_press.png',parent=w)
    btn.clinck_singal.connect(w.close)
    btn.move(100,100)
    w.show()
    sys.exit(a.exec_())









