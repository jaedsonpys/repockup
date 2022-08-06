import os
import shutil
from typing import Union

import requests

GITHUB_API = 'https://api.github.com/search/repositories'
REPO_PER_PAGE = 1000


class Repockup(object):
    def __init__(self, username: str, api_token: str = None) -> None:
        self._api_token = api_token
        self._username = username

    def _get_repositories(self) -> Union[list, None]:
        result = None

        headers = {
            'Authorization': f'token {self._api_token}'
        }

        user_url = f'{GITHUB_API}?q=user:{self._username}&per_page={REPO_PER_PAGE}'
        req = requests.get(user_url, headers=headers)

        if req.status_code == 200:
            result =  req.json()
        
        return result
