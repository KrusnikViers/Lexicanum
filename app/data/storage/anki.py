import html

import genanki
from app.data.language import Language
from app.data.card import Card
from app.data.deck import Deck
from app.data.status_or import Status
from app.data.storage.path import Path
from app.info import PROJECT_NAME, PUBLISHER_NAME

# Update this field each time the model is changed!
_MODEL_VERSION = 4
_MODEL_ID = hash("{}|{}|{}".format(PUBLISHER_NAME, PROJECT_NAME, _MODEL_VERSION)) % 10000000000


def _build_card_html(is_for_question: bool) -> str:
    return '''
        <div class="top_desc">
        {type} in {language}
        </div><hr/>
        <div class="statement">
        {statement}
        </div><hr/>
        <div class="bottom_desc">
        {note}
        </div>
    '''.format(type='{{type}}',
               language='{{question_language}}' if is_for_question else '{{answer_language}}',
               statement='{{question}}' if is_for_question else '{{answer}}',
               note='{{note}}')


_MODEL = genanki.Model(
    _MODEL_ID,
    "{} model".format(PROJECT_NAME),
    fields=[
        {'name': 'card_id'},
        {'name': 'type'},
        {'name': 'question'},
        {'name': 'question_language'},
        {'name': 'answer'},
        {'name': 'answer_language'},
        {'name': 'note'}
    ],
    sort_field_index=1,
    templates=[
        {
            'name': 'Direct question',
            'qfmt': _build_card_html(is_for_question=True),
            'afmt': _build_card_html(is_for_question=False),
        },
        {
            'name': 'Reverse question',
            'qfmt': _build_card_html(is_for_question=False),
            'afmt': _build_card_html(is_for_question=True),
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
        .top_desc,
        .bottom_desc {
            font-size: 12pt;
            color: #777
        }
    '''
)


class _Note(genanki.Note):
    def __init__(self, card: Card):
        super(_Note, self).__init__(
            model=_MODEL,
            fields=[
                str(card.card_id),
                card.card_type.name,
                html.escape(card.question),
                Language.DE.value,
                html.escape(card.answer),
                Language.EN.value,
                html.escape(card.note),
            ]
        )

    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


class AnkiIO:
    @staticmethod
    def write_to_file(deck: Deck, generic_path: Path) -> Status:
        output_deck = genanki.Deck(deck.deck_id, deck.deck_name)
        for card in deck.cards:
            output_deck.add_note(_Note(card))
        output_path = generic_path.with_suffix('.apkg')
        try:
            output_deck.write_to_file(output_path)
        except PermissionError as e:
            return Status.from_status('Writing to {} failed: {}'.format(output_path, str(e)))
        return Status.no_error()
