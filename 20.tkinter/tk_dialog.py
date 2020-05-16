#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tkinter as tk
import tkinter.filedialog


def encrypt():
    key=int(Key.get(), 16)
    data = open(File.get(), 'rb').read()

def getFile():
    file = tkinter.filedialog.askopenfilename(initialdir='C:\\')
    if file:
        File.set(file)


win = tk.Tk()

Key = tk.StringVar(win, '0x1234ABCD')
File = tk.StringVar(win, r'C:\Users\wmx\Desktop\SWM181_StdPeriph_Driver.bin')

tk.Label(win, text=u'加密秘钥：').grid(row=0, column=0)
tk.Entry(win, width=15, textvariable=Key).grid(row=0, column=1, sticky="W")

tk.Label(win, text=u'加密文件：').grid(row=1, column=0)
tk.Entry(win, width=59, textvariable=File).grid(row=1, column=1)
tk.Button(win, text='...', width=4, command=lambda: getFile()).grid(row=1, column=2)

tk.Button(win, text=u'加密', width=4, command=lambda: encrypt()).grid(row=2, column=2)

win.mainloop()