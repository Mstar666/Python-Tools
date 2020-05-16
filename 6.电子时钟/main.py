'''
Created on 2018-08-09 22:39

@author: Freedom
'''
import sys
from PyQt5.QtWidgets import QApplication
from DigitalClock import DigitalClock

def main():

    app = QApplication(sys.argv)
    clock = DigitalClock(None) #新建电子时钟
    clock.show() #显示电子时钟
    sys.exit(app.exec_()) #进入消息循环

if __name__ == '__main__':
    main()
