import motor
import numpy as np
import RPi.GPIO as gpio
import serial
#流程：
#开机初始化
#循环接受数据
#PID调速

#初始化函数
def init_sonic(sonic_en=):
    #因为开机启动有延迟，所以在执行到这里的第一时间就要把开机的信息告诉传感器
    #本来是打算做一个串口通信的
    #后来一想直接做一个使能端即可（具体逻辑还要抓抓波形看看）
    gpio.setmode(gpio.BOARD)
    gpio.setup(sonic_en, gpio.OUT)
    gpio.output(sonic_en, gpio.HIGH)
    ser = serial.Serial("/dev/ttyAMA0", 115200)
    count = ser.inWaiting()
    recv = ser.read(count) 
    return 0 