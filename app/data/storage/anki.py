import html

import genanki

from app.data.card import Card
from app.data.deck import Deck
from app.data.status_or import Status
from app.data.storage.path import Path
from app.info import PROJECT_NAME, PUBLISHER_NAME

# Update this field each time the model is changed!
_MODEL_VERSION = 2
_MODEL_ID = hash("{}|{}|{}".format(PUBLISHER_NAME, PROJECT_NAME, _MODEL_VERSION)) % 10000000000

# TODO: Fix ANKI cards type

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
