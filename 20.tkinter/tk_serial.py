# coding=gbk
'''
'''

__file__ = "XLiCOM.Py"
__author__ = "XIVN1987@163.com"

import sys
import ttk
import time
import queue
import serial
import threading
import tkinter as tk

isOpened = threading.Event()
RQueue = queue.Queue(maxsize=1024)
TQueue = queue.Queue(maxsize=1024)

root = tk.Tk()
ComX = tk.StringVar(root, 'COM1')
Baud = tk.StringVar(root, "9600")
Dbit = tk.StringVar(root, '8')
Sbit = tk.StringVar(root, '1')
Chck = tk.StringVar(root, 'None')
Enty = tk.StringVar(root, 'ABCD')
HexD = tk.BooleanVar(root, False)
HexO = tk.BooleanVar(root, False)
Open = tk.StringVar(root, u'打开串口')


def main():
    root.title("XIVN1987's COM Shell")

    txt1 = tk.Text(root, width=81, border=5)
    txt1.pack(side='top', padx=3, pady=1, anchor='c')

    cnv1 = tk.Canvas(root, height=26, width=580)
    cnv1.pack(side='top', padx=0, pady=0, anchor='c')
    cnv1.create_window(30, 15, window=ttk.Label(root, text=u'输入框：'))
    cnv1.create_window(192, 15, window=ttk.Entry(root, textvariable=Enty, width=44))
    cnv1.create_window(387, 15, window=ttk.Button(root, text=u'发送', width=12, command=lambda: TQueue.put(Enty.get())))
    cnv1.create_window(472, 15, window=ttk.Button(root, text=u'清除', width=9, command=lambda: txt1.delete('1.0', 'end')))
    cnv1.create_window(547, 15, window=ttk.Checkbutton(root, text=u'HEX显示', variable=HexD, onvalue=True, offvalue=False,
                                                       command=lambda: HEXDProc(txt1)))

    cnv2 = tk.Canvas(root, height=26, width=580)
    cnv2.pack(side='top', padx=0, pady=0, anchor='c')
    cnv2.create_window(30, 15, window=ttk.Label(root, text=u'串口号：'))
    cnv2.create_window(105, 15,
                       window=ttk.Combobox(root, textvariable=ComX, values=['COM1', 'COM2', 'COM3', 'COM4'], width=12))
    cnv2.create_window(202, 15, window=ttk.Label(root, text=u'波特率：'))
    cnv2.create_window(277, 15,
                       window=ttk.Combobox(root, textvariable=Baud, values=['4800', '9600', '19200'], width=12))
    cnv2.create_window(398, 15, window=ttk.Button(root, textvariable=Open, width=16, command=lambda: COMOpen(cnv2)))
    cnv2.create_oval(470, 7, 486, 23, fill='black', tag='led')
    cnv2.create_window(547, 15, window=ttk.Checkbutton(root, text=u'HEX发送', variable=HexO, onvalue=True, offvalue=False,
                                                       command=lambda: Enty.set(''.join('%02X' % i for i in
                                                                                        [ord(c) for c in
                                                                                         Enty.get()])) if HexO.get() else Enty.set(
                                                           ''.join([chr(int(i, 16)) for i in
                                                                    [Enty.get()[i * 2:i * 2 + 2] for i in
                                                                     range(0, len(Enty.get()) / 2)]]))))

    cnv3 = tk.Canvas(root, height=26, width=580)
    cnv3.pack(side='top', padx=0, pady=0, anchor='c')
    cnv3.create_window(30, 15, window=ttk.Label(root, text=u'数据位：'))
    cnv3.create_window(105, 15,
                       window=ttk.Combobox(root, textvariable=Dbit, values=['9', '8', '7', '6', '5'], width=12))
    cnv3.create_window(202, 15, window=ttk.Label(root, text=u'停止位：'))
    cnv3.create_window(277, 15, window=ttk.Combobox(root, textvariable=Sbit, values=['1', '2'], width=12))
    cnv3.create_window(370, 15, window=ttk.Label(root, text=u'校验位：'))
    cnv3.create_window(445, 15,
                       window=ttk.Combobox(root, textvariable=Chck, values=['None', 'Odd', 'Even', 'Mark', 'Space'],
                                           width=12))
    cnv3.create_window(547, 15, window=ttk.Button(root, text=u'扩展', width=9))

    com_thread = threading.Thread(target=COMTrce)
    com_thread.setDaemon(True)
    com_thread.start()

    root.bind("<<COMRxRdy>>", lambda e: txt1.insert("insert", ''.join(
        '%02X' % i for i in [ord(c) for c in RQueue.get()]) if HexD.get() else RQueue.get()))

    root.mainloop()


def HEXDProc(txt1):
    if HexD.get():
        s = txt1.get('1.0', 'end')
        s = ''.join('%02X' % i for i in [ord(c) for c in s])
        txt1.delete('1.0', 'end')
        txt1.insert("insert", s)
    else:
        s = txt1.get('1.0', 'end')
        s = ''.join([chr(int(i, 16)) for i in [s[i * 2:i * 2 + 2] for i in range(0, len(s) / 2)]])
        txt1.delete('1.0', 'end')
        txt1.insert("insert", s)


COM = serial.Serial()


def COMOpen(cnv2):
    if not isOpened.isSet():
        try:
            COM.timeout = 1
            COM.xonxoff = 0
            COM.port = ComX.get()
            COM.parity = Chck.get()[0]
            COM.baudrate = int(Baud.get())
            COM.bytesize = int(Dbit.get())
            COM.stopbits = int(Sbit.get())
            COM.open()
        except Exception:
            print
            "COM Open Error!"
        else:
            isOpened.set()
            Open.set(u'关闭串口')
            cnv2.itemconfig('led', fill='green')
    else:
        COM.close()
        isOpened.clear()
        Open.set(u'打开串口')
        cnv2.itemconfig('led', fill='black')


def COMTrce():
    while True:
        if isOpened.isSet():
            rbuf = COM.read(1)  # read one, with timout
            if rbuf:
                n = COM.inWaiting()
                if n:
                    rbuf = rbuf + COM.read(n)
                    RQueue.put(rbuf)
                    root.event_generate("<<COMRxRdy>>")

            if not TQueue.empty():
                COM.write(TQueue.get())


if __name__ == '__main__':
    isOpened.clear()
    main()

