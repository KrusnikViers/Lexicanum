from typing import List

from core.types import Card
from lookup.interface.request import LookupRequest


class LookupResponse:
    def __init__(self, cards: List[Card], request: LookupRequest):
        self.cards = cards
        self.request = request

    def __str__(self):
        return 'LookupResponse for {}:\n{}'.format(str(self.request), '\n'.join(map(str, self.cards)))
