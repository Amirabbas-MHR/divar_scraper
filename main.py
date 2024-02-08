import requests
from urllib3 import disable_warnings
from time import sleep, time_ns
import json
import re


def check_category(category):
    # check if category is valid
    if category not in VALID_CATEGORIES:
        raise Exception(
            f"Wrong category name: '{category}', category should be in the {CATEGORY_FILE_PATH} file.")


def check_districts(districts, city):
    # check if districts are valid
    for enum in districts:
        if enum not in VALID_ENUMS:
            # TODO checking for other cities enums should be added. now only tehran is supported all over the code
            raise Exception(
                f"Wrong enum: '{enum}' , enum should be in the {ENUMS_FILE_PATH} for city {city}")


def main():
    category = 'guitar-bass-amplifier'
    districts = ['61', '54', '55', '56']
    city = 'tehran'

    check_category(category)
    check_districts(districts, city)


if __name__ == "__main__":
    # disables unnecessary warnings
    disable_warnings()

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
    main()
