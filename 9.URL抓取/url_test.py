#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import requests

class MyTest(QWidget):

    def __init__(self, parent=None):
        super(MyTest, self).__init__(parent)

        self.label = QLabel(self)
        self.label.setText("网址")
        self.lineEdit = QLineEdit()
        #self.lineEdit.setText("http://www.baidu.com")
        self.button = QPushButton("开始")
        self.text = QTextEdit()
        #信号于槽
        self.button.clicked.connect(self.getstr)
        #布局嵌套
        wlayout = QVBoxLayout(self) #全局布局
        hlayout = QHBoxLayout() #局部布局
        vlayout = QVBoxLayout() #局部布局

        hlayout.addWidget(self.label)
        hlayout.addWidget(self.lineEdit)
        hlayout.addWidget(self.button)
        vlayout.addWidget(self.text)

        wlayout.addLayout(hlayout) #将局部布局加到全局布局中
        wlayout.addLayout(vlayout)
        #添加标题
        self.setWindowTitle("URL抓取")
        #添加图标
        self.setWindowIcon(QIcon('1.ico'))

    #槽函数
    def getstr(self):
        url = self.lineEdit.text()
        rep = requests.get(url)
        rep.encoding = 'utf-8'
        html = rep.text
        #将抓取的网页源码加入到textEdit中
        #setText()这个函数不能实现
        self.text.setPlainText(html)



if __name__ =="__main__":
    app = QApplication(sys.argv)
    demo = MyTest()
    demo.show()
    sys.exit(app.exec())
