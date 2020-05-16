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
        #禁用最大化按钮
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
 
        #显示区
        self.resultflag = 0
        self.errflag = 0
        
        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMaxLength(30)        
        
        #操作区
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.display)
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
 
        self.show()
 
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox('')
        layout = QGridLayout()
 
        #操作区第1行
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
 
        #操作区第2行
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
 
        #操作区第3行
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
 
        #操作区第4行
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
 
        #操作区第5行,其中'0'独占1行2列
        button40 = QPushButton('0')
        button40.clicked.connect(self.on_click)
        layout.addWidget(button40, 4, 0, 1, 2)  #从4行0列开始占1行2列
 
        button42 = QPushButton('.')
        button42.clicked.connect(self.on_click)
        layout.addWidget(button42, 4, 2, 1, 1)  #从4行2列开始占1行1列
 
        button43 = QPushButton('=')
        button43.clicked.connect(self.on_click)
        layout.addWidget(button43, 4, 3, 1, 1)  #从4行3列开始占1行1列
 
        self.horizontalGroupBox.setLayout(layout)
        
    def on_click(self):
        source = self.sender()
        
        #全部输入清零
        if source.text() == 'Clear All':
            self.display.setText('0')
 
 
        #删除最近输入的一个操作数
        elif source.text() == 'Clear':
            if self.resultflag != 1:           
                clrreg = re.compile(r'[0-9.]+$')
                substr = clrreg.sub('', self.display.text())
                if substr == '':
                    substr = '0'
                self.display.setText(substr)
 
 
        #退格键功能    
        elif source.text() == 'Backspace':
            if self.resultflag != 1:           
                if len(self.display.text()) <= 1:
                    newtext = '0'
                else:
                    newtext = self.display.text()[0 : (len(self.display.text()) - 1)]
                
                self.display.setText(newtext)
 
 
        #计算输入的算术表达式并将结果显示
        elif source.text() == '=':
            if self.resultflag != 1:           
                try:
                    disstr = self.display.text()[:]
                    #考虑表达式不完整的情况处理：尾部为运算符*/则补1
                    if disstr[len(disstr) - 1 : ] in '*/':
                        calstr = disstr + '1'
                    #尾部为运算符+-或小数点则补0
                    elif disstr[len(disstr) - 1 : ] in '+-.':
                        calstr = disstr + '0'
                    else:
                        calstr = disstr[:]
                    result = str(eval(calstr))
                    
                #考虑除0异常处理
                except (ZeroDivisionError, Exception) as errinfo:
                    result = 'Error: '+ str(errinfo)
                    self.errflag = 1
                
                self.display.setText(result)
                self.resultflag = 1
            
 
        #输入数字或小数点：将算术表达式输入同步显示出来
        else:
            self.numhandle() 
    
    def numhandle(self):
        rawstr = self.display.text()[:]
        strlen = len(rawstr)
        lastchar = rawstr[strlen-1 : ]
        inchar = self.sender().text()[:]
        newstr = ''
        
        #前面输入尚未计算结果
        if self.resultflag != 1:
            #当前最后一个字符为运算符（+-*/）
            if lastchar in '+-*/':
                #输入为0-9 -> 直接追加
                if inchar in '0123456789':
                    newstr = rawstr + inchar
                #输入为运算符 -> 忽略输入
                elif inchar in '+-*/':
                    newstr = rawstr[:]
                #输入为小数点 -> 小数点前补0再追加
                else:
                    newstr = rawstr + '0' + inchar
            
            #当前最后一个字符为小数点
            elif lastchar == '.':
                #输入为0-9 -> 直接追加
                if inchar in '0123456789':
                    newstr = rawstr + inchar
                #输入为小数点 -> 忽略输入
                elif inchar == '.':
                    newstr = rawstr[:]
                #输入为运算符 -> 运算符前补0再追加
                else:
                    newstr = rawstr + '0' + inchar
            
            #当前最后一个字符为0-9
            else:
                numreg1 = re.compile(r'[+\-*/]{0,1}[0-9]+\.[0-9]*[0-9]$')
                srchrslt1 = numreg1.search(rawstr)
                #当前最后一个数字前面已经有小数点
                if srchrslt1 != None: 
                    #输入为小数点 -> 忽略输入
                    if inchar == '.':
                        newstr = rawstr[:]
                    #输入为0-9或运算符 -> 直接追加
                    else:
                        newstr = rawstr + inchar
                
                #当前最后一个数字前面没有小数点
                else:
                    numreg2 = re.compile(r'[+\-*/]0$')
                    srchrslt2 = numreg2.search(rawstr)
                    #当前最后一个字符为0且作为最近运算符后的第一个数字
                    if srchrslt2 != None:
                        #输入为小数点或运算符 -> 直接追加
                        if inchar == '.' or inchar in '+-*/':
                            newstr = rawstr + inchar
                        #输入为0-9 -> 忽略输入
                        else:
                            newstr = rawstr[:]
                    #当前字符串即是'0'
                    elif rawstr == '0':
                        #输入为0-9 -> 用输入取代原字符'0'
                        if inchar in '0123456789':
                            newstr = inchar[:]
                        #输入为小数点或运算符 -> 直接追加
                        else:
                            newstr = rawstr + inchar
                    #其他情况均可直接追加
                    else:
                        newstr = rawstr + inchar
 
 
        #前面输入已经计算出结果
        else:
            #考虑计算有无异常
            if self.errflag == 0:
                #输入为运算符 -> 直接追加
                if inchar in '+-*/':
                    newstr = rawstr + inchar
                #输入小数点 -> 以小数点前补0刷新显示
                elif inchar == '.':
                    newstr = '0' + inchar
                #输入0-9 -> 以输入刷新显示
                else:
                    newstr = inchar[:]
            else:
                #输入为运算符 -> 忽略输入并擦除err信息
                if inchar in '+-*/':
                    newstr = '0'
                #输入小数点 -> 以小数点前补0刷新显示
                elif inchar == '.':
                    newstr = '0' + inchar
                #输入0-9 -> 以输入刷新显示
                else:
                    newstr = inchar[:]
                self.errflag = 0
                
            self.resultflag = 0
 
        self.display.setText(newstr)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calculater()
    sys.exit(app.exec_())
