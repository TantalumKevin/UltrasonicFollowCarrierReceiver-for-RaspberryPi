import motor,time,serial
import numpy as np
import RPi.GPIO as gpio


#流程：
#开机初始化
#循环接受数据
#PID调速
ser = serial.Serial("/dev/ttyAMA0", 115200)

def serial_read(count=0):
    while not count:
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        recv = ser.read(count)
        # 清空接收缓冲区
        ser.flushInput()
    #print(recv)
    return recv

#电机初始化
def init_motor(sonic_en=7):
    '''测试串口
    try:
        while True:
            recv = serial_read()        
            if recv == "steste":
                break
            # 必要的软件延时
            time.sleep(0.1)
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
    '''
    #因为开机启动有延迟，所以在执行到这里的第一时间就要把开机的信息告诉传感器
    #本来是打算做一个串口通信的
    #后来一想直接做一个使能端即可（具体逻辑还要抓抓波形看看）
    gpio.setmode(gpio.BOARD)
    gpio.setup(sonic_en, gpio.OUT)
    gpio.output(sonic_en, gpio.HIGH)
    while True:
        recv = serial_read()  
        #print(recv)
        #print((recv == b"steste")-10086)
        if recv == b"steste":
            break
        # 必要的软件延时
        time.sleep(0.1)


if __name__ == '__main__':
    while True:
        init_motor()
        try:
            pf = motor.Platform([[11,13,15],[22,16,18]])
        except :
            ser.write(b"s1e")
        else :
            ser.write(b"s0e")
            break
    print("!!!!!!")
    data=[[0.0], [0.0]]
    try:
        while True:
            recv = serial_read()
            print(recv)
            if recv == b"s":
                recv = float(serial_read())
                print(recv)
                data[0].append(recv)
                time.sleep(0.1)
                recv = float(serial_read())
                print(recv)
                data[1].append(recv)
                print(data)
                pf.RUN(data)
                _ = serial_read()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
