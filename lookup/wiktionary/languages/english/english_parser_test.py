import unittest
from typing import List

from lookup.wiktionary.languages.base.test_utils.wiktionary_cache_reader import get_test_content
from lookup.wiktionary.languages.english import EnglishLocaleParser
from lookup.wiktionary.types import MarkupTree, Definition, PartOfSpeech


class TestEnglishLocaleParser(unittest.TestCase):
    def test_reading_wiktionary_data(self):
        content = get_test_content(__file__, 'parrot.txt')
        self.assertEqual(content.title, 'parrot')
        self.assertEqual(content.language_code, 'en')
        self.assertGreater(len(content.content), 0)

    def test_parrot(self):
        content = get_test_content(__file__, 'parrot.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='parrot',
                           readable_name='Parrot', grammar_note='',
                           translation_articles=['Papagei']),
                Definition(PartOfSpeech.Verb, raw_article_title='parrot',
                           readable_name='to parrot', grammar_note='',
                           translation_articles=['nachplappern'])
            ])

    def test_binoculars(self):
        content = get_test_content(__file__, 'binoculars.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='binoculars',
                           readable_name='Binoculars', grammar_note='',
                           translation_articles=['Fernglas', 'Feldstecher'])
            ])

    def test_cut(self):
        content = get_test_content(__file__, 'cut.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Verb, raw_article_title='cut',
                           readable_name='to cut', grammar_note='',
                           translation_articles=['schneiden', 'einschneiden', 'trennen', 'ausschneiden', 'klappe',
                                                 'beschneiden', 'schwänzen', 'abheben']),
                Definition(PartOfSpeech.Adjective, raw_article_title='cut',
                           readable_name='cut', grammar_note='',
                           translation_articles=['geschnitten', 'geschliffen']),
                Definition(PartOfSpeech.Noun, raw_article_title='cut',
                           readable_name='Cut', grammar_note='',
                           translation_articles=['Schnitt', 'Filmbearbeitung', 'Bearbeitungsversion', 'Aufnahmestück',
                                                 'Stück']),
            ])

    def test_France(self):
        content = get_test_content(__file__, 'France.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='France',
                           readable_name='France', grammar_note='',
                           translation_articles=['Frankreich'])
            ])


def test_sheep(self):
    content = get_test_content(__file__, 'sheep.txt')
    tree = MarkupTree.build(content.title, content.content)
    self.assertCountEqual(
        EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
        [
            Definition(PartOfSpeech.Noun, raw_article_title='sheep',
                       readable_name='Sheep', grammar_note='',
                       translation_articles=['Schaf'])
        ])


def test_woman(self):
    content = get_test_content(__file__, 'woman.txt')
    tree = MarkupTree.build(content.title, content.content)
    self.assertCountEqual(
        EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
        [
            Definition(PartOfSpeech.Verb, raw_article_title='woman',
                       readable_name='to woman', grammar_note='',
                       translation_articles=['feminisieren', 'verweiblichen'])
        ])
