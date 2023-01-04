from typing import List

from core.util import StatusOr
from lookup.wiktionary.web_api import RequestedArticle


class WiktionaryArticle:
    def __init__(self, title: str, see_also: List[str]):
        self.title = title


class WiktionaryLocaleParser:
    @classmethod
    def parse_raw_article(cls, raw_article: str) -> List[WiktionaryArticle]:
        raise NotImplementedError

    @classmethod
    def get_articles_for(cls, search_text: str) -> StatusOr[List[RequestedArticle]]:
        raise NotImplementedError
