import serial
from visual import *

data = serial.Serial('COM4',9600)

obj = cylinder(length = 6,radius =0.6,color = color.red,pos = (-3,0,0))

while(True):
    if(data.isWaiting()!=0):
        k = data.readline()
        y = float(k)
        obj.length = y
        print(y)