import unittest
from typing import List

from lookup.wiktionary.languages.base.test_utils.wiktionary_cache_reader import get_test_content
from lookup.wiktionary.languages.german import GermanLocaleParser
from lookup.wiktionary.types import MarkupTree, Definition, PartOfSpeech


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
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='Papagei',
                           readable_name='Der Papagei', grammar_note='Die Papageien',
                           translation_articles=['parrot', 'popinjay', 'parroter'])
            ]
        )

    def test_gehen(self):
        content = get_test_content(__file__, 'gehen.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Verb, raw_article_title='gehen',
                           readable_name='gehen', grammar_note='',
                           translation_articles=[
                               'walk', 'go', 'leave', 'work', 'operable', 'sell', 'extend', 'reach', 'last', 'go on',
                               'prove', 'tolerable', 'practicable', 'do', 'be on'])
            ]
        )

    def test_Gemuse(self):
        content = get_test_content(__file__, 'Gemuse.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='Gemüse',
                           readable_name='Das Gemüse', grammar_note='Die Gemüse',
                           translation_articles=['vegetable', 'vegetables'])
            ]
        )

    def test_Morgen(self):
        content = get_test_content(__file__, 'Morgen.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.maxDiff = None
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='Morgen',
                           readable_name='Der Morgen', grammar_note='Die Morgen',
                           translation_articles=['morning', 'good morning']),
                Definition(PartOfSpeech.Noun, raw_article_title='Morgen',
                           readable_name='Das Morgen', grammar_note='Nur singular',
                           translation_articles=['morrow', 'tomorrow'])
            ]
        )

    def test_schwer(self):
        content = get_test_content(__file__, 'schwer.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Adverb, raw_article_title='schwer',
                           readable_name='schwer', grammar_note='',
                           translation_articles=['a damn lot']),
                Definition(PartOfSpeech.Adjective, raw_article_title='schwer',
                           readable_name='schwer', grammar_note='',
                           translation_articles=['heavy', 'difficult', 'hard', 'grave', 'serious'])
            ]
        )

    def test_ab_und_zu(self):
        content = get_test_content(__file__, 'ab_und_zu.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Phrase, raw_article_title='ab_und_zu',
                           readable_name='Ab und zu', grammar_note='',
                           translation_articles=['from time to time', 'off and on', 'on and off', 'now and then']),
            ]
        )
