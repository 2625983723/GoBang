import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime


class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game')
        self.setGeometry(100, 100, 100, 100)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)

        self.time = QTime(0, 0, 0)
        self.timeLabel = QLabel('Time: 00:00:00')

        vbox = QVBoxLayout()
        vbox.addWidget(self.timeLabel)
        self.setLayout(vbox)

        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

    def startGame(self):
        self.timer.start(1000)

    def endGame(self):
        self.timer.stop()

    def showTime(self):
        self.time = self.time.addSecs(1)
        self.timeLabel.setText('Time: ' + self.time.toString('hh:mm:ss'))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Main Window')
        self.setGeometry(100, 100, 400, 400)

        self.game = Game()
        self.game.startGame()

        vbox = QVBoxLayout()
        vbox.addWidget(self.game)
        self.setLayout(vbox)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Game()
    window.startGame()
    sys.exit(app.exec_())