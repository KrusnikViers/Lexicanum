import unittest

from lookup.wiktionary.languages.base.test_utils.wiktionary_cache_reader import get_test_content
from lookup.wiktionary.languages.german import GermanLocaleParser
from lookup.wiktionary.types import MarkupTree, Definition, PartOfSpeech


class TestGermanLocaleParser(unittest.TestCase):
    maxDiff = None

    def test_definition_reading_wiktionary_data(self):
        content = get_test_content(__file__, 'Papagei.txt')
        self.assertEqual(content.title, 'Papagei')
        self.assertEqual(content.language_code, 'de')
        self.assertGreater(len(content.content), 0)

    def test_definition_parrot(self):
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

    def test_definition_gehen(self):
        content = get_test_content(__file__, 'gehen.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Verb, raw_article_title='gehen',
                           readable_name='Gehen', grammar_note='',
                           translation_articles=[
                               'walk', 'go', 'leave', 'work', 'operable', 'sell', 'extend', 'reach', 'last', 'go on',
                               'prove', 'tolerable', 'practicable', 'do', 'be on'])
            ]
        )

    def test_definition_Gemuse(self):
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

    def test_definition_Morgen(self):
        content = get_test_content(__file__, 'Morgen.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='Morgen',
                           readable_name='Der Morgen', grammar_note='Die Morgen',
                           translation_articles=['morning', 'good morning']),
                Definition(PartOfSpeech.Noun, raw_article_title='Morgen',
                           readable_name='Das Morgen', grammar_note='Nur Singular',
                           translation_articles=['morrow', 'tomorrow'])
            ]
        )

    def test_definition_nicht(self):
        content = get_test_content(__file__, 'nicht.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Adverb, raw_article_title='nicht',
                           readable_name='Nicht', grammar_note='',
                           translation_articles=['not']),
                Definition(PartOfSpeech.Particle, raw_article_title='nicht',
                           readable_name='Nicht', grammar_note='',
                           translation_articles=['not']),
            ]
        )

    def test_definition_schwer(self):
        content = get_test_content(__file__, 'schwer.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Adjective, raw_article_title='schwer',
                           readable_name='Schwer', grammar_note='',
                           translation_articles=['heavy', 'difficult', 'hard', 'grave', 'serious']),
                Definition(PartOfSpeech.Particle, raw_article_title='schwer',
                           readable_name='Schwer', grammar_note='',
                           translation_articles=['a damn lot']),
            ]
        )

    def test_definition_ab_und_zu(self):
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

    def test_definition_wessen(self):
        content = get_test_content(__file__, 'wessen.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Pronoun, raw_article_title='wessen',
                           readable_name='Wessen', grammar_note='',
                           translation_articles=['whose']),
            ]
        )

    def test_definition_aus(self):
        content = get_test_content(__file__, 'aus.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Preposition, raw_article_title='aus',
                           readable_name='Aus', grammar_note='',
                           translation_articles=['from', 'out of', 'of']),
                Definition(PartOfSpeech.Adverb, raw_article_title='aus',
                           readable_name='Aus', grammar_note='',
                           translation_articles=['over', 'off', 'out of']),
            ]
        )

    def test_definition_und(self):
        content = get_test_content(__file__, 'und.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Conjunction, raw_article_title='und',
                           readable_name='Und', grammar_note='',
                           translation_articles=['and']),
            ]
        )

    def test_definition_hallo(self):
        content = get_test_content(__file__, 'hallo.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Interjection, raw_article_title='hallo',
                           readable_name='Hallo', grammar_note='',
                           translation_articles=['hi', 'hello']),
            ]
        )

    def test_definition_die(self):
        content = get_test_content(__file__, 'die.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Article, raw_article_title='die',
                           readable_name='Die',
                           grammar_note='Deklination: m, f, n, plural; ' +
                                        'Nominativ: der, die, das, die; ' +
                                        'Genitiv: des, der, des, der; ' +
                                        'Dativ: dem, der, dem, den; ' +
                                        'Akkusativ: den, die, das, die',
                           translation_articles=['the'])
            ]
        )

    def test_definition_von(self):
        content = get_test_content(__file__, 'von.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Preposition, raw_article_title='von',
                           readable_name='Von', grammar_note='',
                           translation_articles=['from', 'about', 'of']),
            ]
        )

    def test_definition_zwanzig(self):
        content = get_test_content(__file__, 'zwanzig.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Numeral, raw_article_title='zwanzig',
                           readable_name='Zwanzig', grammar_note='',
                           translation_articles=['twenty']),
            ]
        )

    def test_definition_sprechen(self):
        content = get_test_content(__file__, 'sprechen.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            GermanLocaleParser.extract_definitions(tree, content.title, ['en']),
            [
                Definition(PartOfSpeech.Verb, raw_article_title='sprechen',
                           readable_name='Sprechen', grammar_note='du sprichst; er/sie/es spricht',
                           translation_articles=['speak', 'propose', 'talk']),
            ]
        )
