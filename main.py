from urllib3 import disable_warnings
from modules.configs import *
from modules.explorer import Explorer
from modules.post_scraper import Post
import time


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
    category = 'furniture-wood'
    districts = ['61', '54', '55', '56']
    city = 'tehran'

    check_category(category)
    check_districts(districts, city)

    probe = Explorer(category, districts, city)
    tokens = probe.explore(request_sleep=2, token_limit=47)
    print('\ntoken extraction complete. initiating data scraping... \n\n')
    dataclasses = []
    for token in tokens:
        print(f"Scraping post {token}...")
        post = Post(token)
        done = post.scrape()
        if done:
            print(f"title: {post.persian_title}. extraction complete. sleeping...\n")
            dataclasses.append(post)
        else:
            print("Extraction failed. logged in post_scraper.log")
        time.sleep(2)


if __name__ == "__main__":
    # disables unnecessary warnings
    disable_warnings()

    main()
