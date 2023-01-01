from typing import List

from core.util import StatusOr
from lookup.wiktionary.language_support.abstract import WiktionaryLocaleParser
from lookup.wiktionary.web_requests import request_articles


class GermanLocaleParser(WiktionaryLocaleParser):
    @classmethod
    def get_articles_list(cls, text: str) -> StatusOr[List[str]]:
        articles_status = request_articles(text, 'de')
        if articles_status.is_ok():
            print(articles_status.value)
        else:
            print(articles_status.status)
        return StatusOr(status='Not Implemented')
