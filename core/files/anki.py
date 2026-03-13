import hashlib
import html
from copy import deepcopy

import genanki

from core.info import PROJECT_NAME
from core.types import Card, Deck, Language, CardType
from core.util import UniversalPath, Status

# Update this field each time the model fields are changed.
_MODEL_VERSION = 8
# Update this field iff you need to make model versions unique for this particular program (e.g. in fork)
_MODEL_SALTED_VERSION = 'Original Model {}'.format(_MODEL_VERSION).encode('utf-8')

_MODEL_ASK_BOTH_ID = int(hashlib.md5(_MODEL_SALTED_VERSION).hexdigest()[:7], 16)
_MODEL_ASK_QUESTION_ID = _MODEL_ASK_BOTH_ID - 1
_MODEL_ASK_ANSWER_ID = _MODEL_ASK_QUESTION_ID - 2

# TODO: Update templates with new fields
_QUESTION_CARD = '''
<div class="top_desc">
  {{question_language}} {{type}}
</div><hr/>
<div class="content">
  {{question}}<br/>
  <div class="grammar_notes">
    {{grammar_info}}
  </div>
</div><hr/>
<div class="bottom_desc">
  {{meaning_note}}
</div>
'''

_ANSWER_CARD = '''
<div class="top_desc">
  {{answer_language}} {{type}}
</div><hr/>
<div class="content">
  {{answer}}
</div><hr/>
<div class="bottom_desc">
  {{meaning_note}}
</div>
'''

_MODEL_ASK_BOTH = genanki.Model(
    _MODEL_ASK_BOTH_ID,
    "{} Universal Model".format(PROJECT_NAME),
    fields=[
        {'name': 'card_id'},
        {'name': 'type'},
        {'name': 'question_main'},
        {'name': 'question_grammar'},
        {'name': 'question_language'},
        {'name': 'question_ipa'},
        {'name': 'question_example'},
        {'name': 'answer_main'},
        {'name': 'answer_language'},
        {'name': 'answer_example'},
        {'name': 'note'},
    ],
    sort_field_index=1,
    templates=[
        {
            'name': 'Direct question',
            'qfmt': _QUESTION_CARD,
            'afmt': _ANSWER_CARD
        },
        {
            'name': 'Reverse question',
            'qfmt': _ANSWER_CARD,
            'afmt': _QUESTION_CARD
        },
    ],
    css='''
      .card {
        font-family: arial;
        font-size: 25pt;
        text-align: center;
        color: black;
        background-color: white;
      }
      .content > .grammar_notes {
        font-size: 18pt;
      }
      .top_desc,
      .bottom_desc {
        font-size: 16pt;
        color: #888
      }
    '''
)

_MODEL_ASK_QUESTION = deepcopy(_MODEL_ASK_BOTH)
_MODEL_ASK_QUESTION.model_id = _MODEL_ASK_QUESTION_ID
_MODEL_ASK_QUESTION.name = '{} Question-only Model'.format(PROJECT_NAME)
_MODEL_ASK_QUESTION.templates = [
    {
        'name': 'Direct question',
        'qfmt': _QUESTION_CARD,
        'afmt': _ANSWER_CARD
    },
]

_MODEL_ASK_ANSWER = deepcopy(_MODEL_ASK_BOTH)
_MODEL_ASK_ANSWER.model_id = _MODEL_ASK_ANSWER_ID
_MODEL_ASK_ANSWER.name = '{} Answer-only Model'.format(PROJECT_NAME)
_MODEL_ASK_ANSWER.templates = [
    {
        'name': 'Reverse question',
        'qfmt': _ANSWER_CARD,
        'afmt': _QUESTION_CARD
    },
]


class _Note(genanki.Note):
    @staticmethod
    def _normalize_html_and_delimiters(original_line):
        return '<br/>'.join([html.escape(part.strip()) for part in original_line.split(Card.LINE_DELIMITER)])

    def __init__(self, card: Card, deck: Deck):
        self._deck_id = deck.deck_id
        model = _MODEL_ASK_QUESTION if card.card_type == CardType.CustomQuestion \
            else _MODEL_ASK_ANSWER if card.card_type == CardType.CustomAnswer \
            else _MODEL_ASK_BOTH
        super().__init__(
            model=model,
            fields=[
                str(card.card_id),
                CardType.display_name(card.card_type),
                self._normalize_html_and_delimiters(card.question_main),
                self._normalize_html_and_delimiters(card.question_grammar),
                Language.DE.value,
                html.escape(card.question_ipa),
                self._normalize_html_and_delimiters(card.question_example),
                self._normalize_html_and_delimiters(card.answer_main),
                Language.EN.value,
                self._normalize_html_and_delimiters(card.answer_example),
                self._normalize_html_and_delimiters(card.note),
            ]
        )

    @property
    def guid(self):
        return genanki.guid_for(self._deck_id, self.fields[0])


def write_file(deck: Deck, output_path: UniversalPath) -> Status:
    deck.normalize_for_output()
    output_deck = genanki.Deck(deck.deck_id, deck.deck_name)
    for card in deck.cards:
        output_deck.add_note(_Note(card, deck))
    try:
        output_deck.write_to_file(str(output_path))
    except PermissionError as e:
        return Status('Writing to {} failed: {}'.format(output_path, str(e)))
    return Status()
