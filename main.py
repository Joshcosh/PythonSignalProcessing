import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from scipy.fftpack import fft, ifft
import scipy.io.wavfile as wf
import wave
import struct
#import sounddevice as sd

# add sounddevice later and use the commmand sd.play(data,Fs)

normalizationFactor = 2 ** -15

Fs, reference = wf.read('./audio/ref_samples.wav')

reference = np.double(reference) * normalizationFactor


h = sig.firwin(256, 500, 40, nyq=16000)

# b,a = sig.iirfilter(4,500,0.3,40,'lowpass',ftype='ellip')
#
# yiir = sig.lfilter(b,a,reference)



y = sig.lfilter(h,1,reference)
x = np.arange(y.size) / Fs
plt.plot(x,reference)
plt.plot(x,y)
plt.legend(['Unfiltered', 'Filtered'])
plt.show()
plt.savefig('filtering of reference with fir filter')

y = y/normalizationFactor
y = np.int16(y)

wf.write('filteredReference.wav', Fs, y)


print('Boom')