from typing import List

from lookup.wiktionary.languages.base import WiktionaryLocalizedParser


class GermanLocaleParser(WiktionaryLocalizedParser):
    @classmethod
    def translation_language_codes(cls) -> List[str]:
        return ['de']
