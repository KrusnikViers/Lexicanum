import html
from pathlib import Path

import genanki

from app.data.card import Card
from app.data.deck import Deck
from app.info import PROJECT_NAME, PUBLISHER_NAME

# Update this field each time the model is changed!
_MODEL_VERSION = 2
_MODEL_ID = hash("{}|{}|{}".format(PUBLISHER_NAME, PROJECT_NAME, _MODEL_VERSION)) % 10000000000

_MODEL = genanki.Model(
    _MODEL_ID,
    "{} model".format(PROJECT_NAME),
    fields=[
        {'name': 'card_id'},
        {'name': 'type'},
        {'name': 'question'},
        {'name': 'answer'},
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
                str(card.card_id),
                card.card_type.name,
                html.escape(card.question),
                html.escape(card.answer),
                html.escape(card.note),
            ]
        )

    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])


class AnkiWriter:
    @staticmethod
    def write_to_file(deck: Deck, output: Path) -> bool:
        anki_deck = genanki.Deck(deck.deck_id, deck.deck_name)
        for card in deck.cards:
            anki_deck.add_note(_Note(card))
        anki_deck.write_to_file(str(output))
        return True
