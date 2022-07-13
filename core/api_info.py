API_BASE_URI = 'https://dictionary.yandex.net/api/v1/dicservice.json'

API_CLIENT_KEY = None
# TODO: Replace
if API_CLIENT_KEY is None:
    with open('api_key.txt', 'r') as api_key_file:
        API_CLIENT_KEY = api_key_file.readline().strip()
    print('API_CLIENT_KEY read from file: {}..{}'.format(API_CLIENT_KEY[:4], API_CLIENT_KEY[-4:]))
