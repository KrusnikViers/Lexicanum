from typing import List

from core.util import StatusOr
from lookup.wiktionary.internal.markup import WikitextTreeNode, build_tree_from_markup
from lookup.wiktionary.internal.web_api import fetch_matching_articles


def fetch_structured_articles(search_text: str, locale: str) -> StatusOr[List[WikitextTreeNode]]:
    raw_articles = fetch_matching_articles(search_text, locale=locale)
    if not raw_articles.is_ok():
        return raw_articles.to_other()
    return StatusOr(
        value=[build_tree_from_markup(raw_article.content, raw_article.title) for raw_article in raw_articles.value])
