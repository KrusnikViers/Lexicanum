from typing import List

from core.util import StatusOr
from lookup.wiktionary.internal.markup import WikitextContentNode, build_tree_from_wiki_page_content
from lookup.wiktionary.internal.web_api import fetch_matching_articles, fetch_articles


def fetch_and_parse_matching_articles(search_text: str, locale: str) -> StatusOr[List[WikitextContentNode]]:
    raw_articles = fetch_matching_articles(search_text, locale=locale)
    if not raw_articles.is_ok():
        return raw_articles.to_other()
    return StatusOr(
        value=[build_tree_from_wiki_page_content(raw_article.content, raw_article.title)
               for raw_article in raw_articles.value])


def fetch_and_parse_articles(titles: List[str], locale: str) -> StatusOr[List[WikitextContentNode]]:
    raw_articles = fetch_articles(titles, locale=locale)
    if not raw_articles.is_ok():
        return raw_articles.to_other()
    return StatusOr(
        value=[build_tree_from_wiki_page_content(raw_article.content, raw_article.title)
               for raw_article in raw_articles.value])
