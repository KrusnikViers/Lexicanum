import csv
from pathlib import Path
from typing import List

from app.data.card import Card
from app.info import PROJECT_NAME


class CSVWrapper:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.resolve()

    @classmethod
    def register_dialect(cls):
        custom_dialect = csv.Dialect
        custom_dialect.quoting = csv.QUOTE_MINIMAL
        custom_dialect.quotechar = '`'
        custom_dialect.delimiter = '|'
        custom_dialect.lineterminator = '\n'
        csv.register_dialect(PROJECT_NAME, custom_dialect)

    def import_deck(self) -> List[Card]:
        with open(self.file_path, newline='') as file:
            input_reader = csv.reader(file, PROJECT_NAME)
            return [Card.from_str_list(row) for row in input_reader]

    def export_deck(self, cards: List[Card]):
        with open(self.file_path, 'w', newline='') as file:
            output_writer = csv.writer(file, PROJECT_NAME)
            for card in cards:
                output_writer.writerow(card.to_str_list())
