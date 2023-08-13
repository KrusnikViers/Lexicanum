import unittest
from typing import List

from lookup.wiktionary.languages.base.test_utils.wiktionary_cache_reader import get_test_content
from lookup.wiktionary.languages.english import EnglishLocaleParser
from lookup.wiktionary.types.markup_tree import MarkupTree


class TestEnglishLocaleParser(unittest.TestCase):
    @staticmethod
    def _print_components(title: str, components: List):
        print('--- {} ---'.format(title))
        for component in components:
            print(str(component))
        print()

    def test_reading_wiktionary_data(self):
        content = get_test_content(__file__, 'parrot.txt')
        self.assertEqual(content.title, 'parrot')
        self.assertEqual(content.language_code, 'en')
        self.assertGreater(len(content.content), 0)

    def test_parrot(self):
        content = get_test_content(__file__, 'parrot.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components(tree, content.title, ['de', 'ru'])
        self._print_components(content.title, dc_list)

    def test_binoculars(self):
        content = get_test_content(__file__, 'binoculars.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components(tree, content.title, ['de', 'ru'])
        self._print_components(content.title, dc_list)

    def test_cut(self):
        content = get_test_content(__file__, 'cut.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components(tree, content.title, ['de', 'ru'])
        self._print_components(content.title, dc_list)

    def test_France(self):
        content = get_test_content(__file__, 'France.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components(tree, content.title, ['de', 'ru'])
        self._print_components(content.title, dc_list)

    def test_sheep(self):
        content = get_test_content(__file__, 'sheep.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components(tree, content.title, ['de', 'ru'])
        self._print_components(content.title, dc_list)

    def test_woman(self):
        content = get_test_content(__file__, 'woman.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components(tree, content.title, ['de', 'ru'])
        self._print_components(content.title, dc_list)
