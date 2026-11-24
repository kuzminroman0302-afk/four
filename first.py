import io
import random
import sys
import traceback

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QPlainTextEdit, QRadioButton, QPushButton, QLabel, QLineEdit, \
    QLCDNumber, QCheckBox, QMainWindow, QDialog
from Ui import Ui_Form

class FlagMaker(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.flag = False
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        self.setFixedSize(500, 500)

    def run(self):
        self.flag = True
        self.update()

    def paintEvent(self, event):
        if self.flag:
            qp = QPainter()
            qp.begin(self)
            self.draw_flag(qp)
            qp.end()
            self.flag = False

    def draw_flag(self, qp):
        qp.setBrush(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        size = random.randint(0, 400)
        qp.drawEllipse(100, 100, size, size)

def my_excepthook(type, value, tback):
    traceback.print_exception(type, value, tback)
sys.excepthook = my_excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlagMaker()
    ex.show()
    sys.exit(app.exec())