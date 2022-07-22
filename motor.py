import RPi.GPIO as gpio
import numpy as np

class Motor:
    '''
    电机类:
    初始化函数
    运动（函数）方向、速度-归一化
    '''
    def __init__(self,ctrl):
        self.en = ctrl[0]
        self.in1 = ctrl[1]
        self.in2 = ctrl[2]
        gpio.setmode(gpio.BOARD)
        #使用PWM类定义EN使能端,PWM频率为1kHz
        gpio.setup(self.en, gpio.OUT)
        self.EN = gpio.PWM(self.en,1000)
        #占空比为0,确保电机停转
        self.EN.start(0)
        gpio.setup(self.in1, gpio.OUT)
        gpio.setup(self.in2, gpio.OUT)
        #gpio.output(en, gpio.LOW)
        #gpio.cleanup()
    '''
    L298N 驱动表
    | en|in1|in2|effect|
    | 0 | x | x |  空  |
    | 1 | 0 | 0 |  空  |
    | 1 | 0 | 1 |  反  |
    | 1 | 1 | 0 |  正  |
    | 1 | 1 | 1 | 制动 |
    '''
    def symbol(self,num):
        #符号函数
        return 1 if num>=0 else 0 

    def run(self,speed):
        #输入要求：
        #speed∈[-1,1]
        gpio.output(self.in1,self.symbol(speed))
        gpio.output(self.in2,1-self.symbol(speed))
        self.EN.ChangeDutyCycle(abs(100*speed))


    def brake(self):
        gpio.output(self.in1,1)
        gpio.output(self.in2,1)
        self.EN.ChangeDutyCycle(100)

    def stop(self):
        gpio.output(self.in1,0)
        gpio.output(self.in2,0)
        self.EN.ChangeDutyCycle(0)

class Edge:
    '''
    单侧控制类,包含
    当前控制电机类
    当前速度
    运动(函数)
    '''
    def __init__(self,ctrl1,ctrl2):
        self.motor1 = Motor(ctrl1)#前轮
        self.motor2 = Motor(ctrl2)#后轮
        self.speed = 0
    
    def follow(self,speed):
        self.speed = speed
        motor1.run(speed)
        motor2.run(speed)

class Platform:
    '''
    平台整体控制类,包含
    两侧控制类
    当前速度
    pid(参数)
    pid(函数)
    串    out=p(in)+i(in)+d(in)
    并    out=d(i(p(in)))
    运动(函数)
    '''
    def __init__(self,dists,angle,ctrl):
        self.Left = Edge(ctrl[0],ctrl[1])#前轮
        self.Right = Edge(ctrl[2],ctrl[3])#后轮
        self.speed = [0,0]
        self.DISTS = dists
        self.ANGLE = angle
        self.dpp = 0.01
        self.dpi = 0.01
        self.dpd = 0.01
        self.app = 0.01
        self.api = 0.01
        self.apd = 0.01

    def PID(self,data):
        dists = data[0] - self.DISTS
        angle = data[1] - self.ANGLE
        self.speed[0] += self.dpp*dists[-1]+self.dpi*np.sum(dists)+self.dpd*(dists[-1]-dists[-2])
        self.speed[1] += self.app*angle[-1]+self.api*np.sum(angle)+self.apd*(angle[-1]-angle[-2])

    def RUN(self,data):
        #传入data:二重list,具有最近一段采样时间的一定数量的数据
        #0:距离
        #1:角度
        #PID 更新当前速度
        self.PID(speed,data)
        Left.follow(self.speed[0]-self.speed[1])
        Right.follow(self.speed[0]+self.speed[1])