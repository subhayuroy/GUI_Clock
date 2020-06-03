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

