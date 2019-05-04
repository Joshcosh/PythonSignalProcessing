import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wf
import scipy.signal as sig
from scipy.fftpack import fft

NORMALIZATION_FACTOR = 2 ** -15


def find_section_in_reference(ref_samples_file_name, section_file_name, graphs_dir, audio_output_dir):
    print('Joytunes exercise Uri Masheu')
    # add sounddevice later and use the commmand sd.play(data,Fs)
    frequency, reference = load_wave_file(ref_samples_file_name)
    frequency, section = load_wave_file(section_file_name)
    # todo: if frequency of both is not equal, raise error

    y = filter(reference)

    plot_original_and_filtered(frequency, graphs_dir, reference, y)

    reference_fft_abs, x, y_fft_abs = compute_fft(frequency, reference, y)

    y = plot_original_and_filtered_fft(graphs_dir, reference_fft_abs, x, y, y_fft_abs)

    section_in_reference = correlate_signal_with_reference(frequency, reference, section, y)

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


def correlate_signal_with_reference(frequency, reference, section, y):
    print('Correlating signal with filtered reference...')
    # This runs on every section 1..6
    highest_correlation_index = np.argmax(np.correlate(y, section))
    # todo: instead of minute and second, use one variable of type Duration
    highest_correlation_minute = np.floor((highest_correlation_index / np.double(frequency)) / 60.0)
    highest_correlation_second = (highest_correlation_index / np.double(frequency)) % 60.0
    start_index = highest_correlation_index
    end_index = start_index + section.size
    section_in_reference = reference[start_index:end_index]
    return section_in_reference


def plot_original_and_filtered_fft(graphs_dir, reference_fft_abs, x, y, y_fft_abs):
    print('Plotting frequency domain...')
    # todo: Find in plot docs why it gets stuck when running from terminal
    plt.plot(x, reference_fft_abs)
    plt.plot(x, y_fft_abs)
    plt.legend(['Unfiltered', 'Filtered'])
    # plt.show()
    plt.savefig(graphs_dir + 'fft filtering of reference with fir filter')
    y /= NORMALIZATION_FACTOR
    y = np.int16(y)
    return y


def compute_fft(frequency, reference, y):
    print('Computing fft...')
    reference_fft_abs = np.abs(fft(reference))
    reference_fft_abs = reference_fft_abs[0:np.int(reference_fft_abs.size / 2)]
    y_fft_abs = np.abs(fft(y))
    y_fft_abs = y_fft_abs[0:int(y_fft_abs.size / 2)]
    resolution = np.double(reference_fft_abs.size)
    step = frequency / (2.0 * resolution)
    x = np.arange(0, 8000, step)
    return reference_fft_abs, x, y_fft_abs


def plot_original_and_filtered(frequency, graphs_dir, reference, y):
    # todo: rename x
    x = np.arange(y.size) / frequency
    plt.plot(x, reference)
    plt.plot(x, y)
    plt.legend(['Unfiltered', 'Filtered'])
    # plt.show()
    plt.savefig(graphs_dir + 'filtering of reference with fir filter')


def filter(reference):
    # todo: rename h to something programmers understand :)
    h = sig.firwin(255, 0.1, pass_zero=False)
    # todo: rename H to something programmers understand :)
    # todo: rename f
    f, H = sig.freqz(h, 1, 1000, fs=16000)
    plt.plot(f, 20 * np.log10(np.abs(H)))
    # todo: rename y
    y = sig.lfilter(h, 1, reference)
    return y


def load_wave_file(ref_samples_file_name):
    frequency, reference = wf.read(ref_samples_file_name)
    reference = np.double(reference) * NORMALIZATION_FACTOR
    reference = reference[0:reference.size - 1]
    return frequency, reference
