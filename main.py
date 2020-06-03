import sys, types, os
from time import localtime
from datetime import timedelta, datetime
from math import sin, cos, pi
from threading import Thread

try:
    from tkinter import *
except ImportError:
    try:
        from mtTkinter import *
    except ImportError:
        from tkinter import *

hasPIL = True

try:
    from PIL import Image, ImageTk
except ImportError:
    hasPIL = False

class mapper:
    def __init__(self, world, viewpoint):
        self.world = world
        self.viewpoint = viewpoint
        x_min, y_min, x_max, y_max = self.world
        X_min, Y_min, X_max, Y_max = self.viewpoint
        f_x = float(X_max - X_min) / float(x_max - x_min)
        f_y = float(Y_max - Y_min) / float(y_max - y_min)
        self.f = min(f_x, f_y)
        x_c = 0.5 * (x_min + x_max)
        y_c = 0.5 * (y_min + y_max)
        X_c = 0.5 * (X_min + X_max)
        Y_c = 0.5 * (Y_min + Y_max)
        self.c_1 = X_c - self.f * x_c
        self.c_2 = Y_c - self.f * y_c
    def __windowToViewport(self, x, y):
        X = self.f * x + self.c_1
        Y = self.f * -y + self.c_2
        return X, Y
    def windowToViewport(self, x1, y1, x2, y2):
        return self.__windowToViewport(x1, y1), self.__windowToViewport(x2, y2)

class makeThread(Thread):
    def __init__(self, func):
        Thread.__init__(self)
        self.__action = func
        self.debug = False
    def __del__(self):
        if (self.debug): print("Thread end")
    def run(self):
        if (self.debug): print("Thread begin")
        self.__action()

class clock:
    def __init__(self, root, deltahours = 0, sImage = True, w=400, h=400, useThread = False):
        self.world = [-1,-1, 1, 1]
        self.imgPath = './home/subhayu_roy/PycharmProjects/GUI Clock/images/867-XL-Greyish-Blue.jpg'
        if hasPIL and os.path.exists(self.imgPath):
            self.showImage = sImage
        else:
            self.showImage = False

        self.setColors()
        self.circlesize = 0.09
        self._ALL = 'handles'
        self.root = root
        width, height = w, h
        self.pad = width/16

        if self.showImage:
            self.fluImg = Image.open(self.imgPath)

        self.root.bind("<Escape>", lambda _: root.destroy())
        self.delta = timedelta(hours=deltahours)
        self.canvas = Canvas(root, width=width, height=height, background=self.bgcolor)
        viewport = (self.pad, self.pad, width - self.pad, height - self.pad)
        self.T = mapper(self.world, viewport)
        self.root.title('Clock')
        self.canvas.bind("<Configure>", self.resize)
        self.root.bind("<KeyPress-i>", self.toggleImage)
        self.canvas.pack(fill=BOTH, expand=YES)

        if useThread:
            st = makeThread(self.poll)
            st.debug = True
            st.start()
        else:
            self.poll()
    def resize(self, event):
        sc = self.canvas
        sc.delete(ALL)
        width = sc.winfo_width()
        height = sc.winfo_height()

        imgSize = min(width, height)
        self.pad = imgSize/16
        viewport = (self.pad, self.pad, width - self.pad, height - self.pad)
        self.T = mapper(self.world, viewport)

        if self.showImage:
            flu = self.fluImg.resize(int(0.8*0.8*imgSize), int(0.8*imgSize), Image.ANTIALIAS)
            self.flu = ImageTk.PhotoImage(flu)
            sc.create_image(width/2, height/2, image=self.flu)
        else:
            self.canvas.create_rectangle([[0,0], [width, height]], fill=self.bgcolor)

        self.redraw()
    def setColors(self):
        if self.showImage:
            self.bgcolor = 'antique white'
            self.timecolor = 'dark orange'
            self.circlecolor = 'dark green'
        else:
            self.bgcolor = '#000000'
            self.timecolor = '#ffffff'
            self.circlecolor = '#808080'
    def toggleImage(self, event):
        if hasPIL and os.path.exists(self.imgPath):
            self.showImage = not self.showImage
            self.setColors()
            self.resize(event)
    def redraw(self):
        start = pi/2
        step = pi/6
        for i in range(12):
            angle = start - i*step
            x, y = cos(angle), sin(angle)
            self.paintcircle(x, y)
        self.painthms()
        if not self.showImage:
            self.paintcircle(0, 0)
    def painthms(self):
        self.canvas.delete(self._ALL)
        T = datetime.timetuple(datetime.utcnow() - self.delta)
        x, x, x, h, m, s, x, x, x = T
        self.root.title('%02i:%02i:%02i' % (h, m, s))
        angle = pi/2 - pi/6 * (h+m/60.0)
        x, y = cos(angle)*0.70, sin(angle)*0.70
        scl = self.canvas.create_line
        scl(self.T.windowToViewport(0, 0, x, y), fill=self.timecolor, tag=self._ALL, width=self.pad/3)
        angle = pi/2 - pi/30*(m+s/60.0)
        x, y = cos(angle)*0.90, sin(angle)*0.90
        scl(self.T.windowToViewport(0, 0, x, y), fill=self.timecolor, tag=self._ALL, width=self.pad/5)
        angle = pi / 2 - pi / 30 * s
        x, y= cos(angle)*0.95, sin(angle)*0.95
        scl(self.T.windowToViewport(0, 0, x, y), fill=self.timecolor, tag=self._ALL, arrow='last')
    def paintcircle(self, x, y):
        ss = self.circlesize/2.0
        sco = self.canvas.create_oval
        sco(self.T.windowToViewport(-ss+x, -ss+y, ss+x, ss+y), fill=self.circlecolor)
    def poll(self):
        self.redraw()
        self.root.after(200, self.poll)
