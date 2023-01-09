import json
import pprint
from typing import List

import requests

from core.util import StatusOr, Status

_COMMON_PARAMS = {
    'format': 'json',
    'formatversion': 2  # https://www.mediawiki.org/wiki/API:JSON_version_2
}

_RELEVANT_ARTICLE_TITLES_FETCH_COUNT = 2


class RawWiktionaryArticle:
    def __init__(self, title: str, page_id: int, content: str):
        self.title = title
        self.page_id = page_id
        self.content = content

    def __str__(self):
        return '{}:{}\n{}'.format(self.page_id, self.title, self.content[:100] + '...')


def _localized_endpoint(locale: str):
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


def fetch_matching_articles(search_text: str, locale: str) -> StatusOr[List[RawWiktionaryArticle]]:
    params = _COMMON_PARAMS | {
        'search': search_text.lower(),
        'action': 'opensearch',
        'profile': 'fuzzy',
        'redirects': 'resolve',
        'limit': _RELEVANT_ARTICLE_TITLES_FETCH_COUNT
    }
    result = requests.get(_localized_endpoint(locale), params=params)
    if errcode := _error_by_request_status_code(search_text, locale, result):
        return StatusOr.from_pure(errcode)

    parsed_response = json.loads(result.text)
    return fetch_articles(parsed_response[1], locale)


def fetch_articles(titles: List[str], locale: str) -> StatusOr[List[RawWiktionaryArticle]]:
    params = _COMMON_PARAMS | {
        'action': 'query',
        'prop': 'revisions',
        'rvslots': '*',
        'rvprop': 'content',
        'redirects': '1',
        'titles': '|'.join(titles),
    }
    result = requests.get(url=_localized_endpoint(locale), params=params)
    if errcode := _error_by_request_status_code(', '.join(titles), locale, result):
        return StatusOr.from_pure(errcode)
    parsed_response = json.loads(result.text)
    return StatusOr(value=[RawWiktionaryArticle(page['title'],
                                                page['pageid'],
                                                content=page['revisions'][0]['slots']['main']['content'])
                           for page in parsed_response['query']['pages']])
