import unittest

from lookup.wiktionary.languages.base.test_utils.test_content_reader import get_test_content
from lookup.wiktionary.languages.english import EnglishLocaleParser
from lookup.wiktionary.types.markup_tree import MarkupTree


class TestEnglishNouns(unittest.TestCase):
    def test_reading_wiktionary_data(self):
        content = get_test_content(__file__, 'parrot.txt')
        self.assertEqual(content.title, 'parrot')
        self.assertEqual(content.language_code, 'en')
        self.assertGreater(len(content.content), 0)

    def test_parrot(self):
        content = get_test_content(__file__, 'parrot.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components_from_markup(tree, content.title, ['de', 'ru'])
        for dc in dc_list:
            print(dc)
        print()

    def test_binoculars(self):
        content = get_test_content(__file__, 'binoculars.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components_from_markup(tree, content.title, ['de', 'ru'])
        for dc in dc_list:
            print(dc)
        print()

    def test_cut(self):
        content = get_test_content(__file__, 'cut.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components_from_markup(tree, content.title, ['de', 'ru'])
        for dc in dc_list:
            print(dc)
        print()

    def test_France(self):
        content = get_test_content(__file__, 'France.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components_from_markup(tree, content.title, ['de', 'ru'])
        for dc in dc_list:
            print(dc)
        print()

    def test_sheep(self):
        content = get_test_content(__file__, 'sheep.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components_from_markup(tree, content.title, ['de', 'ru'])
        for dc in dc_list:
            print(dc)
        print()

    def test_woman(self):
        content = get_test_content(__file__, 'woman.txt')
        tree = MarkupTree.build(content.title, content.content)
        dc_list = EnglishLocaleParser.extract_definition_components_from_markup(tree, content.title, ['de', 'ru'])
        for dc in dc_list:
            print(dc)
        print()
