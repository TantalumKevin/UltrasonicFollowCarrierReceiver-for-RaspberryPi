import motor,time,serial
import numpy as np
import RPi.GPIO as gpio


#流程：
#开机初始化
#循环接受数据
#PID调速
#开串口
ser = serial.Serial("/dev/ttyAMA0", 115200)
#设置GPIO编号模式:根据PCB编号
gpio.setmode(gpio.BOARD)
#清空40Pin所有使用引脚,以便后续复用
#巨坑！
gpio.cleanup([7])
gpio.cleanup([x for x in range(1,40)])

def serial_read(count=0):
    while not count:
        # 没有收到字符就重复获取等待
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        recv = ser.read(count)
        # 清空接收缓冲区
        #ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)
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
    #print("!!!!!!")
    data=[[0.0], [0.0]]
    try:
        while True:
            if serial_read() == b"s":
                data[0].append(float(serial_read()))
                data[1].append(float(serial_read()))
                #print(data)
                pf.RUN(data)
                _ = serial_read()
        gpio.cleanup([x for x in range(1,40)])
    except KeyboardInterrupt:
        if ser != None:
            ser.close()
            gpio.cleanup([x for x in range(1,40)])
