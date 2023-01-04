from typing import List

from core.util import StatusOr
from lookup.wiktionary import web_api
from lookup.wiktionary.language_support.abstract import WiktionaryLocaleParser, WiktionaryArticle
from lookup.wiktionary.web_api import RequestedArticle
import mwparserfromhell as mwp


class EnglishLocaleParser(WiktionaryLocaleParser):

    @classmethod
    def parse_raw_article(cls, web_article: web_api.RequestedArticle) -> List[WiktionaryArticle]:
        parsed_article = mwp.parse(web_article.content)
        print('Parse called for {}'.format(web_article))

        return []

    @classmethod
    def get_articles_for(cls, search_text: str) -> StatusOr[List[WiktionaryArticle]]:
        web_articles = web_api.search_articles(search_text, locale='en')
        if not web_articles.is_ok():
            return web_articles.to_other()
        parsed_articles = [parsed_article for web_article in web_articles.value
                           for parsed_article in cls.parse_raw_article(web_article)]
        return StatusOr(status='Not implemented')
