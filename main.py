import io
import random
import sqlite3
import sys
import traceback

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter, QColor
from PyQt6.QtWidgets import QApplication, QWidget, QPlainTextEdit, QRadioButton, QPushButton, QLabel, QLineEdit, \
    QLCDNumber, QCheckBox, QMainWindow, QDialog


class FlagMaker(QWidget):
    def __init__(self):
        super().__init__()
        self.flag = False
        uic.loadUi('main.ui', self)
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        text = cur.execute('''select * from films''').fetchall()
        cur.close()
        text1 = []
        for i in text:
            t = ''
            for j in i:
                t += str(j) + " "
            text1.append(t)
        self.textBrowser.setHtml(f"<p>{"".join(text1)}</p>")
        self.setFixedSize(500, 500)

def my_excepthook(type, value, tback):
    traceback.print_exception(type, value, tback)
sys.excepthook = my_excepthook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FlagMaker()
    ex.show()
    sys.exit(app.exec())