import numpy as np
import sys
from scipy import signal

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def holder_metric(reference, section):
    '''
    find section <b> in reference <a> using the holder metric
    returns the index of shortest distance
    '''
    a = reference
    b = section
    resultsVec = np.zeros((a.size-b.size), dtype=np.double)
    minVal = sys.maxint
    minValIndex = 0

    for index in range(resultsVec.size):
        if index+b.size < a.size:
            # resultsVec[index] = np.power(np.sum(np.power(np.abs(b - a[index:index+b.size]), pow)), 1/pow)
            resultsVec[index] = np.sum(np.abs(b - a[index:index + b.size]))
            if resultsVec[index] < minVal:
                minVal = resultsVec[index]
                minValIndex = index
        if index%160000 == 0:
            print(index)
        if index == resultsVec.size - 2:
            print('here')

    return minValIndex
