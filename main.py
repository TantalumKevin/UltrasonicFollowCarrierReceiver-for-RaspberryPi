import time,serial,motor,RPi.GPIO as gpio


#串口发送
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
    #使能端本来打算直接接到传感器MCU复位引脚上
    #但经过分析发现,为了保障稳定性，还是采用通信比较安全
    gpio.setmode(gpio.BOARD)
    #gpio.setup(sonic_en, gpio.OUT)
    #gpio.output(sonic_en, gpio.HIGH)
    while True:
        #recv = serial_read()  
        #print(recv)
        #print((recv == b"steste")-10086)
        ser.write("shelloe")
        if serial_read() == b"shelloe":
            break

    while True:
        #recv = serial_read()  
        #print(recv)
        #print((recv == b"steste")-10086)
        if serial_read() == b"steste":
            break

#全流程：
#开机初始化
#循环接受数据
#PID调速

#开串口
ser = serial.Serial("/dev/ttyAMA0", 115200)
#设置GPIO编号模式:根据PCB编号
gpio.setmode(gpio.BOARD)

#清空40Pin所有使用引脚,以便后续复用
#巨坑！
#实际使用后发现,该方法还是不行,cleanup函数还是没有权限清空之前程序调用的gpio模式，这意味着……若要清空似乎还是要麻烦一些的
#但是考虑到实际使用中，不存在GPIO复用的情况这个问题也就不存在了
#但是也是确实存在之前测试时复用GPIO产生的无法通信问题
#gpio.cleanup([7])
#gpio.cleanup([x for x in range(1,40)])


if __name__ == '__main__':
    
    while True:
        init_motor()
        try:
            #尝试建立平台类
            pf = motor.Platform([[11,13,15,0.92],[22,16,18,1]])
            pf.test()
        except :
            ser.write(b"s1e")
        else :
            ser.write(b"s0e")
            break
    #print("!!!!!!")
    data=[[0.0],[0.0], [0.0]]
    error_times = 0
    stop_flag = False
    while True:
        try:
            temp=[]
            for index in range(3):
                if serial_read() == b"s":
                    temp.append(float(serial_read()))
                    #print(data[index])
                    _ = serial_read()
            
            pf.RUN(data)
            error_times = error_times-1 if error_times else error_times
        except KeyboardInterrupt:
            if ser != None:
                ser.close()
                gpio.cleanup([x for x in range(1,40)])
        except ValueError :
            #出现这个报错应该是因为数据传输出问题了
            #可能需要检查接线
            #可以的话可以再加入一个报错灯
            error_times += 1
            if not error_times:
                stop_flag = False
            if error_times >=100 or stop_flag:
                pf.stop()
                stop_flag = True
            pass
