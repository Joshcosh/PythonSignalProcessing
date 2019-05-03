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
reference = reference[0:reference.size - 1]

h = sig.firwin(256, 6000, 40, fs=Fs)

y = sig.lfilter(h,1,reference)
# x = np.arange(y.size) / Fs
# plt.plot(x,reference)
# plt.plot(x,y)
# plt.legend(['Unfiltered', 'Filtered'])
# plt.show()
# plt.savefig('filtering of reference with fir filter')


referencefftabs = np.abs(fft(reference))
yfftabs = np.abs(fft(y))
resolution = np.double(referencefftabs.size)
step = Fs/resolution
x = np.arange(-8000, 8000, step)

plt.plot(x, referencefftabs)
plt.plot(x, yfftabs)
plt.legend(['Unfiltered', 'Filtered'])
plt.show()
plt.savefig('fft filtering of reference with fir filter')

y = y/normalizationFactor
y = np.int16(y)

wf.write('filteredReference.wav', Fs, y)


print('Boom')