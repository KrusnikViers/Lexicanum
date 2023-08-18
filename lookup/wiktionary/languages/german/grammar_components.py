from typing import List

from core.util import safe_get
from lookup.wiktionary.languages.german.shared_constants import POS_MAP
from lookup.wiktionary.types import MarkupTree, DefinitionComponent, DCType, PartOfSpeech

_EMPTY_OPTIONS = ('', ' ', '-', '—')


def _noun_grammar(node: MarkupTree) -> List[DefinitionComponent]:
    _GENDERED_ARTICLES = {'n': 'Das', 'm': 'Der', 'f': 'Die'}
    gender = node.keyed_args.get('Genus', 'n')
    assert gender in _GENDERED_ARTICLES  # If there are articles like that, fail-proof solution should be based on them.
    gendered_article = _GENDERED_ARTICLES[gender]

    singular_form = None
    if node.keyed_args.get('Nominativ Singular', '') not in _EMPTY_OPTIONS:
        singular_form = '{} {}'.format(gendered_article, node.keyed_args['Nominativ Singular'])

    plural_form = None
    if node.keyed_args.get('Nominativ Plural', '') not in _EMPTY_OPTIONS:
        plural_form = 'Die {}'.format(node.keyed_args['Nominativ Plural'])

    if not singular_form and not plural_form:
        return []
    elif singular_form and plural_form:
        readable_form = singular_form
        grammar_note = plural_form
    elif singular_form:
        readable_form = singular_form
        grammar_note = 'Nur Singular'
    else:
        readable_form = plural_form
        grammar_note = 'Nur Plural'

    return [
        DefinitionComponent(node.level, DCType.ReadableForm, readable_form),
        DefinitionComponent(node.level, DCType.GrammarNote, grammar_note),
    ]


def _verb_grammar(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    grammar_notes: List[str] = []

    present_1st = node.keyed_args.get('Präsens_ich', '-')
    if present_1st != '-' and present_1st != wiki_title[:-1]:
        grammar_notes.append('ich {}'.format(present_1st))
    present_2nd = node.keyed_args.get('Präsens_du', '-')
    if present_2nd != '-' and present_2nd != wiki_title[:-2] + 'st':
        grammar_notes.append('du {}'.format(present_2nd))
    present_3rd = node.keyed_args.get('Präsens_er, sie, es', '-')
    if present_3rd != '-' and present_3rd != wiki_title[:-2] + 't':
        grammar_notes.append('er/sie/es {}'.format(present_3rd))

    if grammar_notes:
        return [DefinitionComponent(node.level, DCType.GrammarNote, '; '.join(grammar_notes))]
    return []


def pronoun_grammar_components(node: MarkupTree) -> List[DefinitionComponent]:
    grammar_note = 'Deklination: m, f, n, plural'
    _DECLINATIONS = ['Nominativ', 'Genitiv', 'Dativ', 'Akkusativ']
    _TYPES = ['Singular m', 'Singular f', 'Singular n', 'Plural']
    for declination in _DECLINATIONS:
        words_list = []
        for word_type in _TYPES:
            words_list.append(node.keyed_args.get('{} {}'.format(declination, word_type), '-'))
        if words_list.count('-') != len(_TYPES):
            grammar_note += '; {}: {}'.format(declination, ', '.join(words_list))
    if grammar_note.count(';') != 0:
        return [DefinitionComponent(node.level, DCType.GrammarNote, grammar_note)]


def grammar_components(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    pos_key = safe_get(node.name.split(), 1)
    if pos_key not in POS_MAP:
        return []

    match POS_MAP[pos_key]:
        case PartOfSpeech.Noun:
            return _noun_grammar(node)
        case PartOfSpeech.Verb:
            return _verb_grammar(node, wiki_title)

    return []
