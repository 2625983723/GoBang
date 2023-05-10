from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSound
from gamecore import Gamecore
from gamewidgetplus import Gamewidgetplus
from netconfig import Netconfig
from netclient import Netclient
from netserver import Netserver
from PyQt5.QtWidgets import *
import json

class Netplayer(QObject):
    close_clicked=pyqtSignal()
    def __init__(self):
        super(Netplayer, self).__init__()
        self.game_core=Gamecore()
        self.game_widget=Gamewidgetplus()
        self.net_config=Netconfig()
        self.net_objet=None
        self.is_active=False
        self.m_color='black'
        self.history=[]
        self.game_widget.start_clicked.connect(self.restart_game)
        self.game_widget.goback_clicked.connect(self.closeGame)
        self.game_widget.position_clicked.connect(self.down_chess)
        self.game_widget.lose_clicked.connect(self.lose_game)
        self.game_widget.regret_clicked.connect(self.reget_game)
        self.game_widget.urge_clicked.connect(self.urge)
        self.net_config.config_signal.connect(self.reverce_config)
        self.net_config.exit_signal.connect(self.close_clicked)

    def start_game(self):
        self.net_config.show()

    def reverce_config(self,netType,name,ip,port):
        if netType == 'client':
            self.net_objet=Netclient(name,ip,port)
        elif netType=='server':
            self.net_objet=Netserver(name,ip,port)
        else:
            return
        self.game_widget.show()
        self.net_objet.build_connect()
        self.net_objet.msg_signal.connect(self.parse_data)
        self.net_config.hide()
    def init_game(self):
        self.current_color='black'
        self.history.clear()
        self.game_core.init_game()
        self.game_widget.reset()

    def _start_game(self):
        self.init_game()
        self.is_active=True

    def restart_game(self):
        msg={}
        msg['msg_type']='restart'
        self.net_objet.send_data(json.dumps(msg))

    @staticmethod
    def get_reverse_color(color):
        if color=='black':
            return 'white'
        return 'black'

    def switch_color(self):
        self.current_color=self.get_reverse_color(self.current_color)

    def closeGame(self):
        self.close_clicked.emit()
        self.game_widget.close()
        self.net_objet.socked_close()
        del self.net_objet
        self.net_objet = None

    def down_chess(self, position):
        if not self.is_active:
            return
        if self.m_color != self.current_color:
            return
        result = self.game_core.down_chessman(position[0], position[1], self.current_color)
        if result is None:
            return
        self.game_widget.down_chess(position, self.current_color)
        self.history.append(position)
        self.switch_color()
        if result != 'Down':
            self.game_win(result)
        msg={}
        msg['msg_type']='position'
        msg['x'] = position[0]
        msg['y'] = position[1]
        self.net_objet.send_data(json.dumps(msg))

    def _down_chess(self, position):
        result = self.game_core.down_chessman(position[0], position[1], self.current_color)
        self.game_widget.down_chess(position, self.current_color)
        self.history.append(position)
        self.switch_color()
        if result != 'Down':
            self.game_win(result)
            return

    def game_win(self,color):
        self.game_widget.show_win(color)
        self.is_active=False

    def lose_game(self):
        self.game_win(self.get_reverse_color(self.m_color))
        msg={}
        msg['msg_type'] = 'lose'
        self.net_objet.send_data(json.dumps(msg))


    def reget_game(self):
        if not self.is_active:
            return
        if len(self.history) <= 0:
            return
        if self.m_color != self.current_color:
            QMessageBox.warning(self.game_widget,'五子棋的消息提示','无法悔棋')
            return
        msg={}
        msg['msg_type'] = 'reget'
        self.net_objet.send_data(json.dumps(msg))

    def _reget_game(self):
        if not self.game_core.reget(*self.history.pop()):
            return
        self.game_widget.goback()

    def urge(self):
        QSound.play('source/cuicu.wav')
        msg={}
        msg['msg_type']='urge'
        self.net_objet.send_data(json.dumps(msg))


    def parse_data(self,data):
        try:
            msg=json.loads(data)
        except Exception as e:
            print(e)
            return
        if msg['msg_type'] == 'position':
            self._down_chess((int(msg['x']), int(msg['y'])))
        elif msg['msg_type'] == 'restart':
            result = QMessageBox.information(self.game_widget, '消息提示', '请求开始游戏', QMessageBox.Yes|QMessageBox.No)
            if result == QMessageBox.Yes:
                self._start_game()
                self.m_color = 'white'
                msg={}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'restart'
                msg['action_result'] = 'yes'
                self.net_objet.send_data(json.dumps(msg))
            else:
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'restart'
                msg['action_result'] = 'no'
                self.net_objet.send_data(json.dumps(msg))

        elif msg['msg_type'] == 'response':
            if msg['action_type'] == 'restart':
                if msg['action_result'] == 'yes':
                    self._start_game()
                    self.m_color = 'black'
                else :
                    QMessageBox.information(self.game_widget, '消息提示', '对方拒绝了你')
            elif msg['action_type'] == 'reget':
                if msg['action_result'] == 'yes':
                    self._reget_game()
                else:
                    QMessageBox.information(self.game_widget, '消息提示', '对方拒绝了你')

        elif msg['msg_type'] == 'reget':
            result = QMessageBox.information(self.game_widget, '消息提示', '对方请求悔棋', QMessageBox.Yes|QMessageBox.No)
            if result == QMessageBox.Yes:
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'reget'
                msg['action_type'] = 'yes'
                self.net_objet.send_data(json.dumps(msg))
                self.reget_game()
            else:
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'reget'
                msg['action_type'] = 'no'
                self.net_objet.send_data(json.dumps(msg))
                self.reget_game()
        elif msg['msg_type'] == 'lose':
            self.game_win(self.m_color)

        elif msg['msg_type'] == 'urge':
            QSound.play('source/cuicu.wav')
