import os
import json
import shutil
from typing import Union

import requests

GITHUB_API = 'https://api.github.com/search/repositories'
REPO_PER_PAGE = 100


class Repockup(object):
    def __init__(self, username: str, api_token: str = None) -> None:
        self._api_token = api_token
        self._username = username

        home_user = os.getenv('HOME')
        self._repo_json = os.path.join(home_user, 'repockup.json')

    def _get_repositories(self) -> dict:
        repositories = {}

        headers = {
            'Authorization': f'token {self._api_token}'
        }

        user_url = f'{GITHUB_API}?q=user:{self._username}&per_page={REPO_PER_PAGE}'
        req = requests.get(user_url, headers=headers)

        if req.status_code == 200:
            result = req.json()
            items = result.get('items')

            for repo in items:
                repo_data = {
                    'pushed_at': repo['pushed_at'],
                    'clone_url': repo['ssh_url']
                }
                
                repositories[repo['name']] = repo_data

        return repositories
