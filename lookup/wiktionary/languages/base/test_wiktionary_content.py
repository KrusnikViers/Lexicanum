import unittest

from build_tools.refresh_wiktionary_test_data import refresh_wiktionary_test_data


class TestWiktionaryContent(unittest.TestCase):
    def test_content_needs_refreshing(self):
        self.assertFalse(refresh_wiktionary_test_data(dry_run=True))
