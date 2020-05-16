# -*- coding: utf-8 -*-
 
'''
Description: A simple calculater based on PyQt5
Author: waterfronter
Last Edit: 2017.10.15
'''
 
import sys
import re
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QGroupBox, QLineEdit
from PyQt5.QtCore import Qt
 
class Calculater(QWidget):
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('Calculater')
        self.setGeometry(100, 100, 350, 150)
        #������󻯰�ť
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
 
        #��ʾ��
        self.resultflag = 0
        self.errflag = 0
        
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(30)        
        
        #������
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.display)
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox('')
        layout = QGridLayout()
 
        #��������1��
        button00 = QPushButton('Backspace')
        button00.clicked.connect(self.on_click)
        layout.addWidget(button00, 0, 0)
 
        button01 = QPushButton('Clear')
        button01.clicked.connect(self.on_click)
        layout.addWidget(button01, 0, 1)
 
        button02 = QPushButton('Clear All')
        button02.clicked.connect(self.on_click)
        layout.addWidget(button02, 0, 2)
 
        button03 = QPushButton('/')
        button03.clicked.connect(self.on_click)
        layout.addWidget(button03, 0, 3)
 
        #��������2��
        button10 = QPushButton('7')
        button10.clicked.connect(self.on_click)
        layout.addWidget(button10, 1, 0)
 
        button11 = QPushButton('8')
        button11.clicked.connect(self.on_click)
        layout.addWidget(button11, 1, 1)
 
        button12 = QPushButton('9')
        button12.clicked.connect(self.on_click)
        layout.addWidget(button12, 1, 2)
 
        button13 = QPushButton('*')
        button13.clicked.connect(self.on_click)
        layout.addWidget(button13, 1, 3)
 
        #��������3��
        button20 = QPushButton('4')
        button20.clicked.connect(self.on_click)
        layout.addWidget(button20, 2, 0)
 
        button21 = QPushButton('5')
        button21.clicked.connect(self.on_click)
        layout.addWidget(button21, 2, 1)
 
        button22 = QPushButton('6')
        button22.clicked.connect(self.on_click)
        layout.addWidget(button22, 2, 2)
 
        button23 = QPushButton('-')
        button23.clicked.connect(self.on_click)
        layout.addWidget(button23, 2, 3)
 
        #��������4��
        button30 = QPushButton('1')
        button30.clicked.connect(self.on_click)
        layout.addWidget(button30, 3, 0)
 
        button31 = QPushButton('2')
        button31.clicked.connect(self.on_click)
        layout.addWidget(button31, 3, 1)
 
        button32 = QPushButton('3')
        button32.clicked.connect(self.on_click)
        layout.addWidget(button32, 3, 2)
 
        button33 = QPushButton('+')
        button33.clicked.connect(self.on_click)
        layout.addWidget(button33, 3, 3)
 
        #��������5��,����'0'��ռ1��2��
        button40 = QPushButton('0')
        button40.clicked.connect(self.on_click)
        layout.addWidget(button40, 4, 0, 1, 2)  #��4��0�п�ʼռ1��2��
 
        button42 = QPushButton('.')
        button42.clicked.connect(self.on_click)
        layout.addWidget(button42, 4, 2, 1, 1)  #��4��2�п�ʼռ1��1��
 
        button43 = QPushButton('=')
        button43.clicked.connect(self.on_click)
        layout.addWidget(button43, 4, 3, 1, 1)  #��4��3�п�ʼռ1��1��
 
        self.horizontalGroupBox.setLayout(layout)
        
    def on_click(self):
        source = self.sender()
        
        #ȫ����������
        if source.text() == 'Clear All':
            self.display.setText('0')
 
 
        #ɾ����������һ��������
        elif source.text() == 'Clear':
            if self.resultflag != 1:           
                clrreg = re.compile(r'[0-9.]+$')
                substr = clrreg.sub('', self.display.text())
                if substr == '':
                    substr = '0'
                self.display.setText(substr)
 
 
        #�˸������    
        elif source.text() == 'Backspace':
            if self.resultflag != 1:           
                if len(self.display.text()) <= 1:
                    newtext = '0'
                else:
                    newtext = self.display.text()[0 : (len(self.display.text()) - 1)]
                
                self.display.setText(newtext)
 
 
        #����������������ʽ���������ʾ
        elif source.text() == '=':
            if self.resultflag != 1:           
                try:
                    disstr = self.display.text()[:]
                    #���Ǳ��ʽ���������������β��Ϊ�����*/��1
                    if disstr[len(disstr) - 1 : ] in '*/':
                        calstr = disstr + '1'
                    #β��Ϊ�����+-��С������0
                    elif disstr[len(disstr) - 1 : ] in '+-.':
                        calstr = disstr + '0'
                    else:
                        calstr = disstr[:]
                    result = str(eval(calstr))
                    
                #���ǳ�0�쳣����
                except (ZeroDivisionError, Exception) as errinfo:
                    result = 'Error: '+ str(errinfo)
                    self.errflag = 1
                
                self.display.setText(result)
                self.resultflag = 1
            
 
        #�������ֻ�С���㣺���������ʽ����ͬ����ʾ����
        else:
            self.numhandle() 
    
    def numhandle(self):
        rawstr = self.display.text()[:]
        strlen = len(rawstr)
        lastchar = rawstr[strlen-1 : ]
        inchar = self.sender().text()[:]
        newstr = ''
        
        #ǰ��������δ������
        if self.resultflag != 1:
            #��ǰ���һ���ַ�Ϊ�������+-*/��
            if lastchar in '+-*/':
                #����Ϊ0-9 -> ֱ��׷��
                if inchar in '0123456789':
                    newstr = rawstr + inchar
                #����Ϊ����� -> ��������
                elif inchar in '+-*/':
                    newstr = rawstr[:]
                #����ΪС���� -> С����ǰ��0��׷��
                else:
                    newstr = rawstr + '0' + inchar
            
            #��ǰ���һ���ַ�ΪС����
            elif lastchar == '.':
                #����Ϊ0-9 -> ֱ��׷��
                if inchar in '0123456789':
                    newstr = rawstr + inchar
                #����ΪС���� -> ��������
                elif inchar == '.':
                    newstr = rawstr[:]
                #����Ϊ����� -> �����ǰ��0��׷��
                else:
                    newstr = rawstr + '0' + inchar
            
            #��ǰ���һ���ַ�Ϊ0-9
            else:
                numreg1 = re.compile(r'[+\-*/]{0,1}[0-9]+\.[0-9]*[0-9]$')
                srchrslt1 = numreg1.search(rawstr)
                #��ǰ���һ������ǰ���Ѿ���С����
                if srchrslt1 != None: 
                    #����ΪС���� -> ��������
                    if inchar == '.':
                        newstr = rawstr[:]
                    #����Ϊ0-9������� -> ֱ��׷��
                    else:
                        newstr = rawstr + inchar
                
                #��ǰ���һ������ǰ��û��С����
                else:
                    numreg2 = re.compile(r'[+\-*/]0$')
                    srchrslt2 = numreg2.search(rawstr)
                    #��ǰ���һ���ַ�Ϊ0����Ϊ����������ĵ�һ������
                    if srchrslt2 != None:
                        #����ΪС���������� -> ֱ��׷��
                        if inchar == '.' or inchar in '+-*/':
                            newstr = rawstr + inchar
                        #����Ϊ0-9 -> ��������
                        else:
                            newstr = rawstr[:]
                    #��ǰ�ַ�������'0'
                    elif rawstr == '0':
                        #����Ϊ0-9 -> ������ȡ��ԭ�ַ�'0'
                        if inchar in '0123456789':
                            newstr = inchar[:]
                        #����ΪС���������� -> ֱ��׷��
                        else:
                            newstr = rawstr + inchar
                    #�����������ֱ��׷��
                    else:
                        newstr = rawstr + inchar
 
 
        #ǰ�������Ѿ���������
        else:
            #���Ǽ��������쳣
            if self.errflag == 0:
                #����Ϊ����� -> ֱ��׷��
                if inchar in '+-*/':
                    newstr = rawstr + inchar
                #����С���� -> ��С����ǰ��0ˢ����ʾ
                elif inchar == '.':
                    newstr = '0' + inchar
                #����0-9 -> ������ˢ����ʾ
                else:
                    newstr = inchar[:]
            else:
                #����Ϊ����� -> �������벢����err��Ϣ
                if inchar in '+-*/':
                    newstr = '0'
                #����С���� -> ��С����ǰ��0ˢ����ʾ
                elif inchar == '.':
                    newstr = '0' + inchar
                #����0-9 -> ������ˢ����ʾ
                else:
                    newstr = inchar[:]
                self.errflag = 0
                
            self.resultflag = 0
 
        self.display.setText(newstr)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculater()
    sys.exit(app.exec_())
