#人机算法类
class GobangAlogotiem(object):
    def __init__(self,chessboard):
        self.chessboard=chessboard

    def get_point_score(self, x, y, color):
        '''
        返回每个点的得分
        y:行坐标 垂直
        x:列坐标 水平
        color：棋子颜色
        :return:
        '''
        # 分别计算点周围5子以内，空白、和同色的分数
        blank_score = 0
        color_score = 0

        # 记录该点的每条线的棋子分数
        blank_score_plus = [0, 0, 0, 0]  # 横向 纵向 正斜线 反斜线
        color_score_plus = [0, 0, 0, 0]

        # 横线
        # 右侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
        # print('123123')
        # 左侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1

        # 竖线
        # 上方
        i = x  # 横坐标
        j = y  # 纵坐标
        while j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break
            if j <= y - 4:
                break
            j -= 1
        # 竖线
        # 下方
        i = x  # 横坐标
        j = y  # 纵坐标
        while j < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break

            if j >= y + 4:  # 最近五个点
                break
            j += 1
        # 正斜线
        # 右上
        i = x
        j = y
        while i < 19 and j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[2] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break

            if i >= x + 4:  # 最近五个点
                break
            i += 1
            j -= 1
        # 左下
        i = x
        j = y
        while j < 19 and i >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[2] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break

            if j >= y + 4:  # 最近五个点
                break
            i -= 1
            j += 1
        # 反斜线
        # 左上
        i = x
        j = y
        while i >= 0 and j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[3] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1
            j -= 1
        # 右上
        i = x
        j = y
        while i < 19 and j < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[3] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
            j += 1

        for k in range(4):
            if color_score_plus[k] >= 5:
                return 100

        # color_score *= 5
        return max([x + y for x, y in zip(color_score_plus, blank_score_plus)])

    #获取落子位置
    def get_point(self):
        white_score=[[0 for i in range(19)] for j in range(19)]
        black_score = [[0 for i in range(19)] for j in range(19)]
        #模拟落子之前 判断是否能落子
        for i in range(19):
            for j in range(19):
               if self.chessboard[i][j] != None:
                   continue
               #模拟落子
               self.chessboard[i][j]='white'
               white_score[i][j]=self.get_point_score(j,i,'white')
               self.chessboard[i][j] = None
               self.chessboard[i][j]='black'
               black_score[i][j]=self.get_point_score(j,i,'black')
               #清空模拟落子
               self.chessboard[i][j]=None
        #将二维列表转换为一维列表
        r_white_score=[]
        r_black_score=[]
        for i in white_score:
            r_white_score.extend(i)
        for i in black_score:
            r_black_score.extend(i)
        #找到black和white的分值最大值
        socre=[max(x,y) for x,y in zip(r_black_score,r_white_score)]
        print(socre)
        #找最大分数坐标
        chess_index=socre.index(max(socre))
        print(chess_index)
        y=chess_index//19
        x=chess_index%19
        print(x,y)
        return (x,y)








