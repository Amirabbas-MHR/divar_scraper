import requests
from dataclasses import dataclass


@dataclass
class Post:
    token: str
    persian_district: str = None
    category: str = None
    phone_number: str = None
    persian_title: str = None
    persian_subtitle: str = None
    persian_description: str = None
    url: str = None
    location: tuple = None
    is_business: bool = False
    business_data: list = None
    parent_category: str = None
    gparent_category: str = None
    city: str = None
    price: int = None
    persian_category: str = None
    persian_city: str = None

    def __get_phone_number(self, auth_key):
        base_url = 'https://api.divar.ir/v8/postcontact/web/contact_info/'

        headers = {
            'authority': 'api.divar.ir',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': f'Basic {auth_key}',
            'origin': 'https://divar.ir',
            'priority': 'u=1, i',
            'referer': 'https://divar.ir/',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.6099.216 Safari/537.36',
        }
        url = base_url + self.token
        response = requests.get(url, headers=headers, verify=False)
        json_data = response.json()
        if response.status_code == 200:
            try:
                self.phone_number = json_data['widget_list'][0]['data']['action']['payload']['phone_number']
                print(f"Post with token {self.token}: {self.phone_number}")
            except:
                print(f"Post with token {self.token} has hidden number.")
        elif response.status_code == 401:
            print("Authorization key expired/incorrect.")
        else:
            print(f"Unknown error occoured with code {response.status_code}: {response.text}")

    def scrape(self, auth_key=None, get_phone_number=True) -> bool:
        if get_phone_number and auth_key is None:
            raise Exception("Please provide an auth key if get_phone_number is True")

        headers = {
            'authority': 'api.divar.ir',
            'accept': 'application/json-filled',
            'accept-language': 'en-US,en;q=0.9',
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

        response = requests.get(f'https://api.divar.ir/v8/posts-v2/web/{self.token}', headers=headers)
        self.url = response.url

        if response.status_code != 200:
            with open('post_scraper.log', 'a') as file:
                file.write(f"request to {response.url} failed with {response.status_code} code. "
                           f"with text: {response.text} \n")
                return False
            # raise Exception(f"request to {response.url} failed with {response.status_code} code.")

        data = response.json()

        # sections stuff
        sections = data['sections']
        for section in sections:
            if section['section_name'] == "TITLE":
                self.persian_title = section['widgets'][0]['data']['title']
                self.persian_subtitle = section['widgets'][0]['data']['subtitle']
                continue

            if section['section_name'] == 'DESCRIPTION':
                self.persian_description = section['widgets'][1]['data']['text']
                continue

            if section['section_name'] == 'MAP':
                lat = section['widgets'][0]['data']['location']['exact_data']['point']['latitude']
                long = section['widgets'][0]['data']['location']['exact_data']['point']['longitude']
                self.location = (lat, long)
                continue

            if section['section_name'] == 'BUSINESS_SECTION':
                self.is_business = True
                self.business_data = []
                for widget in section['widgets']:
                    try:
                        self.business_data.append(widget['data']['title'])
                    except:
                        pass
                    try:
                        self.business_data.append(widget['data']['text'])
                    except:
                        pass

        # webengage stuff
        self.category = data['webengage']['category']
        self.parent_category = data['webengage']['cat_2']
        self.gparent_category = data['webengage']['cat_1']
        self.city = data['webengage']['city']
        self.price = data['webengage']['price']

        # seo stuff
        self.persian_category = data['seo']['web_info']['category_slug_persian']
        self.persian_district = data['seo']['web_info']['district_persian']
        self.persian_city = data['seo']['web_info']['city_persian']

        if get_phone_number:
            self.__get_phone_number(auth_key)

        return True
