import glob
import os.path
import shutil
import unittest
from pathlib import Path

from build_tools import qt_gen_ui_files

_TEST_FILE_UI = 'test_form.ui'
_TEST_FILE_GEN_UI = 'test_form_uic.py'


class QtGetUiTest(unittest.TestCase):
    local_test_dir = Path(os.path.realpath(__file__)).parent / 'test_data'
    initial_set_of_files = []

    def setUp(self):
        self.initial_set_of_files = glob.glob(str(self.local_test_dir / '*'))
        for test_file in self.initial_set_of_files:
            file_path = Path(test_file)
            if file_path.suffix == '.testdata':
                file_path.copy(file_path.parent / file_path.stem)

    def tearDown(self):
        # Remove all files except the initial set.
        temp_files_list = glob.glob(str(self.local_test_dir / '*'))
        for temp_file in temp_files_list:
            if temp_file in self.initial_set_of_files:
                continue

            file_path = Path(temp_file)
            if file_path.is_file():
                file_path.unlink()
            else:
                shutil.rmtree(str(file_path))

    def test_empty_run(self):
        self.local_test_dir.joinpath(_TEST_FILE_UI).unlink()
        qt_gen_ui_files.regenerate_files(self.local_test_dir)

    def test_generate_files(self):
        self.assertEqual(qt_gen_ui_files.generate_files(self.local_test_dir), 1)
        self.assertTrue(self.local_test_dir.joinpath(_TEST_FILE_GEN_UI).is_file())

    def test_remove_generated_files(self):
        qt_gen_ui_files.generate_files(self.local_test_dir)
        self.assertEqual(qt_gen_ui_files.remove_generated_files(self.local_test_dir), 1)
        self.assertFalse(self.local_test_dir.joinpath(_TEST_FILE_GEN_UI).is_file())

    def test_regenerate_files(self):
        qt_gen_ui_files.regenerate_files(self.local_test_dir)
        self.assertTrue(self.local_test_dir.joinpath(_TEST_FILE_GEN_UI).is_file())

    def test_not_a_file(self):
        self.local_test_dir.joinpath('not_a_file.ui').mkdir()
        with self.assertRaises(ValueError):
            qt_gen_ui_files.generate_files(self.local_test_dir)
