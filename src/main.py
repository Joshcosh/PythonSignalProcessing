import audio_search
import numpy as np
import os
import datetime


def main():
    print('~~~ Joytunes exercise by Uri Shilo ~~~')
    audio_dir = '../audio/'
    print('Creating outputs dir')
    current_dt = datetime.datetime.now()
    current_dt = current_dt.strftime("../outputs_%Y%m%d%H%M%S")
    graphs_dir = current_dt + '/graphs/'
    audio_output_dir = current_dt + '/sections_in_reference/'

    os.mkdir(current_dt)
    os.mkdir(graphs_dir)
    os.mkdir(audio_output_dir)

    ref_samples_file_name = 'ref_samples.wav'
    section_file_names = ['section1', 'section2', 'section3',
                          'section4', 'section5', 'section6']

    index_start_array = np.zeros(len(section_file_names), dtype=int)
    index_end_array = np.zeros(len(section_file_names), dtype=int)

    print('Loading reference...')
    frequency, reference = audio_search.load_wave_file(audio_dir + ref_samples_file_name)

    print('Creating filter...')
    reference_filtered = audio_search.filter(reference, graphs_dir + 'filter freq response')

    for i, section_file_name in enumerate(section_file_names):
        print('---> Section' + str(i+1) + ':')
        print('Load wave file...')
        frequency, section = audio_search.load_wave_file(audio_dir + section_file_name + '.wav')

        print('Search start...')
        index_start_array[i], index_end_array[i] = \
            audio_search.correlate_signal_with_reference(reference_filtered, section)
        print('Search done...')

        audio_search.save_outputs(audio_output_dir + section_file_name + '.wav', frequency, section)

        print('Creating plots...')
        audio_search.plot_section_and_found_interval\
            (graphs_dir + section_file_name, frequency, section,
             reference[index_start_array[i]:index_end_array[i]],
             index_start_array[i], index_end_array[i])

    print('Done!')

if __name__ == '__main__':
    main()
