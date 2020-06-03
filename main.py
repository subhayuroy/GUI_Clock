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

