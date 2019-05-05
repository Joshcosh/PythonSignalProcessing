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


def plot_section_and_found_interval(graphs_dir, section, section_in_reference):
    print('Plotting section and reference in time domain...')
    plt.plot(section_in_reference)
    plt.plot(section)
    plt.legend(['sectionInReference', 'section'])
    # plt.show()
    plt.savefig(graphs_dir + 'section found comparison')


def correlate_signal_with_reference(reference, section):
    print('Correlating signal with filtered reference...')
    # This runs on every section 1..6
    highest_correlation_index = np.argmax(np.correlate(reference, section))
    # todo: instead of minute and second, use one variable of type Duration
    start_index = highest_correlation_index
    end_index = start_index + section.size

    return start_index, end_index


def plot_original_and_filtered_fft(graphs_dir, reference_fft_abs, x, y, y_fft_abs):
    print('Plotting frequency domain...')
    # todo: Find in plot docs why it gets stuck when running from terminal
    plt.plot(x, reference_fft_abs)
    plt.plot(x, y_fft_abs)
    plt.legend(['Unfiltered', 'Filtered'])
    # plt.show()
    plt.savefig(graphs_dir + 'fft filtering of reference with fir filter')


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
