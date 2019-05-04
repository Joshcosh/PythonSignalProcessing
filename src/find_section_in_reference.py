import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wf
import scipy.signal as sig
from scipy.fftpack import fft


def find_section_in_reference(ref_samples_file_name, section_file_name, graphs_dir, audio_output_dir):
    print('Joytunes exercise Uri Masheu')
    # add sounddevice later and use the commmand sd.play(data,Fs)
    normalization_factor = 2 ** -15
    frequency, reference = wf.read(ref_samples_file_name)
    reference = np.double(reference) * normalization_factor
    reference = reference[0:reference.size - 1]

    frequency, section = wf.read(section_file_name)
    section = np.double(section) * normalization_factor
    section = section[0:section.size - 1]

    # todo: rename h to something programmers understand :)
    h = sig.firwin(255, 0.1, pass_zero=False)
    # todo: rename H to something programmers understand :)
    # todo: rename f
    f, H = sig.freqz(h, 1, 1000, fs=16000)
    plt.plot(f, 20 * np.log10(np.abs(H)))
    # todo: rename y
    y = sig.lfilter(h, 1, reference)
    # todo: rename x
    x = np.arange(y.size) / frequency
    plt.plot(x, reference)
    plt.plot(x, y)
    plt.legend(['Unfiltered', 'Filtered'])
    # plt.show()
    plt.savefig(graphs_dir + 'filtering of reference with fir filter')
    reference_fft_abs = np.abs(fft(reference))
    print('Computing fft...')
    reference_fft_abs = reference_fft_abs[0:np.int(reference_fft_abs.size / 2)]
    y_fft_abs = np.abs(fft(y))
    y_fft_abs = y_fft_abs[0:int(y_fft_abs.size / 2)]
    resolution = np.double(reference_fft_abs.size)
    step = frequency / (2.0 * resolution)
    x = np.arange(0, 8000, step)
    print('Plotting frequency domain...')
    # todo: Find in plot docs why it gets stuck when running from terminal
    plt.plot(x, reference_fft_abs)
    plt.plot(x, y_fft_abs)
    plt.legend(['Unfiltered', 'Filtered'])
    # plt.show()
    plt.savefig(graphs_dir + 'fft filtering of reference with fir filter')
    y /= normalization_factor
    y = np.int16(y)

    print('Correlating signal with filtered reference...')
    # This runs on every section 1..6
    highest_correlation_index = np.argmax(np.correlate(y, section))
    # todo: instead of minute and second, use one variable of type Duration
    highest_correlation_minute = np.floor((highest_correlation_index / np.double(frequency)) / 60.0)
    highest_correlation_second = (highest_correlation_index / np.double(frequency)) % 60.0
    start_index = highest_correlation_index
    end_index = start_index + section.size
    section_in_reference = reference[start_index:end_index]
    print('Plotting section and reference in time domain...')
    plt.plot(section_in_reference)
    plt.plot(section)
    plt.legend(['sectionInReference', 'section'])
    # plt.show()
    plt.savefig(graphs_dir + 'section found comparison')
    print('Saving outputs...')
    wf.write(audio_output_dir + 'section2InReference.wav', frequency, section_in_reference)
    wf.write(audio_output_dir + 'filteredReference.wav', frequency, y)
    print('Done! :)')
