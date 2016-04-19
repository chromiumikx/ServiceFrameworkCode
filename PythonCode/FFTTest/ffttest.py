import numpy as np
from scipy.fftpack import rfft, irfft, fftfreq

time   = np.linspace(0,10,2000)
signal = np.cos(5*np.pi*time)

W = fftfreq(signal.size, d=time[1]-time[0])
f_signal = rfft(signal)

import pylab as plt
plt.subplot(121)
plt.plot(time,signal)
plt.subplot(122)
plt.plot(W,f_signal)
plt.xlim(0,10)
plt.show()
