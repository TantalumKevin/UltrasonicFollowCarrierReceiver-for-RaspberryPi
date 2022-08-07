import motor,time,serial
import numpy as np
import RPi.GPIO as gpio


#流程：
#开机初始化
#循环接受数据
#PID调速
ser = serial.Serial("/dev/ttyAMA0", 115200)

def serial_read():
    # 获得接收缓冲区字符
    count = ser.inWaiting()
    
    return ser.read(count) if count!=0 else 0
#初始化函数
def init_sonic(sonic_en=3):
    #因为开机启动有延迟，所以在执行到这里的第一时间就要把开机的信息告诉传感器
    #本来是打算做一个串口通信的
    #后来一想直接做一个使能端即可（具体逻辑还要抓抓波形看看）
    #gpio.setmode(gpio.BOARD)
    #gpio.setup(sonic_en, gpio.OUT)
    #gpio.output(sonic_en, gpio.HIGH)

    while True:
        recv = serial_read()
        # 清空接收缓冲区
        ser.flushInput()
        if recv != 0 :
            print(recv)
        # 必要的软件延时
        time.sleep(0.1)
    '''
    ser = serial.Serial("/dev/ttyAMA0", 115200)
    count = ser.inWaiting()
    
    for i in range(1000):
        recv = ser.read(count)
        print(recv) 
        '''
    return 0 

if __name__ == '__main__':
    try:
        init_sonic()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
