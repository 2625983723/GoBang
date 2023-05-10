#核心类，无需界面直接继承QObject
from PyQt5.QtCore import QObject
class Gamecore(QObject):
    """
    记录棋盘信息，落子回合，判断输赢  悔棋
    """
    def __init__(self):
        super(Gamecore, self).__init__()
        #创建二维列表  记录棋盘信息
        self.chessboard=[[None for i in range(19)]for i in range(19)]
        print(self.chessboard)
    #初始化游戏
    def init_game(self):
        #遍历横坐标
        for i in range(19):
            #遍历纵坐标
            for j in range(19):
                #拿值全部赋值为None
                self.chessboard[i][j]=None
    #落子方法  放在二维列表  进行判断输赢 x，y，color
    def down_chessman(self, x, y, color):
        #判断是否可以落子
        #如果不为空  不能落子  返回None告诉用户不能落子
        if self.chessboard[y][x] is not None:
            return None
        #获取位置的none赋值color
        self.chessboard[y][x] = color
        #判断输赢
        return self.judge_win(x, y, color)
    #悔棋：
    def reget(self,x,y):
        #判断是否为空  为空不能悔棋
        if self.chessboard[y][x] is None:
            return False
        #不为空 悔棋  赋值为None
        self.chessboard[y][x] = None
        return True

    #胜利判断  x，y，color
    def judge_win(self, x, y, color):  # x: 水平坐标，y:垂直坐标 i:水平坐标 j:垂直坐标
        # 水平方向 y 相同 chessboard[chessman.y][i]
        # print('judge:', x, y)
        count = 1
        # 左边
        i = x - 1
        while i >= 0:
            if self.chessboard[y][i] == None \
                    or self.chessboard[y][i] != color:
                break
            count += 1
            i -= 1
        # 右边
        i = x + 1
        while i <= 18:
            if self.chessboard[y][i] == None or self.chessboard[y][i] != color:
                break
            count += 1
            i += 1

        if count >= 5:
            return color

        # 竖直方向 x 相同 chessboard[j][chessman.x]
        count = 1
        # 上边
        j = y - 1
        while j >= 0:
            if self.chessboard[j][x] == None or self.chessboard[j][x] != color:
                break
            count += 1
            j -= 1
        # 下边
        j = y + 1
        while j <= 18:
            if self.chessboard[j][x] == None or self.chessboard[j][x] != color:
                break
            count += 1
            j += 1

        if count >= 5:
            return color

        # 正斜线
        count = 1
        # 右上
        j, i = y - 1, x + 1
        while j >= 0 and i <= 18:
            if self.chessboard[j][i] == None or self.chessboard[j][x] != color:
                break
            count += 1
            j -= 1
            i += 1
        # 左下
        j, i = y + 1, x - 1
        while i >= 0 and j <= 18:
            if self.chessboard[j][i] == None or self.chessboard[j][i] != color:
                break
            count += 1
            i -= 1
            j += 1
        if count >= 5:
            return color

        # 反斜线
        count = 1
        # 左上
        j, i = y - 1, x - 1
        while j >= 0 and i >= 0:
            if self.chessboard[j][i] == None or self.chessboard[j][i] != color:
                break
            count += 1
            j -= 1
            i -= 1
        # 右下
        j, i = y + 1, x + 1
        while i <= 18 and j <= 18:
            if self.chessboard[j][i] == None or self.chessboard[j][i] != color:
                break
            count += 1
            i += 1
            j += 1
        if count >= 5:
            return color
        return 'Down'



a=Gamecore()
print(a.down_chessman(1, 1, 'black'))
print(a.down_chessman(2, 1, 'black'))
print(a.down_chessman(3, 1, 'black'))
print(a.down_chessman(4, 1, 'black'))
print(a.down_chessman(5, 1, 'black'))
