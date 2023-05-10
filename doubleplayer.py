from PyQt5.QtCore import *
from gamewidget import Gamewidget
from gamecore import Gamecore
class Doubleplayer(QObject):
    exit_clicked=pyqtSignal()
    def __init__(self):
        super(Doubleplayer, self).__init__()
        self.game_widget=Gamewidget()
        self.game_core=Gamecore()
        #当前棋子颜色
        self.current_color='black'
        #游戏状态  False
        self.is_active=False
        #历史记录
        self.history = []
        self.game_widget.start_clicked.connect(self.start_game)
        self.game_widget.goback_clicked.connect(self.stop_game)
        self.game_widget.position_clicked.connect(self.down_chess)
        self.game_widget.lose_clicked.connect(self.lose_game)
        self.game_widget.regret_clicked.connect(self.regret)
    #获得相反颜色
    @staticmethod
    def get_reverse_color(color):
        if color == 'black':
            return 'white'
        else:
            return 'black'
    #切换当前颜色
    def switch_color(self):
        self.current_color=self.get_reverse_color(self.current_color)
    #开始游戏
    def start_game(self):
        #展示游戏界面
        self.game_widget.show()
        self.game_widget.startGame()
        #初始化游戏属性
        self.init_game()
        self.is_active=True
    #初始化游戏属性
    def init_game(self):
        #初始化棋子颜色
        self.current_color='black'
        #清空历史记录
        self.history.clear()
        #棋盘信息全部重置为None
        self.game_core.init_game()
        #清空棋子显示
        self.game_widget.reset()
    #退出游戏到菜单界面
    def stop_game(self):
        self.exit_clicked.emit()
        self.game_widget.close()
    #落子逻辑
    def down_chess(self,position):
        #判断游戏状态
        if not self.is_active:
            return
        #判断是否可以落子
        result=self.game_core.down_chessman(position[0], position[1], self.current_color)
        if result is None:
            return
        #显示棋子
        self.game_widget.down_chess(position, self.current_color)
        #坐标添加到历史记录
        self.history.append(position)
        #交换棋子颜色
        self.switch_color()
        #判断输赢 展示输赢信息
        if result != 'Down':
            self.game_win(result)

    #游戏获胜方法
    def game_win(self, color):
        self.game_widget.show_win(color)
        self.is_active=False

    #认输
    def lose_game(self):
        self.game_win(self.get_reverse_color(self.current_color))
    #悔棋
    def regret(self):
        if not self.is_active:
            return
        if len(self.history) <= 0:
            return
        if not self.game_core.reget(*self.history.pop()):
            return
        self.game_widget.goback()
        self.switch_color()

