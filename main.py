from urllib3 import disable_warnings
from modules.configs import *
from modules.explorer import Explorer
from modules.post_scraper import Post
from modules.recorder import Recorder
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

    # check if categories and districts are valid
    check_category(category)
    check_districts(districts, city)

    recorder = Recorder('test1.csv')  # Recorder object init

    probe = Explorer(category, districts, city)  # Explorer object init

    tokens = probe.explore(request_sleep=1, token_limit=100)  # Explorer object extracts tokens
    print('\ntoken extraction complete. initiating data scraping... \n\n')
    for token in tokens:
        print(f"Scraping post {token}...")
        post = Post(token)
        done = post.scrape(AUTH)
        if done:
            print(f"title: {post.persian_title}. extraction complete. Recording...\n")
            recorder.record(post)

        else:
            print("Extraction failed. logged in post_scraper.log")
        time.sleep(1)
    recorder.flush()  # to commit any remaining posts


if __name__ == "__main__":
    # disables unnecessary warnings
    disable_warnings()
    main()
