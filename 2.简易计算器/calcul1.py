#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --*-- coding:utf-8 --*--
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QFont
from PyQt5 import QtWidgets
from PyQt5.Qt import *

class Calculator(QtWidgets.QWidget):
    def __init__(self):
        super(Calculator, self).__init__()
        self.initUI()
        self.reset()
        self.display.setText("0")

    def initUI(self):
        self.resize(400,450)
        self.adjustSize()
        self.setWindowTitle('简易计算器')
        Grid = QtWidgets.QGridLayout()

        self.display = QtWidgets.QLineEdit('')
        self.display.setFont(QFont("Times", 20))
        self.display.setReadOnly(True)
        self.display.setAlignment(QtCore.Qt.AlignRight)
        self.display.setMaxLength(20)
        Grid.addWidget(self.display, 0, 0, 1, 4)

        names = ['C', '(', 'Del', '+',
                 '7', '8', '9', '-',
                 '4', '5', '6', '*',
                 '1', '2', '3', '/',
                 '0', '.', ')', '=']
        pos = [(0, 0), (0, 1), (0, 2), (0, 3),
               (1, 0), (1, 1), (1, 2), (1, 3),
               (2, 0), (2, 1), (2, 2), (2, 3),
               (3, 0), (3, 1), (3, 2), (3, 3),
               (4, 0), (4, 1), (4, 2), (4, 3)]
        c = 0
        for name in names:
            button = QtWidgets.QPushButton(name)
            button.setFixedSize(QtCore.QSize(100, 60))
            button.setFont(QFont('Times', 30))
            button.clicked.connect(self.ButtonClicked)
            Grid.addWidget(button, pos[c][0] + 1, pos[c][1])
            c = c + 1

        self.setLayout(Grid)

    def ButtonClicked(self):
        text = self.sender().text()
        if text == "=":
            r = eval(self.number)
            #print(self.number)
            #result = str(r).decode('ascii')
            result = str(r)
            self.display.setText(str(result))  #计算结果
            self.number = result
        elif text == "Del":
            self.number = self.number[:-1]
            self.display.setText(self.number)
        elif text == "C":
            self.reset()
            self.display.setText(self.number)
        else:
            if text in "+-*/":
                self.number = self.number + text
            else:
                print(text)
                if self.number[-1] == '/' and text == '0':
                    QMessageBox.critical(self, '提示', '除数不能为0')
                else:
                    self.number = self.number + text if self.number != "0" else text

            self.display.setText(str(self.number))

    def reset(self):
        self.number = "0"

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Calculator()
    ex.show()
    sys.exit(app.exec_())