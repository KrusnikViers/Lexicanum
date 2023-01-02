from typing import List

from core.util import StatusOr
from lookup.wiktionary import web_api
from lookup.wiktionary.language_support.abstract import WiktionaryLocaleParser, WiktionaryArticle
from lookup.wiktionary.web_api import RequestedArticle


class EnglishLocaleParser(WiktionaryLocaleParser):

    @classmethod
    def parse_raw_article(cls, web_article: web_api.RequestedArticle) -> List[WiktionaryArticle]:
        print('Parse called for {}'.format(web_article))
        return []

    @classmethod
    def get_articles_for(cls, search_text: str) -> StatusOr[List[RequestedArticle]]:
        return web_api.request_article(search_text, locale='en')
