import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft
import scipy.signal as signal
import scipy.signal as sig
import playground as pg
import pyaudio as au
import othermethods as om
import struct
import os

Fs = 16000.0
normalizationFactor = 2 ** -15

fid = wave.open('./audio/ref_samples.wav', 'rb')
reference = np.frombuffer(fid.readframes(-1), np.int16, -1)
fid.close()
reference = np.double(reference) * normalizationFactor

f, Pwelch_spec = signal.welch(reference, Fs, scaling='spectrum')

plt.semilogy(f, Pwelch_spec)
plt.xlabel('frequency [Hz]')
plt.ylabel('PSD')
plt.grid()
plt.show()

signalBack = reference

wav_file = wave.open('found_in_reference.wav', "w")
# wav params
nchannels = 1
sampwidth = 2
nframes = signalBack.size
comptype = "NONE"
compname = "not compressed"

wav_file.setparams((nchannels, sampwidth, Fs, nframes, comptype, compname))

for sample in signalBack:
    wav_file.writeframes(struct.pack('h', int(sample)))

wav_file.close()

print('Boom')