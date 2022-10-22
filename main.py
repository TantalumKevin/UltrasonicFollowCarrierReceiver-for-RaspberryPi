import time,serial,motor,RPi.GPIO as gpio

class SonicError(Exception):
    def __init__(self, ):
        pass

#串口接收
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
        ser.write(b"shelloe")
        temp = serial_read()
        if temp[0:7] == b"shelloe":
            break

    while True:
        #recv = serial_read()  
        #print(recv)
        #print((recv == b"steste")-10086)
        if temp[-6:] == b"steste":
            break
        temp = serial_read()

#全流程：
#开机初始化
#循环接受数据
#PID调速

#设置GPIO编号模式:根据PCB编号

gpio.setmode(gpio.BOARD)
#检测是否进入调试模式
# 截断程序
gpio.setup(7, gpio.IN)
if gpio.input(7) :
    with open("/home/pi/ultrasonic-follow-carrier/out.log","a") as log:
        log.write("\nExit @ "+time.strftime('%Y-%m-%d %H:%M:%S'))
    exit()
#开串口
ser = serial.Serial("/dev/ttyAMA0", 460800)

gpio.setmode(gpio.BOARD)

#清空40Pin所有使用引脚,以便后续复用
#巨坑！
#实际使用后发现,该方法还是不行,cleanup函数还是没有权限清空之前程序调用的gpio模式，这意味着……若要清空似乎还是要麻烦一些的
#但是考虑到实际使用中，不存在GPIO复用的情况这个问题也就不存在了
#但是也是确实存在之前测试时复用GPIO产生的无法通信问题
#gpio.cleanup([7])
#gpio.cleanup([x for x in range(1,40)])


if __name__ == '__main__':
    
    while not gpio.input(7):
        while not gpio.input(7):
            init_motor()
            try:
                #尝试建立平台类
                pf = motor.Platform([[11,13,15,0.92],[22,16,18,1]])
                # pf.test()
            except :
                ser.write(b"s1e")
            else :
                ser.write(b"s0e")
                break
        # print("!!!!!!")
        while True:
            temp=str(serial_read())
            if temp[2] == "s":
                inde = temp.find('e')
                if inde == -1 :
                    continue
                init_data = int(temp[3:inde])
                break
        pf.set_Config(init_data,0)
        data=[[0,0]]
        error_times = 0
        stop_flag = False
        while not gpio.input(7):
            try:
                temp_data = serial_read().decode()
                # print("len=",len(temp_data))
                # print(temp_data)
                if temp_data[0:11] == 'sreboote':
                    #接收到重启指令
                    #print(1)
                    raise SonicError()
                temp = temp_data.split('e')[0].replace("sl","").split('r')
                # 根据通信输出结果
                # 计算dis和agl后输入data中
                result = [(int(temp[1])+int(temp[0]))/2,int(temp[1])-int(temp[0])]
                # print(result)
                data.append(result)
                # 注意data数据量以防止溢出
                if len(data) >200:
                    # 数据组应该是50Hz收入
                    # 200组即保留时间4s
                    data.pop(0)
                # print(len(data))
                pf.PID(data)
                pf.RUN()
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
                    pf.STOP()
                    stop_flag = True
                pass
            except SonicError :
                break
            except:
                continue
    if ser != None:
        ser.close()
    gpio.cleanup([x for x in range(1,40)])
    with open("/home/pi/ultrasonic-follow-carrier/out.log","a") as log:
        log.write("\nExit @ "+time.strftime('%Y-%m-%d %H:%M:%S'))
    exit()