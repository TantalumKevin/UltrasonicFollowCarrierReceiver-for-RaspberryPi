import motor,time
import numpy as np

#       en,in1,in2
ctrl = [[3,5,7],[8,10,12],[11,13,15],[19,21,23]]

mt = motor.Motor(ctrl[0])
for i in range(-100,100):
    mt.run(i/100)
    time.sleep(20)
