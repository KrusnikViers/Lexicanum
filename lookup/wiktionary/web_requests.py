import json
import pprint
from typing import List

import requests

from core.util import StatusOr

_COMMON_PARAMS = {
    'format': 'json',
    'formatversion': 2  # https://www.mediawiki.org/wiki/API:JSON_version_2
}


def request_articles(text: str, locale: str) -> StatusOr[List[str]]:
    url = 'https://{}.wiktionary.org/w/api.php'.format(locale)
    params = _COMMON_PARAMS | {
        'action': 'query',
        'prop': 'revisions',
        'rvslots': '*',
        'rvprop': 'content',
        'redirects': '1',
        'titles': text,
    }

    result = requests.get(url=url, params=params)
    if result.status_code != 200:
        print('Failed: {}\nRequest to {} with params {} failed:\n{}'.format(result.status_code,
                                                                            url, pprint.pformat(params),
                                                                            result.text))
        return StatusOr(status='Failed to get wiki articles for {}: {}'.format(text, result.status_code))
    print(pprint.pformat(json.loads(result.text), indent=1))
    return StatusOr(value=[result.text])
