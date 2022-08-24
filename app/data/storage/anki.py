import html
from typing import List

import genanki

from app.data.card import Card
from app.info import PROJECT_NAME, PUBLISHER_NAME

# Update this field each time the model is changed!
_MODEL_VERSION = 1

# Last 10 digits of hashed (hopefully) unique model id string.
# App version is not used, because different versions still can use the same model
_MODEL_ID = hash("{}|{}|{}".format(PUBLISHER_NAME, PROJECT_NAME, _MODEL_VERSION)) % 10000000000

_MODEL = genanki.Model(
    _MODEL_ID,
    "{} model".format(PROJECT_NAME),
    fields=[
        {'name': 'card_id'},
        {'name': 'question'},
        {'name': 'answer'},
        {'name': 'type'},
        {'name': 'note'}
    ],
    sort_field_index=1,
    templates=[
        {
            'name': 'Direct question',
            'qfmt': '{{type}}<hr/>{{question}}<hr/>{{note}}',
            'afmt': '{{type}}<hr/>{{answer}}<hr/>{{note}}',
        },
        {
            'name': 'Reverse question',
            'qfmt': '{{type}}<hr/>{{answer}}<hr/>{{note}}',
            'afmt': '{{type}}<hr/>{{question}}<hr/>{{note}}',
        },
    ])


class _Note(genanki.Note):
    def __init__(self, card: Card):
        super(_Note, self).__init__(
            model=_MODEL,
            fields=[
                str(card.time_id),
                html.escape(card.question),
                html.escape(card.answer),
                card.card_type.name,
                html.escape(card.note),
            ]
        )

    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


class AnkiWriter:
    def __init__(self, file_path: str):
        self.file_path: str = file_path

    def export(self, deck: List[Card]):
        anki_deck = genanki.Deck(112332142314, 'Some Name')
        for card in deck:
            anki_deck.add_note(_Note(card))
        anki_deck.write_to_file(self.file_path)
