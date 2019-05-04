from find_section_in_reference import find_section_in_reference


def main():
    ref_samples_file_name = '../audio/ref_samples.wav'
    section_file_name = '../audio/section6.wav'
    graphs_dir = '../graphs/'
    audio_output_dir = '../audioout/'

    find_section_in_reference(ref_samples_file_name, section_file_name, graphs_dir, audio_output_dir)


if __name__ == '__main__':
    main()
