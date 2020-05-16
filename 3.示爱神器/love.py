import datetime
import tkinter as tk
from PIL import Image, ImageTk
import time
import tkinter.font as tkFont

def Timer():
        min_ = 0
        hour = 0
        day = 0
        d1 = datetime.datetime.now() 
        d2 = datetime.datetime(2015,5,2,13,14,30)
        interval = d1 - d2
        sec = interval.days*24*3600 + interval.seconds
        if sec>=60:
            min_ = sec//60
            sec = sec%60
            if min_>=60:        
                hour = min_//60
                min_=min_%60
                if hour>=24:
                    day = hour//24                    
                    hour = hour%24
        timer = '老婆,认识你:'+str(day)+' 天 '+str(hour)+' 小时 '+str(min_)+' 分钟 '+str(sec)+' 秒'\
								+ '\n' +'未 来 的 日 子 都 听 你 的 ^_^'

        return timer

class Watch(tk.Frame):  
    msec = 1000  
    def __init__(self, parent=None, **kw):  
            tk.Frame.__init__(self, parent, kw)  
            self._running = False  
            self.timestr1 = tk.StringVar()  
            self.timestr2 = tk.StringVar()  
            self.makeWidgets()  
            self.flag  = True  
    def makeWidgets(self):
            ft = tkFont.Font(family='Fixdsys', size=30, weight=tkFont.NORMAL)
            self.bgtimg=tk.PhotoImage(file='timg.gif')
            l2 = tk.Label(self, textvariable = self.timestr2,compound='center',image=self.bgtimg,font = ft)    
            l2.pack()  
    def _update(self):  
        self._settime()  
        self.timer = self.after(self.msec, self._update)  
    def _settime(self):  
        time1 = Timer()    
        self.timestr2.set(time1)
    def start(self):  
        self._update()  
        self.pack(side = 'top')
        
if __name__ == '__main__':  
    def main():
        window = tk.Tk()
        window.title('青春那年 我们正好')
        window.geometry('800x650')
        canvas = tk.Canvas(window,height = '560',width = '800',bg = 'white')
        image = Image.open('timg_2.jpeg')  
        im = ImageTk.PhotoImage(image)
        canvas.create_image(300,50,image = im)
        canvas.pack(side = 'top')
        
        frame1 = tk.Frame(window)  
        frame1.pack(side = 'bottom')  
        mw = Watch(window)
        mw.start()
        
        window.mainloop()

    main()

