import unittest

from lookup.wiktionary.languages.base.testing_utils import get_test_content


class TestEnglishNouns(unittest.TestCase):
    def test_reading_wiktionary_data(self):
        content = get_test_content(__file__, 'parrot.txt')
        self.assertEqual(content.title, 'parrot')
        self.assertEqual(content.language_code, 'en')
        self.assertGreater(len(content.content), 0)
