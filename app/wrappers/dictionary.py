import os

import requests

from app.data.language import Language

_API_BASE_URI = 'https://dictionary.yandex.net/api/v1/dicservice.json'
_API_CLIENT_KEY = 'Yandex.Dictionary API key'

# This section is to prevent storing confidential API key in the repo. To make application use the actual key, set it
# to `YD_API_KEY` environment variable before running the program.
if actual_key := os.environ.get('YD_API_KEY'):
    _API_CLIENT_KEY = actual_key


# Receives word for translation and its language. Returns raw(!) json from external dictionary service.
def get_raw_translations_list(word: str, source_language: Language) -> str:
    language_pair = 'en-de' if source_language == Language.EN else 'de-en'
    return requests.get(url='{}/{}'.format(_API_BASE_URI, 'lookup'), params={
        'key': _API_CLIENT_KEY,
        'lang': language_pair,
        'text': word
    }).text
