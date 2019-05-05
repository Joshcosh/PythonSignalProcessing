import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wf
import scipy.signal as sig
from scipy.fftpack import fft

NORMALIZATION_FACTOR = 2 ** -15


def normalize(y):
    y /= NORMALIZATION_FACTOR
    y = np.int16(y)
    return y


def save_outputs(audio_output_file, frequency, section):
    print('Saving output...')
    wf.write(audio_output_file, frequency, section)


def plot_section_and_found_interval(file_name, frequency, section, section_in_reference, index_start, index_end):
    t = np.arange(index_start, index_end)
    t = np.double(t)
    t /= np.double(frequency)
    plt.plot(t, section_in_reference)
    plt.plot(t, section)
    plt.legend(['section in reference', 'section'])
    # plt.show()
    plt.savefig(file_name)
    plt.close()


def correlate_signal_with_reference(reference, section):
    print('Correlating signal with filtered reference...')
    # This runs on every section 1..6
    highest_correlation_index = np.argmax(np.correlate(reference, section))
    # todo: instead of minute and second, use one variable of type Duration
    start_index = highest_correlation_index
    end_index = start_index + section.size

    return start_index, end_index


def plot_original_and_filtered(frequency, graphs_dir, reference, y):
    x = np.arange(y.size) / frequency
    plt.plot(x, reference)
    plt.plot(x, y)
    plt.legend(['Unfiltered', 'Filtered'])
    # plt.show()
    plt.savefig(graphs_dir + 'filtering of reference with fir filter')
    plt.close()


def filter(reference, plot_name):
    h = sig.firwin(255, 0.1, pass_zero=False)
    f, H = sig.freqz(h, 1, 1000, fs=16000)
    plt.plot(f, 20 * np.log10(np.abs(H)))
    plt.title('FIR High Pass Filter')
    plt.savefig(plot_name)
    plt.close()
    y = sig.lfilter(h, 1, reference)
    return y


def load_wave_file(ref_samples_file_name):
    frequency, reference = wf.read(ref_samples_file_name)
    reference = np.double(reference) * NORMALIZATION_FACTOR
    reference = reference[0:reference.size - 1]
    return frequency, reference
