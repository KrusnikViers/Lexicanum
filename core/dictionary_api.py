import os

import requests

from core.card import Language

API_BASE_URI = 'https://dictionary.yandex.net/api/v1/dicservice.json'
API_CLIENT_KEY = 'Yandex.Dictionary API key'

# This section is to prevent storing confidential API key in the repo. To make application use the actual key, set it
# to `YD_API_KEY` environment variable before running the program.
if actual_key := os.environ.get('YD_API_KEY'):
    API_CLIENT_KEY = actual_key


def request_translations(word: str, source_language: Language) -> str:
    return requests.get(url='{}/{}'.format(API_BASE_URI, 'lookup'), params={
        'key': API_CLIENT_KEY,
        'lang': 'en-de' if source_language == Language.EN else 'de-en',
        'text': word
    }).text
