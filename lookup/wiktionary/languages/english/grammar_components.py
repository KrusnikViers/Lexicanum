from typing import List

from core.util import safe_get
from lookup.wiktionary.types import MarkupTree, DefinitionComponent, DCType, PartOfSpeech


def _noun_grammar(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    grammar_notes = []
    if node.name == 'en-plural noun':
        grammar_notes.append('Mainly plural')
    if node.plain_args:
        for plain_arg in node.plain_args:
            if plain_arg == '~':
                new_form = wiki_title.capitalize() + 's'
            elif plain_arg == '-':
                new_form = 'Mainly plural'
            elif len(plain_arg) < 4 and safe_get(plain_arg, -1) == 's':
                new_form = wiki_title.capitalize() + plain_arg
            else:
                new_form = plain_arg.capitalize()
            if new_form not in grammar_notes:
                grammar_notes.append(new_form)
    if 'sg' in node.keyed_args:
        grammar_notes.append('Singular variant: {}'.format(node.keyed_args['sg'].capitalize()))
    if grammar_notes:
        return [DefinitionComponent(node.level, DCType.GrammarNote, '; '.join(grammar_notes))]
    return []


def _verb_grammar(node: MarkupTree, wiki_title: str) -> List[DefinitionComponent]:
    readable_form = DefinitionComponent(node.level, DCType.ReadableForm, 'To {}'.format(wiki_title))
    grammar_notes = []
    for plain_arg in node.plain_args:
        grammar_notes.append(plain_arg.capitalize())
    if grammar_notes:
        return [readable_form,
                DefinitionComponent(node.level, DCType.GrammarNote, '; '.join(grammar_notes))]
    return [readable_form]


def _adjective_grammar(node: MarkupTree) -> List[DefinitionComponent]:
    grammar_notes = []
    for plain_arg in node.plain_args:
        if plain_arg == '-':
            grammar_notes.append('Generally not comparable')
        else:
            grammar_notes.append(plain_arg.capitalize())
    if 'sup' in node.keyed_args:
        grammar_notes.append('The {}'.format(node.keyed_args['sup']))
    if grammar_notes:
        return [DefinitionComponent(node.level, DCType.GrammarNote, '; '.join(grammar_notes))]
    return []


def grammar_components(node: MarkupTree, pos: PartOfSpeech, wiki_title: str) -> List[DefinitionComponent]:
    match pos:
        case PartOfSpeech.Noun:
            return _noun_grammar(node, wiki_title)
        case PartOfSpeech.Verb:
            return _verb_grammar(node, wiki_title)
        case PartOfSpeech.Adjective:
            return _adjective_grammar(node)
    return []
