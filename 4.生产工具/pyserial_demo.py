import sys
import time
import serial.tools.list_ports
from PyQt5.QtWidgets import QWidget, QDesktopWidget
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.Qt import QTimer
from PyQt5.QtGui import QIcon
from ui_demo_1 import Ui_Form
# import PyQt5.sip
# from PyQt5 import QtCore
# from PyQt5.QtCore import *
# import win32ctypes.pywin32.win32api
# from PyQt5.QtWidgets import QApplication, QWidget

class Pyqt5_Serial(QWidget, Ui_Form):
    def __init__(self, *args, **kwargs):
        super(Pyqt5_Serial, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.ctrl_init()
        self.show_init()
        self.ser_init()
        self.centre()

    def ser_init(self):
        self.ser = serial.Serial()
        self.port_check()

    def ctrl_init(self):
        # 串口检测按钮
        self.s1__box_1.clicked.connect(self.port_check)
        # 串口信息显示
        self.s1__box_2.currentTextChanged.connect(self.port_imf)
        # 打开串口按钮
        self.open_button.clicked.connect(self.port_open)
        # 关闭串口按钮
        self.close_button.clicked.connect(self.port_close)
        # 发送数据按钮
        self.s3__send_button.clicked.connect(self.data_send)
        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)
        self.timer_send_cb.stateChanged.connect(self.data_send_timer)
        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)
        # 定时器检查串口
        self.chktimer = QTimer(self)
        self.chktimer.timeout.connect(self.port_check)
        #self.chktimer.start(5000)

        # 清除发送窗口
        self.s3__clear_button.clicked.connect(self.send_data_clear)
        # 清除接收窗口
        self.s2__clear_button.clicked.connect(self.receive_data_clear)
        # 保存文件
        self.s2__save_button_2.clicked.connect(self.save_data_file)
        # 定时打印
        self.pushButton_9.clicked.connect(self.timer_print)
        # 加速度设置
        self.pushButton_6.clicked.connect(self.kinco_set_accle)
        # 减速度设置
        self.pushButton_7.clicked.connect(self.kinco_set_decel)
        # 超声波id设置
        self.pushButton_5.clicked.connect(self.ks103_set_id)

        # 复位
        self.s4__send_5.clicked.connect(lambda : self.send_cmd("reset"))
        # 恢复出厂信息
        self.s4__send_3.clicked.connect(lambda : self.send_cmd("restore"))
        # 版本信息
        self.s4__send_7.clicked.connect(lambda : self.send_cmd("version"))
        # 系统信息
        self.s4__send_8.clicked.connect(lambda : self.send_cmd("sys-msg"))
        # 底盘信息
        self.s4__send_4.clicked.connect(lambda : self.send_cmd("kinco-msg"))
        # BMS信息
        self.s4__send_6.clicked.connect(lambda : self.send_cmd("bms-msg"))
        # 传感器信息
        self.s4__send_11.clicked.connect(lambda : self.send_cmd("sen-msg"))
        # 手掌信息
        self.s4__send_10.clicked.connect(lambda : self.send_cmd("plam-msg"))
        # 舵机ID设置使能
        self.s4__send_2.clicked.connect(lambda: self.send_cmd('ctldbg:1'))
        # 舵机ID设置
        self.s4__send_1.clicked.connect(self.servo_set_id)
        # 循环运动开
        self.pushButton_4.clicked.connect(lambda: self.send_cmd('ctlsrvo:1'))
        # 循环运动关
        self.pushButton_8.clicked.connect(lambda: self.send_cmd('ctlsrvo:0'))
        # 全部松轴
        self.pushButton.clicked.connect(lambda: self.send_cmd('srvo-torque:0'))
        # 全部锁轴
        self.pushButton_3.clicked.connect(lambda: self.send_cmd('srvo-torque:1'))
        # 舵机归中
        self.pushButton_2.clicked.connect(lambda: self.send_cmd('ctldef'))
        # 底盘锁轴
        self.pushButton_17.clicked.connect(lambda: self.send_cmd('set-kinco:lock:15'))
        # 底盘松轴
        self.pushButton_16.clicked.connect(lambda: self.send_cmd('set-kinco:lock:06'))
        # 打印超声波数据
        self.pushButton_20.clicked.connect(lambda: self.send_cmd('ks103-dbg:1'))

    def show_init(self):
        # 窗口初始化设置
        self.setWindowTitle("YYD测试工具V1.0(试用版)")
        #self.setWindowFlags(QtCore.Qt.CustomizeWindowHint) #隐藏标题栏
        #self.setWindowOpacity(0.96)
        #self.setMinimumHeight(720)
        #self.move(500, 200)
        #self.setFixedSize(900, 800)
        # self.showMaximized()
        # print(self.pos())
        self.adjustSize()
        #print(self.sizePolicy())

        # 按键状态
        self.close_button.setEnabled(False)
        self.open_button.setStyleSheet("background-color : cyan")
        #self.formGroupBox.setStyleSheet("background-color : yellow")
        # self.label_3.setStyleSheet("background-color : yellow")

        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.lineEdit.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.lineEdit_2.setText(str(self.data_num_sended))
        self.serail_open_flag = False   #串口打开标志

    def centre(self):
        screen = QDesktopWidget().screenGeometry()
        print(screen.x(),screen.y(), screen.width(), screen.height())
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # 发送串口指令
    def send_cmd(self, str_cmd):
        if self.serail_open_flag == True:
            sendOrder = str(str_cmd + '$\r\n').encode('ascii')
            self.ser.write(sendOrder)
            print(sendOrder, type(sendOrder))

    # 设置舵机ID
    def servo_set_id(self):
        servoId = self.s1__box_7.currentText()
        sendOrder = "setid:%s"%(servoId)
        self.send_cmd(sendOrder)

    # 发送定时打印
    def timer_print(self):
        servoId = self.s1__box_9.currentText()
        sendOrder = "setprint:1," + servoId
        self.send_cmd(sendOrder)

    # 加速度设置
    def kinco_set_accle(self):
        input_s = "set-kinco:accel:" + self.LE_7.text()
        if input_s != "":
            self.send_cmd(input_s)

    # 减速度设置
    def kinco_set_decel(self):
        input_s = "set-kinco:decel:" + self.LE_8.text()
        if input_s != "":
            self.send_cmd(input_s)

    # 超声波ID设置
    def ks103_set_id(self):
        OldId = self.s1__box_8.currentText()
        NewId = self.s1__box_10.currentText()
        sendOrder = "setid:" + OldId + ',' + NewId
        self.send_cmd(sendOrder)

    def save_data_file(self):
        if self.s2__receive_text.toPlainText() != '':
            localtime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + '.txt'
            print(localtime,type(localtime))
            fp = open(localtime, 'a+', encoding='utf-8')
            fp.write(self.s2__receive_text.toPlainText())
            fp.close()
            QMessageBox.about(None, '提示', '保存成功！')

    # 串口检测
    def port_check(self):
        if self.serail_open_flag != True:
            # 检测所有存在的串口，将信息存储在字典中
            self.Com_Dict = {}
            port_list = list(serial.tools.list_ports.comports())
            self.s1__box_2.clear()
            for port in port_list:
                self.Com_Dict["%s" % port[0]] = "%s" % port[1]
                self.s1__box_2.addItem(port[0])
            if len(self.Com_Dict) == 0:
                self.state_label.setText(" 无串口")

    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.s1__box_2.currentText()
        if imf_s != "":
            self.state_label.setText(self.Com_Dict[self.s1__box_2.currentText()])

    # 打开串口
    def port_open(self):
        self.serail_open_flag = True
        self.ser.port = self.s1__box_2.currentText()
        self.ser.baudrate = int(self.s1__box_3.currentText())
        self.ser.bytesize = int(self.s1__box_4.currentText())
        self.ser.stopbits = int(self.s1__box_6.currentText())
        self.ser.parity = self.s1__box_5.currentText()
        try:
            self.ser.open()
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None
        # 打开串口接收定时器，周期为10ms
        self.timer.start(20)

        if self.ser.isOpen():
            self.open_button.setEnabled(False)
            self.close_button.setEnabled(True)
            self.formGroupBox1.setTitle("串口状态（已开启）")

    # 关闭串口
    def port_close(self):
        self.serail_open_flag = False
        self.timer.stop()
        self.timer_send.stop()
        try:
            self.ser.close()
        except:
            pass
        self.open_button.setEnabled(True)
        self.close_button.setEnabled(False)
        self.lineEdit_3.setEnabled(True)
        # 接收数据和发送数据数目置零
        self.data_num_received = 0
        self.lineEdit.setText(str(self.data_num_received))
        self.data_num_sended = 0
        self.lineEdit_2.setText(str(self.data_num_sended))
        self.formGroupBox1.setTitle("串口状态（已关闭）")

    # 发送数据
    def data_send(self):
        if self.serail_open_flag == True:
            input_s = self.s3__send_text.toPlainText()
            if input_s != "":
                # 非空字符串
                if self.hex_send.isChecked():
                    # hex发送
                    input_s = input_s.strip()
                    send_list = []
                    while input_s != '':
                        try:
                            num = int(input_s[0:2], 16)
                        except ValueError:
                            QMessageBox.critical(self, 'wrong data', '请输入十六进制数据，以空格分开!')
                            return None
                        input_s = input_s[2:].strip()
                        send_list.append(num)
                    input_s = bytes(send_list)
                else:
                    # ascii发送
                    input_s = (input_s + '\r\n').encode('utf-8')
                #print(type(input_s))
                num = self.ser.write(input_s)
                self.data_num_sended += num
                self.lineEdit_2.setText(str(self.data_num_sended))
        else:
            pass

    # 接收数据
    def data_receive(self):
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num > 0:
            data = self.ser.read(num)
            num = len(data)
            # hex显示
            if self.hex_receive.checkState():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                print(type(out_s))
                self.s2__receive_text.insertPlainText(out_s)
            else:
                print(type(data))
                try:
                    tempStr = data.decode('GB2312')
                    self.s2__receive_text.insertPlainText(str(tempStr))
                except:
                    print('decode err')
                    return None
                # 串口接收到的字符串为b'123',要转化成unicode字符串才能输出到窗口中去
                #self.s2__receive_text.insertPlainText(data.decode('iso-8859-1'))
                # self.s2__receive_text.insertPlainText(data.decode('gbk'))
            # 统计接收字符的数量
            self.data_num_received += num
            self.lineEdit.setText(str(self.data_num_received))

            # 获取到text光标
            textCursor = self.s2__receive_text.textCursor()
            # 滚动到底部
            textCursor.movePosition(textCursor.End)
            # 设置光标到text中去
            self.s2__receive_text.setTextCursor(textCursor)
        else:
            pass

    # 定时发送数据
    def data_send_timer(self):
        if self.timer_send_cb.isChecked():
            self.timer_send.start(int(self.lineEdit_3.text()))
            self.lineEdit_3.setEnabled(False)
        else:
            self.timer_send.stop()
            self.lineEdit_3.setEnabled(True)

    # 清除显示
    def send_data_clear(self):
        self.s3__send_text.setText("")

    # 接收清除
    def receive_data_clear(self):
        self.s2__receive_text.setText("")
        self.lineEdit.setText("0")
        self.lineEdit_2.setText("0")
        self.data_num_received = 0
        self.data_num_sended = 0

    # #鼠标按下事件
    # def mousePressEvent(self, evt):
    #     if evt.button() == Qt.LeftButton:
    #         self.move_flag = True
    #         self.mouse_x = evt.globalX()
    #         self.mouse_y = evt.globalY()
    #         #print(self.mouse_x, self.mouse_y)
    #         self.start_x = self.x()
    #         self.start_y = self.y()
    #
    # def mouseMoveEvent(self, evt):
    #     if self.move_flag == True:
    #         move_x = evt.globalX() - self.mouse_x
    #         move_y = evt.globalY() - self.mouse_y
    #         dest_x = self.start_x + move_x
    #         dest_y = self.start_y + move_y
    #         #print(evt.globalX(), evt.globalY())
    #         #print(evt.screenPos())
    #         self.move(dest_x, dest_y)
    #
    # def mouseReleaseEvent(self, QMouseEvent):
    #     self.move_flag = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    #QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    myshow = Pyqt5_Serial()
    icon = QIcon("YYD.png")
    myshow.setWindowIcon(icon)
    myshow.show()
    sys.exit(app.exec_())
