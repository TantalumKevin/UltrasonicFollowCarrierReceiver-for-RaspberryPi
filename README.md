# Ultrasonic Follow Carrier

## 1介绍
**本项目为2021-2022学年第二学期电气工程学院2020级卓越班嵌入式系统与智能设计课程设计：超声波跟随载物平台之树莓派端。**
根据设计，树莓派为载物平台驱动核心，运行Python语言代码，驱动传感器与电机。

## 2结构

### 2.1 文件结构
```Python
.
┣━ main.py         #主程序，包含控制全流程
┣━ motor_test.py   #电机驱动测试程序(非关键程序，可删除)
┗━ motor.py        #电机底层驱动(main.py讲调用此文件，务必将其与main.py放在同一文件夹内)
```

### 2.2 程序结构

程序流程如下所示:

**┌>调用串口-><br>
│使能传感器-><br>
│获取初始回传数据-><br>
│循环读取传感器数据-><br>
│[根据传感器原始数据计算目标相对位置->]<br>
│使用PID算法调控电机 ─┐<br>
 └───────────────┘**

## 3驱动

### 3.1 传感器驱动
根据设计，传感器与上位机间通讯协议为串口通信，参数115200+8n1，通信数据为字符串格式，以```'s'```作为开始，以```'e'```作为结束。<br>
相关通信指令如下:<br>
1. hello:发送数据```"shelloe"```，使能传感器，使其开始传输数据。此时传感器正常回报```"shelloe"```，否则无输出。
2. test:接受数据```"steste"```，此时上位机收到后可以自行处理，无回报。
3. x in range(0,10):发送数据
```"sxe"```，其中```x```代表错误号以便于排查问题。
4. 传感器数据回报格式:```"s"```->```数据```->```"e"```；
5. 回报顺序: ```Δt```-> ```ΔD1```->```ΔD2```

### 3.2 电机驱动

本项目电机驱动采用L298N双路电机驱动模块，同侧前轮后轮电机共用一路，从而实现```前进```、```后退```以及```差速转向```。<br>
L298N驱动模块驱动表如下:
| EN | IN1 | IN2 | Effect(效果) |
|:-----:|:-----:|:-----:|:-----:|
| 0 | x | x | 空 |
| 1 | 0 | 0 | 空 |
| 1 | 0 | 1 | 反 |
| 1 | 1 | 0 | 正 |
| 1 | 1 | 1 | 制动 |

为实现电机转速可调，可在使能端(EN)施加PWM波用以调速。

```motor.py```中对隔引脚定义如下:
```Python
class Motor:
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
```

同时可根据驱动表写出运动函数:
```Python
class Motor:
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
```

而```./motor.py```中包含的```Platform```类则是根据项目需求封装的更高级别的类，以驱动四个电机，包含;
- 初始化函数(  ```__init(self,ctrl,dists=0,angle=0)```)
- 参数设置函数(```set_Config(self,dists,angle)```)
- PID调速函数(```PID(self,data)```)
- 运动函数(```RUN(self,data)```)
- 测试函数(```test(self)```),用于测试电机情况


#### 本项目其他仓库传送门
| Transmitter for Arduino UNO | Transmitter PCB | Receiver for Raspberry Pi | Receiver for STM32F103 | Receiver PCB |
| ---- | ---- | ---- | ---- | ---- |
| [Github](https://github.com/TantalumKevin/UltrasonicFollowCarrierTransmitter-for-ArduinoUNO) | [Github](https://github.com/TantalumKevin/UltrasonicFollowCarrierTransmitter-PCB) | [Github](https://github.com/TantalumKevin/UltrasonicFollowCarrierReceiver-for-RaspberryPi)  | [Github](https://github.com/TantalumKevin/UltrasonicFollowCarrierReceiver-for-STM32F103) | [Github](https://github.com/TantalumKevin/UltrasonicFollowCarrierReceiver-PCB) |
| [Gitee](https://gitee.com/kevin_ud/ultrasonic-follow-carrier-transmitter-for-arduino-uno)  | [Gitee](https://gitee.com/kevin_ud/ultrasonic-follow-carrier-transmitter-pcb) | [Gitee](https://gitee.com/kevin_ud/ultrasonic-follow-carrier)  | [Gitee](https://gitee.com/kevin_ud/ultrasonic-follow-carrier-receiver-for-stm32-f103) | [Gitee](https://gitee.com/kevin_ud/ultrasonic-follow-carrier-receiver-pcb) |
