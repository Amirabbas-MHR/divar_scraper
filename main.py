from urllib3 import disable_warnings
from modules.configs import *
from modules.explorer import Explorer
from modules.post_scraper import Post
from modules.recorder import Recorder
from modules.logger import Logger
from time import sleep

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

    logger = Logger()  # initializing logger
    logger.info(f"logger initialized. logging in {logger.log_file}", __name__)

    # check if categories and districts are valid
    check_category(category)
    check_districts(districts, city)

    record_file = "test1.csv"
    recorder = Recorder(logger, record_file)  # Recorder object init
    logger.info(f"recorder initialized. recording in {record_file}", __name__)

    probe = Explorer(logger, category, districts, city)  # Explorer object init
    logger.info(f"explorer initialized. searching in {category} - {city}: {districts}", __name__)

    logger.info(f"Initiating token extraction.", __name__)
    tokens = probe.explore(request_sleep=1, token_limit=10)  # Explorer object extracts tokens
    logger.info(f"token extraction complete. a total of {len(tokens)} tokens extracted.", __name__)

    for token in tokens:
        # TODO add the scraping post 10/120 or 15/120 or ... loading
        print(f"Scraping post {token}...")
        post = Post(logger, token)
        done = post.scrape(AUTH)

        if done:
            print(f"title: {post.persian_title}. extraction complete. Recording...\n")
            recorder.record(post)
        else:
            print(f"post {token} scraping failed. check post_scraper logs.")

        sleep(1)

    recorder.flush()  # to commit any remaining posts


if __name__ == "__main__":
    # disables unnecessary warnings
    disable_warnings()
    main()
