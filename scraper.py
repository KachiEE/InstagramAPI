import requests
import json
import time
from bs4 import BeautifulSoup as BS


class InstaSpider():
    base_url = 'https://instagram.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    data = []

    def __init__(self, username):
        '''
        username: list of strings
        '''
        self.username = username

    def fetch(self):
        user_url = []
        for each in self.username:
            user = self.base_url + each
            user_url.append(user)

        responses = []
        for each in user_url:
            try:
                response = requests.get(each, headers=self.headers)
                responses.append(response)
            except:
                responses.append(f'{each} can not be reached')
            time.sleep(3)
        return responses

    def parse(self, responses):
        profiles = []

        # Data Extraction logic
        for response in responses:
            try:
                soup = BS(response.text, 'html.parser')
                scripts = soup.find_all('script')        
                script = scripts[4]
                
                script_text = script.contents[0]
                data = script_text[script_text.find('{"config"') : -1]
                data = json.loads(data.strip())
                user_data = data['entry_data']['ProfilePage'][0]['graphql']['user']

                profile = {
                    'username': user_data['username'],
                    'full_name': user_data['full_name'],
                    'post_count': user_data['edge_owner_to_timeline_media']['count'],
                    'followers': user_data['edge_followed_by']['count'],
                    'following': user_data['edge_follow']['count'],
                }
                profiles.append(profile)
            except:
                profiles.append({'not found': f'info from {response.url} not found'})
        return profiles

    def run(self):
        responses = self.fetch()
        profiles = self.parse(responses)
        return profiles
