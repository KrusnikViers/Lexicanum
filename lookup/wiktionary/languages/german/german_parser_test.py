import unittest
from typing import List

from lookup.wiktionary.languages.base.test_utils.wiktionary_cache_reader import get_test_content
from lookup.wiktionary.languages.german import GermanLocaleParser
from lookup.wiktionary.types.markup_tree import MarkupTree


class TestGermanLocaleParser(unittest.TestCase):
    @staticmethod
    def _print_components(title: str, components: List):
        print('--- {} ---'.format(title))
        for component in components:
            print(str(component))
        print()

    def test_reading_wiktionary_data(self):
        content = get_test_content(__file__, 'Papagei.txt')
        self.assertEqual(content.title, 'Papagei')
        self.assertEqual(content.language_code, 'de')
        self.assertGreater(len(content.content), 0)

    def test_parrot(self):
        content = get_test_content(__file__, 'Papagei.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = GermanLocaleParser.extract_definition_components(tree, content.title, ['en', 'ru'])
        self._print_components(content.title, dc_list)

    def test_gehen(self):
        content = get_test_content(__file__, 'gehen.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = GermanLocaleParser.extract_definition_components(tree, content.title, ['en', 'ru'])
        self._print_components(content.title, dc_list)

    def test_Gemuse(self):
        content = get_test_content(__file__, 'Gemuse.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = GermanLocaleParser.extract_definition_components(tree, content.title, ['en', 'ru'])
        self._print_components(content.title, dc_list)

    def test_Morgen(self):
        content = get_test_content(__file__, 'Morgen.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = GermanLocaleParser.extract_definition_components(tree, content.title, ['en', 'ru'])
        self._print_components(content.title, dc_list)

    def test_schwer(self):
        content = get_test_content(__file__, 'schwer.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = GermanLocaleParser.extract_definition_components(tree, content.title, ['en', 'ru'])
        self._print_components(content.title, dc_list)
