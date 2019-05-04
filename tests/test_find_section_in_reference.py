import filecmp
from unittest import TestCase

from find_section_in_reference import find_section_in_reference


class TestFindSectionInReference(TestCase):
    def test_find_section_in_reference(self):
        ref_samples_file_name = '../audio/ref_samples.wav'
        section_file_name = '../audio/section6.wav'
        graphs_dir = '../graphs/'
        audio_output_dir = '../audioout/'
        find_section_in_reference(ref_samples_file_name, section_file_name, graphs_dir, audio_output_dir)
        files_equal = filecmp.cmp('test_files/expectedSection2InReference.wav',
                                  audio_output_dir + 'section2InReference.wav')
        self.assertTrue(files_equal)
