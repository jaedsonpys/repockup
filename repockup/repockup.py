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

    def _get_repositories(self) -> list:
        repositories = []

        if self._api_token:
            headers = {'Authorization': f'token {self._api_token}'}

        user_url = f'{GITHUB_API}?q=user:{self._username}&per_page={REPO_PER_PAGE}'
        req = requests.get(user_url, headers=headers)

        if req.status_code == 200:
            result = req.json()
            items = result.get('items')

            for repo in items:
                repositories.append({
                    'name': repo['name'],
                    'pushed_at': repo['pushed_at'],
                    'clone_url': repo['ssh_url']
                })

        return repositories

    def _get_repo_json(self) -> list:
        if os.path.isfile(self._repo_json):
            with open(self._repo_json, 'r') as reader:
                repo_json = json.load(reader)
        else:
            repo_json  = []
        
        return repo_json

    def _add_repo_json(self, data: list) -> None:
        with open(self._repo_json, 'w') as writer:
            json.dump(data, writer, indent=4, ensure_ascii=False)
