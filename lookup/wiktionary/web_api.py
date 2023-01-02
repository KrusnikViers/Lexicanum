import json
import pprint
from typing import List

import requests

from core.util import StatusOr

_COMMON_PARAMS = {
    'format': 'json',
    'formatversion': 2  # https://www.mediawiki.org/wiki/API:JSON_version_2
}


class RequestedArticle:
    def __init__(self, title: str, page_id: int, content: str):
        self.title = title
        self.page_id = page_id
        self.content = content


def request_article(search_text: str, locale: str) -> StatusOr[List[RequestedArticle]]:
    url = 'https://{}.wiktionary.org/w/api.php'.format(locale)
    params = _COMMON_PARAMS | {
        'action': 'query',
        'prop': 'revisions',
        'rvslots': '*',
        'rvprop': 'content',
        'redirects': '1',
        'titles': search_text,
    }

    result = requests.get(url=url, params=params)
    if result.status_code == 404:
        return StatusOr(status='No articles found for {}:\'{}\''.format(locale, search_text))
    if result.status_code != 200:
        print('Failed: {}\nRequest to {} with params {} failed:\n{}'.format(result.status_code,
                                                                            url, pprint.pformat(params),
                                                                            result.text))
        return StatusOr(status='Request failed for {}:\'{}\':{}'.format(locale, search_text, result.status_code))

    parsed_response = json.loads(result.text)
    parsed_pages: List[RequestedArticle] = []
    for page in parsed_response['query']['pages']:
        parsed_pages.append(RequestedArticle(page['title'], page['pageid'],
                                             content=page['revisions'][0]['slots']['main']['content']))
    return StatusOr(value=parsed_pages)
