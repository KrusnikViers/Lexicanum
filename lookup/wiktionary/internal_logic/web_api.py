import json
import pprint
from typing import List

import requests

from core.util import StatusOr, Status

_COMMON_PARAMS = {
    'format': 'json',
    'formatversion': 2  # https://www.mediawiki.org/wiki/API:JSON_version_2
}

_RELEVANT_ARTICLE_TITLES_FETCH_COUNT = 3


class WebArticle:
    def __init__(self, title: str, page_id: int, content: str):
        self.title = title
        self.page_id = page_id
        self.content = content

    def __str__(self):
        return '{}:{}\n{}'.format(self.page_id, self.title, self.content[:100] + '...')


def _endpoint_url(locale: str):
    return 'https://{}.wiktionary.org/w/api.php'.format(locale)


def _error_by_request_status_code(text: str, locale: str, response: requests.Response) -> Status | None:
    if response.status_code == 404:
        return Status('Nothing found for \'{}\'({})'.format(text, locale))
    if response.status_code != 200:
        print('Failed: {}\nRequest to {} failed:\n{}'.format(response.status_code,
                                                             pprint.pformat(response.request.url),
                                                             response.text))
        return Status('Request failed for \'{}\'({}): {}'.format(text, locale, response.status_code))
    return None


def search_articles(search_text: str, endpoint_language_code: str) -> StatusOr[List[WebArticle]]:
    params = _COMMON_PARAMS | {
        'search': search_text.lower(),
        'action': 'opensearch',
        'profile': 'fuzzy',
        'redirects': 'resolve',
        'limit': _RELEVANT_ARTICLE_TITLES_FETCH_COUNT
    }
    result = requests.get(_endpoint_url(endpoint_language_code), params=params)
    if errcode := _error_by_request_status_code(search_text, endpoint_language_code, result):
        return StatusOr.from_pure(errcode)

    parsed_response = json.loads(result.text)
    return retrieve_articles(parsed_response[1], endpoint_language_code)


def retrieve_articles(titles: List[str], endpoint_language_code: str) -> StatusOr[List[WebArticle]]:
    if not titles:
        return StatusOr(value=[])

    params = _COMMON_PARAMS | {
        'action': 'query',
        'prop': 'revisions',
        'rvslots': '*',
        'rvprop': 'content',
        'redirects': '1',
        'titles': '|'.join(titles),
    }
    result = requests.get(url=_endpoint_url(endpoint_language_code), params=params)
    if errcode := _error_by_request_status_code(', '.join(titles), endpoint_language_code, result):
        return StatusOr.from_pure(errcode)
    parsed_response = json.loads(result.text)
    meaningful_pages = [page for page in parsed_response['query']['pages'] if
                        'missing' not in page and
                        'title' in page and 'pageid' in page and 'revisions' in page]
    return StatusOr(value=[WebArticle(page['title'],
                                      page['pageid'],
                                      content=page['revisions'][0]['slots']['main']['content'])
                           for page in meaningful_pages])
