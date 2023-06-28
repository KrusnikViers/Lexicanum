from copy import deepcopy
from typing import List, Dict, NamedTuple

from lookup.wiktionary.types.definition import Definition, PartOfSpeech


class DefinitionSetKey(NamedTuple):
    wiki_title: str
    part_of_speech: PartOfSpeech


DefinitionSet = Dict[DefinitionSetKey, List[Definition]]


# If words are similar up to translation, it means that there could be different translations for a different meanings.
# We'll split translations into exclusive and common buckets, and create separate records for all non-empty buckets.
def _merge_similar_definitions(existing_definition: Definition, new_definition: Definition,
                               definitions_list: List[Definition]) -> List[Definition]:
    common_translations = []
    only_new_translations = []
    for new_translation in new_definition.translation_articles:
        if new_translation in existing_definition.translation_articles:
            common_translations.append(new_translation)
        else:
            only_new_translations.append(new_translation)

    if len(common_translations) == len(existing_definition.translation_articles):
        # There is no need for exclusive record for old definition
        existing_definition.meaning_note += ' / {}'.format(new_definition.meaning_note)
    else:
        existing_definition.translation_articles = [x for x in existing_definition.translation_articles if
                                                    x not in common_translations]
        if common_translations:
            common_definition = deepcopy(existing_definition)
            common_definition.meaning_note += ' / {}'.format(new_definition.meaning_note)
            common_definition.translation_articles = common_translations
            definitions_list.append(common_definition)
    if only_new_translations:
        new_definition.translation_articles = only_new_translations
        definitions_list.append(deepcopy(new_definition))
    return definitions_list


def _add_definition_to_key(new_definition: Definition, definitions_list: List[Definition]) -> List[Definition]:
    definition_deduplicated = False
    for dedup_candidate in definitions_list:
        # If readable form of grammar information is different, words are different enough to be separate records.
        if dedup_candidate.readable_name != new_definition.readable_name or \
                dedup_candidate.grammar_note != new_definition.grammar_note:
            continue

        definition_deduplicated = True
        # If anything matches up to meaning note, just add missing translation options to existing definition.
        if dedup_candidate.meaning_note == new_definition.meaning_note:
            for new_translation in new_definition.translation_articles:
                if new_translation not in dedup_candidate.translation_articles:
                    dedup_candidate.translation_articles.append(new_translation)
        else:
            definitions_list = _merge_similar_definitions(dedup_candidate, new_definition, definitions_list)

    if not definition_deduplicated:
        definitions_list.append(deepcopy(new_definition))
    return definitions_list


def build_definition_set(definitions: List[Definition]) -> DefinitionSet:
    result: DefinitionSet = dict()
    for definition in definitions:
        # There is nothing we can do if no translations were extracted.
        if not definition.translation_articles:
            continue

        key = DefinitionSetKey(definition.raw_article_title, definition.part_of_speech)
        if key not in result:
            result[key] = [deepcopy(definition)]
        else:
            result[key] = _add_definition_to_key(definition, result[key])
    return result
