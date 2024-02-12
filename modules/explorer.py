import requests
from time import sleep, time
import re
from .configs import *


class Explorer:
    def __init__(self, logger, category: str, districts: list, city='tehran', ):
        """
        Explorer object. Handles methods on exploring and extracting data.

        :param logger: Logger object to trigger logging
        :param category: category name of posts. the acceptable list is in categories.json
        :param districts: list of enums . which is a code for divar for each district. go to tehran.json to read the enums
        :param city: tehran is ONLY supported now #TODO check the readme.txt for the problem of other cities.
        """

        self.city = city
        self.districts = districts
        self.category = category
        self.logger = logger

    def __initial_lastPostDate(self) -> int:
        """

        :return: lastPotDate from the initial get request to divar.ir, used internallhy to get pages of posts
        """
        _cookies = {
            'did': '80dce4fa-1571-4f8b-b8ec-986b57261433',
            'multi-city': 'tehran%7C',
            'city': 'tehran',
            'token': '',
            'chat_opened': '',
            'sessionid': '',
            'FEATURE_FLAG': '%7B%22flags%22%3A%7B%22search_bookmark_enabled_web_side%22%3A%7B%22name%22%3A'
                            '%22search_bookmark_enabled_web_side%22%2C%22bool_value%22%3Atrue%2C%22routeLabels%22%3A%5B'
                            '%22browse%22%5D%7D%2C%22search_page_empty_state_web_server_side_enabled%22%3A%7B%22name%22'
                            '%3A%22search_page_empty_state_web_server_side_enabled%22%2C%22bool_value%22%3Afalse%7D%2C'
                            '%22ENGAGED_USER_SHOW_LOAD_MORE_EXPERIMENT%22%3A%7B%22name%22%3A'
                            '%22ENGAGED_USER_SHOW_LOAD_MORE_EXPERIMENT%22%2C%22bool_value%22%3Afalse%7D%2C'
                            '%22WEB_REQUEST_WITH_TOKEN_ENABLED%22%3A%7B%22name%22%3A%22WEB_REQUEST_WITH_TOKEN_ENABLED'
                            '%22'
                            '%2C%22bool_value%22%3Afalse%7D%7D%2C%22evaluatedAt%22%3A%222024-02-07T18%3A16%3A04'
                            '.491212032Z%22%2C%22maximumCacheUsageSecondsOnError%22%3A86400%2C'
                            '%22minimumRefetchIntervalSeconds%22%3A3600%2C%22expireDate%22%3A1707333364492%7D',
        }

        _headers = {
            'authority': 'divar.ir',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.6',
            'cache-control': 'max-age=0',
            'if-none-match': 'W/"7ccfc-K4zLTU21yMgtiilnlqtlBH8Sjok"',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'service-worker-navigation-preload': 'true',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
                          'Safari/537.36',
        }

        _params = {
            'goods-business-type': 'all',
        }

        response = requests.get(f'https://divar.ir/s/tehran/{URI_SCHEMA[self.category][0]}', params=_params,
                                cookies=_cookies,
                                headers=_headers).text

        # Extracting the initial lastPostDate
        pattern = r'"lastPostDate":\s*(\d+)'

        # Search for the pattern in the response html string
        match = re.search(pattern, response)

        # If match found, return the lastPostDate
        if match:
            self.initial_lastPostDate = match.group(1)
            self.logger.info(f"Initial lastPostDate extraction successful: {self.initial_lastPostDate}", __name__)
            return int(self.initial_lastPostDate)

        # If the match is not found, error will be raised and response is saved in error_file_path
        error_file_path = f"{LOGS_PATH}/{time()}-lastPostDateError.txt"  # inserting the unix time stamp to clearify
        self.logger.fatal(f"Could not find the initial 'lastPostDate'. request response is logged in "
                          f"lastPostDateError.txt", __name__)
        with open(error_file_path, 'w') as file:
            file.write(response)
        raise Exception(
            f"Could not find the initial lastPostDate. logged the initial request response in {error_file_path}")

    def explore(self, request_sleep: int = 1, token_limit: int = 100) -> list[str]:
        """
        gets the available post tokens in the given category, city and districts.

        :param request_sleep: cooldown time between requests to api.divar.ir to prevent IP ban problems
        :param token_limit: maximum number of tokens before ending the exploration
        :return: a list of tokens
        """
        cookies = {
            'did': '80dce4fa-1571-4f8b-b8ec-986b57261433',
            'multi-city': 'tehran%7C',
            'city': 'tehran',
            'token': '',
            'chat_opened': '',
            'sessionid': '',
            'FEATURE_FLAG': '%7B%22flags%22%3A%7B%22search_bookmark_enabled_web_side%22%3A%7B%22name%22%3A'
                            '%22search_bookmark_enabled_web_side%22%2C%22bool_value%22%3Atrue%2C%22routeLabels%22%3A'
                            '%5B%22browse%22%5D%7D%2C%22search_page_empty_state_web_server_side_enabled%22%3A%7B'
                            '%22name%22%3A%22search_page_empty_state_web_server_side_enabled%22%2C%22bool_value%22'
                            '%3Afalse%7D%2C%22ENGAGED_USER_SHOW_LOAD_MORE_EXPERIMENT%22%3A%7B%22name%22%3A'
                            '%22ENGAGED_USER_SHOW_LOAD_MORE_EXPERIMENT%22%2C%22bool_value%22%3Afalse%7D%2C'
                            '%22WEB_REQUEST_WITH_TOKEN_ENABLED%22%3A%7B%22name%22%3A%22WEB_REQUEST_WITH_TOKEN_ENABLED'
                            '%22%2C%22bool_value%22%3Afalse%7D%7D%2C%22evaluatedAt%22%3A%222024-02-08T00%3A03%3A43'
                            '.517673852Z%22%2C%22maximumCacheUsageSecondsOnError%22%3A86400%2C'
                            '%22minimumRefetchIntervalSeconds%22%3A3600%2C%22expireDate%22%3A1707354223515%7D',
        }

        headers = {
            'authority': 'api.divar.ir',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.6',
            'content-type': 'application/json',
            'origin': 'https://divar.ir',
            'referer': 'https://divar.ir/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 '
                          'Safari/537.36',
        }

        persian_districts = [distr['enumName'] for distr in nears if (distr['enum'] in self.districts)]
        print("Initiating...\n")
        print(f"\n Extracting tokens of {self.category} category, from districts {persian_districts} in {self.city}")

        # Everything is on routine, except the parameter 'last_post_date'
        # To handle that, only for the page 1, we need to set it as 'initial_lastPostDate'
        # Which is for some reason sent to the client with a simple get request \
        # (done in self.__initial_lastPostDate function)
        # But for pages > 1:
        # last_post_date should be set equal to last_post_date of the previous page.
        # so where do we get this 'last_post_date'? it is received in fetch request response of each page,
        # in address of response['last_post_date']
        # not so easy, but here is the code:

        self.__initial_lastPostDate()  # getting the initial lastPostDate from the get request
        last_post_date = self.initial_lastPostDate  # initially set to initial lastPostDate

        target_tokens = []  # a list containing all extracted tokens
        page = 1  # page counter

        while len(target_tokens) <= token_limit:
            print(f"\npage {page}")

            json_data = {
                'page': page,
                'json_schema': {
                    'category': {
                        'value': self.category
                    },
                    'districts': {
                        'vacancies': self.districts
                    },
                    'sort': {
                        'value': 'sort_date',
                    },
                },
                'last-post-date': int(last_post_date),
            }
            # TODO the url should be changed based on the input city.
            response = requests.post(
                f'https://api.divar.ir/v8/web-search/1/{self.category}',
                cookies=cookies,
                headers=headers,
                json=json_data,
            )
            # check if request was successful
            if response.status_code != 200:
                error_file_path = f"{LOGS_PATH}/{time()}-getPostsPageError.txt"  # inserting the unix time stamp to  clearify
                log.fatal(
                    f"getting posts page failed with code {response.status_code}. response in: {error_file_path}")
                with open(error_file_path, 'w') as file:
                    file.write(response.text)
                # TODO should this be raise an exception or just handle it another way?
                raise Exception(
                    f"Request to {response.url} failed. Response recorded {error_file_path}")

            result_json = response.json()['web_widgets']['post_list']

            last_post_date = response.json()[
                'last_post_date']  # here we use the received last_post_date as the next page's param
            page_tokens = []

            for post in result_json:
                # token can be used to access the post using https://divar.ir/v/<token> where all the information lies.
                token = post['data']['action']['payload']['token']
                # If a token is extracted twice, it means we are passing the lastPostDate incorrectly
                if token in target_tokens:
                    self.logger.fatal(f"Token <{token}> is extracted twice.", __name__)
                    raise Exception(f"Token <{token}> is extracted twice. There seems to be a problem with pages"
                                    " or last_post_update parameter...")
                self.logger.info(f"Token <{token}> extracted.", __name__)
                print(f"token {token} extracted.")
                page_tokens.append(token)

            target_tokens += page_tokens
            if len(page_tokens) < 24:
                # it means the page is not full, so next page does not exist (a full page in divar, contains 24 posts)
                break
            sleep(request_sleep)
            page += 1
        print(f"\ntoken extraction complete. a total of {len(target_tokens)} tokens extracted.")
        return target_tokens
