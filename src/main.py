import audio_search
import numpy as np
import os


def main():
    print('~~~ Joytunes exercise by Uri Shilo ~~~')
    audio_dir = '../audio/'
    graphs_dir = '../graphs/'
    audio_output_dir = '../sections_in_reference/'
    os.makedirs(audio_output_dir)
    ref_samples_file_name = 'ref_samples.wav'
    section_file_names = ['section1.wav', 'section2.wav', 'section3.wav',
                          'section4.wav', 'section5.wav', 'section6.wav']
    index_start_array = np.zeros(len(section_file_names), dtype=int)
    index_end_array = np.zeros(len(section_file_names), dtype=int)

    print('Loading reference...')
    frequency, reference = audio_search.load_wave_file(audio_dir + ref_samples_file_name)

    print('Creating filter...')
    reference_filtered = audio_search.filter(reference)

    for i, section_file_name in enumerate(section_file_names):
        print('---> Section' + str(i+1) + ':')
        print('Load wave file...')
        frequency, section = audio_search.load_wave_file(audio_dir + section_file_name)
        print('Search start...')
        index_start_array[i], index_end_array[i] = \
            audio_search.correlate_signal_with_reference(reference_filtered, section)
        print('Search done...')
        audio_search.save_outputs(audio_output_dir+section_file_name, frequency, section)

    print('Creating plots...')




    print('Done!')

if __name__ == '__main__':
    main()
