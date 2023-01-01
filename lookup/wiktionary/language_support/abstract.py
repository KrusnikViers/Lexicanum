from typing import List

from core.util import StatusOr


class WiktionaryLocaleParser:
    @classmethod
    def get_articles_list(cls, text: str) -> StatusOr[List[str]]:
        raise NotImplementedError
