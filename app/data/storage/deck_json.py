import json
from typing import List
from app.data.card import Card, CardType

# Modify when incompatible changes are made to the underlying model
_JSON_VERSION = 1

class DeckJsonWriter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def export(self, deck: List[Card]):
        pass