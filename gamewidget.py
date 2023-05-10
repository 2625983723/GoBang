import sys
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from chessman import Chessman
from mybutton import MyButton


#游戏界面类
class Gamewidget(QWidget):
    goback_clicked = pyqtSignal()
    start_clicked = pyqtSignal()
    regret_clicked = pyqtSignal()
    lose_clicked = pyqtSignal()
    #点击落子信号
    position_clicked=pyqtSignal(tuple)#x,y
    def __init__(self,parent=None):
        super(Gamewidget, self).__init__(parent)
        self.initui()
        self.chessman_list=[]
    def initui(self):
        # 设置窗口大小
        self.setFixedSize(760, 650)
        # 设置标题
        self.setWindowTitle('五子棋游戏')
        # 窗口图标
        self.setWindowIcon(QIcon('source/黑子.jpg'))
        # 设置背景图
        # 获取当前窗口调色板
        p = QPalette(self.palette())
        # 上传图片
        brush = QBrush(QImage('source/游戏界面.png'))
        # 设置调色板
        p.setBrush(QPalette.Background, brush)
        # 给窗口设置新的调色板
        self.setPalette(p)
        self.goback_button = MyButton(
            'source/返回按钮_hover.png',
            'source/返回按钮_normal.png',
            'source/返回按钮_press.png',
            parent=self)
        self.goback_button.move(650, 50)

        self.start_button = MyButton(
            'source/开始按钮_hover.png',
            'source/开始按钮_normal.png',
            'source/开始按钮_press.png',
            parent=self)
        self.start_button.move(650, 200)

        self.regret_button = MyButton(
            'source/悔棋按钮_hover.png',
            'source/悔棋按钮_normal.png',
            'source/悔棋按钮_press.png',
            parent=self)
        self.regret_button.move(650, 300)

        self.lose_button = MyButton(
            'source/认输按钮_hover.png',
            'source/认输按钮_normal.png',
            'source/认输按钮_press.png',
            parent=self)
        self.lose_button.move(650, 400)
        #绑定信号与槽
        self.goback_button.clinck_singal.connect(self.goback_clicked)
        self.start_button.clinck_singal.connect(self.start_clicked)
        self.regret_button.clinck_singal.connect(self.regret_clicked)
        self.lose_button.clinck_singal.connect(self.lose_clicked)
        #设置标识
        self.focus_point=QLabel(self)
        self.focus_point.setPixmap(QPixmap('source/标识.png'))
        self.focus_point.setFixedSize(QPixmap('source/标识.png').size())
        self.focus_point.hide()#隐藏
        #创建lable显示输赢结果
        self.win_lbl=QLabel(self)
        self.win_lbl.hide()
        self.gametime_button = QLabel(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)


        self.time = QTime(0, 0, 0)
        self.timeLabel = QLabel('Time: 00:00:00')
        self.timeLabel.setFixedSize(200, 50)
        layout = QFormLayout()
        layout.addWidget(self.timeLabel)
        # self.menu_widget.setLayout(layout)
        self.setLayout(layout)
        self.timeLabel.show()
    #重置游戏
    def showTime(self):
        self.time = self.time.addSecs(1)
        self.timeLabel.setText('Time: ' + self.time.toString('hh:mm:ss'))

    def startGame(self):
        self.timer.start(1000)

    def reset(self):
        self.focus_point.hide()#隐藏标识
        for chessman in self.chessman_list:
            chessman.close()#关闭棋子显示
            del chessman  #删除对象  释放资源
        self.chessman_list.clear()
        self.win_lbl.hide()#隐藏输赢判断
    #悔棋
    def goback(self):
        if len(self.chessman_list)>0:#判断列表是否有棋子
            #删除最后一颗棋子，获取这颗棋子
            chessman = self.chessman_list.pop()
            chessman.close()#关闭棋子显示
            del chessman #删除棋子对象
            self.focus_point.hide()#隐藏标识

    #显示输赢
    def show_win(self,color):
        if color == 'black':
            self.win_lbl.setPixmap(QPixmap('source/黑棋胜利.png'))
            self.win_lbl.show()
            self.win_lbl.move(100,100)
            self.win_lbl.raise_()
        elif color == 'white':
            self.win_lbl.setPixmap(QPixmap('source/白棋胜利.png'))
            self.win_lbl.show()
            self.win_lbl.move(100,100)
            self.win_lbl.raise_()
    #讲点击坐标，转为位置坐标
    @staticmethod
    def reverse_to_postion(coordinate):
        pos_x=coordinate.x()
        pos_y=coordinate.y()
        #左边界  上边界  x=50-15  y=50-15
        #右边界  下边界  x=50+18*30+15    y=50+18*30+15
        if pos_x <= 35 or pos_x >= 605 or pos_y <= 35 or pos_y >= 605:
            return None
        #坐标在转换   点击坐标转换为位置坐标
        block_x = (pos_x-35)//30
        block_y = (pos_y-35)//30
        return (block_x,block_y)
    #获取鼠标点击坐标，发射坐标信号
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        #使用reverse_to_postion方法 讲a0点击坐标转换为位置坐标
        position=self.reverse_to_postion(coordinate=a0)
        if position is None:
            return
        else:
            self.position_clicked.emit(position)
    #将位置坐标转为落子交点像素坐标
    @staticmethod
    def reverse_to_coordinate(position):
        x = 50+position[0]*30
        y = 50+position[1]*30
        return (x, y)
    #落子
    def down_chess(self, position, color):
        chessman = Chessman(color, self)
        chessman.setindex(x=position[0], y=position[1])
        point = QPoint(*self.reverse_to_coordinate(position))
        chessman.move(point)
        chessman.show()
        self.chessman_list.append(chessman)
        #落子音效
        QSound.play('source/luozisheng.wav')
        self.focus_point.move(point.x()-15, point.y()-15)
        self.focus_point.show()
        #标识顶层显示
        self.focus_point.raise_()

##以下为测试代码
class testobject(QObject):
    def __init__(self, w):
        super().__init__()
        self.w = w
    def reverse_data(self, data):
        w.down_chess(data, 'black')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Gamewidget()
    w.startGame()
    w.show()
    # w.show_win('white')
    # w.down_chess((1,0),'black')
    # w.down_chess((5,5), 'black')
    obj = testobject(w)
    w.position_clicked.connect(obj.reverse_data)
    sys.exit(app.exec_())