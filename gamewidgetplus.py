import sys

from gamewidget import *

class Gamewidgetplus(Gamewidget):
    urge_clicked=pyqtSignal()
    def __init__(self,parent=None):
        super(Gamewidgetplus, self).__init__(parent)
        self.urge_btn=MyButton('source/催促按钮_hover.png','source/催促按钮_normal.png','source/催促按钮_press.png',parent=self)
        self.urge_btn.move(650,350)
        self.urge_btn.clinck_singal.connect(self.urge_clicked)

