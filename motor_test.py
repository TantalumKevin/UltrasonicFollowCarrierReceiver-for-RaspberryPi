import motor,time
import numpy as np

#       en,in1,in2
ctrl = [[3,5,7],[12,8,10]]

mt0 = motor.Motor(ctrl[0])
mt1 = motor.Motor(ctrl[1])

for i in range(-100,100):
    mt0.run(i/100)
    mt1.run(i/100)
    time.sleep(0.02)

mt0.run(1)
mt1.run(1)
time.sleep(1)
mt0.run(0)
mt1.run(0)