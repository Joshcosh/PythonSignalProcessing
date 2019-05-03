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

Fs, section = wf.read('./audio/section2.wav')
section = np.double(section) * normalizationFactor
section = section[0:section.size - 1]


h = sig.firwin(255, 0.1, pass_zero=False)
f, H = sig.freqz(h, 1, 1000, fs=16000)
plt.plot(f, 20*np.log10(np.abs(H)))

y = sig.lfilter(h, 1, reference)
x = np.arange(y.size) / Fs

plt.plot(x, reference)
plt.plot(x, y)
plt.legend(['Unfiltered', 'Filtered'])
plt.show()
plt.savefig('./graphs/filtering of reference with fir filter')

referencefftabs = np.abs(fft(reference))
referencefftabs = referencefftabs[0:np.int(referencefftabs.size/2)]
yfftabs = np.abs(fft(y))
yfftabs = yfftabs[0:int(yfftabs.size/2)]
resolution = np.double(referencefftabs.size)
step = Fs/(2.0*resolution)
x = np.arange(0, 8000, step)

plt.plot(x, referencefftabs)
plt.plot(x, yfftabs)
plt.legend(['Unfiltered', 'Filtered'])
plt.show()
plt.savefig('./graphs/fft filtering of reference with fir filter')

y = y/normalizationFactor
y = np.int16(y)


indexOfHighestCorrelation = np.argmax(np.correlate(y, section))

MinuteOfHighestCorrelation = np.floor((indexOfHighestCorrelation / np.double(Fs)) / 60.0)
SecondOfHighestCorrelation = (indexOfHighestCorrelation / np.double(Fs)) % 60.0

startIndex = indexOfHighestCorrelation
endIndex = startIndex + section.size

sectionInReference = y[startIndex:endIndex]

wf.write('./audioout/section2InReference.wav', Fs, sectionInReference)


wf.write('./audioout/filteredReference.wav', Fs, y)

print('Boom')
