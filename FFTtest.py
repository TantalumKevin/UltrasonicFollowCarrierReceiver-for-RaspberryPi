from scipy.fftpack import fft
import numpy as np, time


#采样率-采样次数/s
srate = 1280 * 1000
#采样周期
speriod = 1/srate
#采样点数
N = 40 * 1000
pi = 3.1415926
# (0.0,采样点*周期数,采样点)
t = np.linspace(0.0, N * speriod, N)
y = np.sin(2*pi*t) + 10*np.sin(40*1000*2*pi*t) + np.sin(2*pi*20*1000*t) + np.sin(2*pi*10*1000*t) + np.sin(2*pi*5*1000*t)
start = time.time()
yfft = abs(fft(y))
n = N/2
yfft /= n
binwidth = srate/N
f = np.linspace(0.0, srate-binwidth, N)
print("yf:",len(yfft))
print("fmax:",srate-binwidth)
print("dur:",N * speriod)
print("处理耗时：",time.time()-start)
i = 0
while True:
    if f[i] == 40*1000:
        break
    i += 1
print(yfft[i])