import motor,time
import numpy as np
import RPi.GPIO as gpio
pf = motor.Platform([[11,13,15,0.92],[22,16,18,1]])
pf.test()

'''
#       en,in1,in2
ctrl = [[11,13,15],[22,16,18]]

mt0 = motor.Motor(ctrl[0])
mt1 = motor.Motor(ctrl[1])
for i in range(20,100):
    mt0.run(i/100)
    mt1.run(i/100)
    time.sleep(0.02)
mt0.run(0.5)
mt1.run(0.5)
time.sleep(0.5)
mt0.run(0)
mt1.run(0)
gpio.cleanup()
'''