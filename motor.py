import RPi.GPIO as gpio, numpy as np, time

class Motor:
    '''
    电机类:
    初始化函数
    运动（函数）方向、速度-归一化
    '''
    def __init__(self,ctrl):
        #ctrl为三元素列表，包含三个功能引脚的标号(以BOARD方式计)
        self.en = ctrl[0]
        self.in1 = ctrl[1]
        self.in2 = ctrl[2]
        gpio.setmode(gpio.BOARD)
        #使用PWM类定义EN使能端,PWM频率为1kHz
        gpio.setup(self.en, gpio.OUT)
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
        #符号函数,为run函数判断运动方向
        return 1 if num>=0 else 0 

    def run(self,speed):
        #运动函数
        #输入要求：
        #speed∈[-1,1]
        gpio.output(self.in1,self.symbol(speed))
        gpio.output(self.in2,1-self.symbol(speed))
        self.EN.ChangeDutyCycle(abs(100*speed))


    def brake(self):
        #刹车函数-施加反向作用力
        gpio.output(self.in1,1)
        gpio.output(self.in2,1)
        self.EN.ChangeDutyCycle(100)

    def stop(self):
        #停转函数-电机自由转动
        gpio.output(self.in1,0)
        gpio.output(self.in2,0)
        self.EN.ChangeDutyCycle(0)

class Platform:
    '''
    平台整体控制类,包含
    两侧电机控制类
    当前速度
    pid(参数)
    pid(函数)
    串    out=p(in)+i(in)+d(in)
    并    out=d(i(p(in)))
    运动(函数)
    '''
    def __init__(self,ctrl,dists=0,angle=0):
        self.Left = Motor(ctrl[0])#前轮
        self.Right = Motor(ctrl[1])#后轮
        self.speed = [0,0]
        self.DISTS = dists
        self.ANGLE = angle
        self.dpp = 0.01
        self.dpi = 0.01
        self.dpd = 0.01
        self.app = 0.01
        self.api = 0.01
        self.apd = 0.01
    
    def set_Config(self,dists,angle):
        self.DISTS = dists
        self.ANGLE = angle

    def PID(self,data):
        dists = [dist - self.DISTS for dist in data[0]]
        angle = [angl - self.ANGLE for angl in data[0]]
        self.speed[0] += self.dpp*dists[-1]+self.dpi*np.sum(dists)+self.dpd*(dists[-1]-dists[-2])
        self.speed[1] += self.app*angle[-1]+self.api*np.sum(angle)+self.apd*(angle[-1]-angle[-2])

    def RUN(self,data):
        #传入data:二重list,具有最近一段采样时间的一定数量的数据
        #0:距离
        #1:角度
        #PID 更新当前速度
        self.PID(data)
        self.Left.run(self.speed[0]-self.speed[1])
        self.Right.run(self.speed[0]+self.speed[1])
        
    def test(self):
        self.Left.run(1)
        self.Right.run(-1)
        time.sleep(0.2)
        self.Left.stop()
        self.Right.stop()