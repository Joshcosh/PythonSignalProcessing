import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def correlate(a, b):
    y = 0
    # h = np.flipud(b)
    h = b
    crossCorrelationVec = np.zeros((a.size+2*b.size-2), dtype=np.double)
    zaz = np.zeros((a.size+2*b.size-2), dtype=np.double)
    zaz[b.size-1:b.size+a.size-1] = a
    maxVal = 0
    maxValIndex = 0

    for index in range(crossCorrelationVec.size-h.size):
        crossCorrelationVec[index] = np.dot(h, zaz[index:index+h.size])
        if crossCorrelationVec[index] > maxVal:
            maxVal = crossCorrelationVec[index]
            maxValIndex = index

    numOfSample = np.arange(crossCorrelationVec.size)

    fig, ax = plt.subplots()
    ax.plot(numOfSample, crossCorrelationVec)

    ax.set(xlabel='num of sample (correlation)', ylabel='correlation',
           title='correlation result')
    ax.grid()

    fig.savefig("correlation.png")

    plt.show()
    maxValIndex = np.argmin(crossCorrelationVec)
    argMaxUnshifted = maxValIndex - b.size + 1

    return argMaxUnshifted

def calcEnergiesVec(inputVec, winSize):
    indexVec = np.arange(0, inputVec.size, winSize)

    outputVec = np.zeros(indexVec.size, dtype=np.double)
    outputIndex = 0

    for ind in indexVec:
        outputVec[outputIndex] = np.dot(inputVec[ind:ind+winSize], inputVec[ind:ind+winSize])
        outputIndex += 1

    return outputVec


def calcOverlappingEnergies(inputVec, winSize, shift):
    indexVec = np.arange(0, inputVec.size, shift)

    outputVec = np.zeros(indexVec.size, dtype=np.double)
    outputIndex = 0

    for ind in indexVec:
        outputVec[outputIndex] = np.dot(inputVec[ind:ind+winSize], inputVec[ind:ind+winSize])
        outputIndex += 1

    return outputVec

def calcOverlappingFft(inputVec, winSize, shift):
    indexVec = np.arange(0, inputVec.size, shift)

    outputVec = np.zeros(indexVec.size, dtype=np.double)
    outputIndex = 0

    for ind in indexVec:
        outputVec[outputIndex] = np.dot(inputVec[ind:ind+winSize], inputVec[ind:ind+winSize])
        outputIndex += 1

    return outputVec

def getVec():
    return np.arange(4)

def findMaxAutoCorr(signal):
    autoCorrVec = np.correlate(signal, signal, 'full')
    return np.argmax(autoCorrVec)

def graphExamples():
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig("test.png")
    plt.show()

