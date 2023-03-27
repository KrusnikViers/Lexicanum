from typing import List
from lookup.wiktionary.internal.interface_internals import SourceLookupData, WordDefinition


def maybe_print_answer_start(text: str):
    print('\n\n\n>>>>>>>>>>> Answer Lookup: {}'.format(text))


def maybe_print_question_start(text: str):
    print('\n\n\n>>>>>>>>>>> Question Lookup: {}'.format(text))

def maybe_print_source_definitions(source_definitions: List[WordDefinition]):
    print('\n--START---- Definitions ----------')
    for definition in source_definitions:
        print(str(definition))
    print('---END----- Definitions ----------')

def maybe_print_source_data(data: SourceLookupData):
    # return
    print('\n--START---- Source Data ----------')
    for key, value in data.translated_words_to_sources.items():
        print('{}:'.format(key))
        for definition in value:
            print(' -{}'.format(str(definition)))
    print('Unique words: {}'.format(', '.join(data.unique_translation_titles)))
    print('---END----- Source Data ----------')
