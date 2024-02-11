import json

# loading valid categories list
CATEGORY_FILE_PATH = 'config/categories.json'
with open(CATEGORY_FILE_PATH, 'r') as category_file:
    VALID_CATEGORIES = json.load(category_file)['categories']

# loading valid enums list
ENUMS_FILE_PATH = 'config/tehran.json'
with open(ENUMS_FILE_PATH, 'r') as enums_file:
    nears = json.load(enums_file)['nears']
    VALID_ENUMS = [near['enum'] for near in nears]

# loading the mapper of category name to it's uri, used to send the initial get request
URI_SCHEME_FILE_PATH = 'config/uri_scheme.json'
with open(URI_SCHEME_FILE_PATH, 'r') as uri_scheme_file:
    URI_SCHEMA = json.load(uri_scheme_file)['urischema']['display']

SECRET_PATH = 'config/secret.txt'
with open(SECRET_PATH, 'r') as secret_file:
    AUTH = secret_file.read()

RECORDS_PATH = 'records/'
LOGS_PATH = 'logs/'
