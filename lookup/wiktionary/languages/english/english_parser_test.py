import unittest

from lookup.wiktionary.languages.base.test_utils.wiktionary_cache_reader import get_test_content
from lookup.wiktionary.languages.english import EnglishLocaleParser
from lookup.wiktionary.types import MarkupTree, Definition, PartOfSpeech


class TestEnglishLocaleParser(unittest.TestCase):
    maxDiff = None

    def test_definition_reading_wiktionary_data(self):
        content = get_test_content(__file__, 'parrot.txt')
        self.assertEqual(content.title, 'parrot')
        self.assertEqual(content.language_code, 'en')
        self.assertGreater(len(content.content), 0)

    def test_definition_parrot(self):
        content = get_test_content(__file__, 'parrot.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='parrot',
                           readable_name='Parrot', grammar_note='',
                           translation_articles=['Papagei']),
                Definition(PartOfSpeech.Verb, raw_article_title='parrot',
                           readable_name='To parrot', grammar_note='',
                           translation_articles=['nachplappern'])
            ])

    def test_definition_binoculars(self):
        content = get_test_content(__file__, 'binoculars.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='binoculars',
                           readable_name='Binoculars', grammar_note='Mainly plural; Singular variant: Binocular',
                           translation_articles=['Fernglas', 'Feldstecher'])
            ])

    def test_definition_cut(self):
        content = get_test_content(__file__, 'cut.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Verb, raw_article_title='cut',
                           readable_name='To cut', grammar_note='Cuts; Cutting; Cut',
                           translation_articles=['schneiden', 'einschneiden', 'trennen', 'ausschneiden', 'klappe',
                                                 'beschneiden', 'schwänzen', 'abheben']),
                Definition(PartOfSpeech.Adjective, raw_article_title='cut',
                           readable_name='Cut', grammar_note='',
                           translation_articles=['geschnitten', 'geschliffen']),
                Definition(PartOfSpeech.Noun, raw_article_title='cut',
                           readable_name='Cut', grammar_note='Cuts',
                           translation_articles=['Schnitt', 'Filmbearbeitung', 'Bearbeitungsversion', 'Aufnahmestück',
                                                 'Stück']),
            ])

    def test_definition_France(self):
        content = get_test_content(__file__, 'France.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='France',
                           readable_name='France', grammar_note='Mainly plural; Frances',
                           translation_articles=['Frankreich'])
            ])

    def test_definition_sheep(self):
        content = get_test_content(__file__, 'sheep.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Noun, raw_article_title='sheep',
                           readable_name='Sheep', grammar_note='Sheeps; Sheep',
                           translation_articles=['Schaf'])
            ])

    def test_definition_woman(self):
        content = get_test_content(__file__, 'woman.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Verb, raw_article_title='woman',
                           readable_name='To woman', grammar_note='',
                           translation_articles=['feminisieren', 'verweiblichen'])
            ])

    def test_definition_or(self):
        content = get_test_content(__file__, 'or.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.maxDiff = None
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Conjunction, raw_article_title='or',
                           readable_name='Or', grammar_note='',
                           translation_articles=['oder']),
                Definition(PartOfSpeech.Noun, raw_article_title='or',
                           readable_name='Or', grammar_note='Ors',
                           translation_articles=['Gold']),
                Definition(PartOfSpeech.Adjective, raw_article_title='or',
                           readable_name='Or', grammar_note='Generally not comparable',
                           translation_articles=['golden']),
            ])

    def test_definition_eleven(self):
        content = get_test_content(__file__, 'eleven.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Numeral, raw_article_title='eleven',
                           readable_name='Eleven', grammar_note='',
                           translation_articles=['elf'])
            ])

    def test_definition_from(self):
        content = get_test_content(__file__, 'from.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Preposition, raw_article_title='from',
                           readable_name='From', grammar_note='',
                           translation_articles=['von', 'aus', 'vor'])
            ])

    def test_definition_go(self):
        content = get_test_content(__file__, 'go.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Verb, raw_article_title='go',
                           readable_name='To go', grammar_note='Goes; Going; Went; Gone',
                           translation_articles=['gehen', 'dran', 'sein', 'ziehen', 'verschwinden', 'weggehen',
                                                 'fortgehen', 'kaputtgehen', 'kaputt', 'machen', 'los']),
                Definition(PartOfSpeech.Noun, raw_article_title='go',
                           readable_name='Go', grammar_note='Gos; Goes',
                           translation_articles=['Versuch']),
                Definition(PartOfSpeech.Noun, raw_article_title='go',
                           readable_name='Go', grammar_note='Mainly plural',
                           translation_articles=['Go']),
            ]
        )

    def test_definition_good(self):
        content = get_test_content(__file__, 'good.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Adjective, raw_article_title='good',
                           readable_name='Good', grammar_note='Better; The best',
                           translation_articles=['gut', 'brav', 'gehörig', 'lecker', 'gesund', 'schön', 'angenehm',
                                                 'effektiv']),
                Definition(PartOfSpeech.Noun, raw_article_title='good',
                           readable_name='Good', grammar_note='Goods',
                           translation_articles=['Gute', 'Gut']),
            ])

    def test_definition_hello(self):
        content = get_test_content(__file__, 'hello.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Interjection, raw_article_title='hello',
                           readable_name='Hello', grammar_note='',
                           translation_articles=['hallo', 'guten Tag', 'servus', 'moin', 'grüß Gott', 'jemand da?',
                                                 'halloho'])
            ])

    def test_definition_into(self):
        content = get_test_content(__file__, 'into.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Preposition, raw_article_title='into',
                           readable_name='Into', grammar_note='',
                           translation_articles=['in', 'gen', 'gegen', 'nach Beginn', 'für', 'auf', 'nach',
                                                 'hinsichtlich'])
            ])

    def test_definition_the(self):
        content = get_test_content(__file__, 'the.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Article, raw_article_title='the',
                           readable_name='The', grammar_note='',
                           translation_articles=['der', 'die', 'das', 'dieser']),
                Definition(PartOfSpeech.Adverb, raw_article_title='the',
                           readable_name='The', grammar_note='',
                           translation_articles=['je desto', 'je umso', 'je je', 'umso'])

            ])

    def test_definition_whose(self):
        content = get_test_content(__file__, 'whose.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Pronoun, raw_article_title='whose',
                           readable_name='Whose', grammar_note='',
                           translation_articles=['dessen', 'wessen', 'deren']),
                Definition(PartOfSpeech.Pronoun, raw_article_title='whose',
                           readable_name='Whose', grammar_note='',
                           translation_articles=['wem gehört gehören']),
            ])

    def test_definition_youre_welcome(self):
        content = get_test_content(__file__, 'youre_welcome.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Phrase, raw_article_title="you're_welcome",
                           readable_name="You're welcome", grammar_note='',
                           translation_articles=['bitte', 'gern geschehen', 'keine Ursache', 'nichts zu danken'])
            ])

    def test_definition_nope(self):
        content = get_test_content(__file__, 'nope.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Particle, raw_article_title='nope',
                           readable_name='Nope', grammar_note='',
                           translation_articles=['nee', 'nö']),
            ])

    def test_definition_important(self):
        content = get_test_content(__file__, 'important.txt')
        tree = MarkupTree.build(content.title, content.content)
        self.assertCountEqual(
            EnglishLocaleParser.extract_definitions(tree, content.title, ['de']),
            [
                Definition(PartOfSpeech.Adjective, raw_article_title='important',
                           readable_name='Important', grammar_note='',
                           translation_articles=['wichtig'], meaning_note='', ipa_note='')

            ])
