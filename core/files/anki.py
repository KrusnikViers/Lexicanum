import hashlib
import html

import genanki

from core.helpers import UniversalPath, Status
from core.info import PROJECT_NAME
from core.types import Card, Deck, Language

# Update this field each time the model fields are changed. This will require manual conversion of already existing
# cards in Anki manually.
_MODEL_VERSION = 5
# Update this field iff you need to make model versions unique for this particular program (e.g. in fork)
_MODEL_SALTED_VERSION = 'Original Model {}'.format(_MODEL_VERSION).encode('utf-8')

_MODEL_ID = int(hashlib.md5(_MODEL_SALTED_VERSION).hexdigest()[:7], 16)

_QUESTION_CARD = '''
<div class="top_desc">
  {{question_language}} {{type}}
</div><hr/>
<div class="content">
  {{question}}<br/>
  <div class="additional">
    {{question_additional}}
  </div>
</div><hr/>
<div class="bottom_desc">
  {{note}}
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
  {{note}}
</div>
'''

_MODEL = genanki.Model(
    _MODEL_ID,
    "{} Model".format(PROJECT_NAME),
    fields=[
        {'name': 'card_id'},
        {'name': 'type'},
        {'name': 'question'},
        {'name': 'question_additional'},
        {'name': 'question_language'},
        {'name': 'answer'},
        {'name': 'answer_language'},
        {'name': 'note'}
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
      .content > .additional {
        margin-top: 8px;
        font-size: 18pt;
      }
      .top_desc,
      .bottom_desc {
        font-size: 16pt;
        color: #888
      }
    '''
)


class _Note(genanki.Note):
    def __init__(self, card: Card):
        question_split = [html.escape(part.strip()) for part in card.question.split('/')]
        super(_Note, self).__init__(
            model=_MODEL,
            fields=[
                str(card.card_id),
                card.card_type.name,
                question_split[0],
                '<br/>'.join(question_split[1:]),
                Language.DE.value,
                html.escape(card.answer),
                Language.EN.value,
                html.escape(card.note),
            ]
        )

    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


def write_file(deck: Deck, output_path: UniversalPath) -> Status:
    deck.normalize_for_output()
    output_deck = genanki.Deck(deck.deck_id, deck.deck_name)
    for card in deck.cards:
        output_deck.add_note(_Note(card))
    output_path_str = output_path.with_suffix('.apkg')
    try:
        output_deck.write_to_file(output_path_str)
    except PermissionError as e:
        return Status('Writing to {} failed: {}'.format(output_path_str, str(e)))
    return Status()
