import motor,time
import numpy as np

#       en,in1,in2
ctrl = [[3,5,7],[8,10,12]]

mt0 = motor.Motor(ctrl[0])
mt1 = motor.Motor(ctrl[1])
for i in range(-100,100):
    mt1.run(i/100)
    mt2.run(i/100)
    time.sleep(0.02)
