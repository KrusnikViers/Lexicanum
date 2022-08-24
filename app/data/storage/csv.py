import csv
from pathlib import Path
from typing import List, Optional

from app.data.card import Card
from app.info import PROJECT_NAME


class CSVWrapper:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.resolve()

    # This method should be called only once per program run, before any import or export calls are made.
    @staticmethod
    def register_dialect():
        custom_dialect = csv.Dialect
        custom_dialect.quoting = csv.QUOTE_MINIMAL
        custom_dialect.quotechar = '`'
        custom_dialect.delimiter = '|'
        custom_dialect.lineterminator = '\n'
        custom_dialect.escapechar = '\\'
        csv.register_dialect(PROJECT_NAME, custom_dialect)

    def import_deck(self) -> Optional[List[Card]]:
        try:
            with open(self.file_path, newline='') as file:
                input_reader = csv.reader(file, PROJECT_NAME)
                return [Card.from_str_list(row) for row in input_reader]
        except FileNotFoundError:
            return None

    def export_deck(self, cards: List[Card]):
        with open(self.file_path, 'w', newline='') as file:
            output_writer = csv.writer(file, PROJECT_NAME)
            for card in cards:
                output_writer.writerow(card.to_str_list())
