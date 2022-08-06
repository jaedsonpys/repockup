import json
import os
import shutil
import subprocess
from threading import Thread
from typing import Union

import requests

GITHUB_API = 'https://api.github.com/search/repositories'
REPO_PER_PAGE = 100


class Repockup(object):
    def __init__(
        self,
        username: str,
        dest_dir: str,
        api_token: str = None
    ) -> None:
        self._username = username
        self._dest_dir = dest_dir
        self._api_token = api_token

        home_user = os.getenv('HOME')
        self._repo_json = os.path.join(home_user, 'repockup.json')
        self._repo_temp = os.path.join(home_user, 'repockup_temp')

        if not os.path.isdir(self._repo_temp):
            os.mkdir(self._repo_temp)
        else:
            shutil.rmtree(self._repo_temp, ignore_errors=True)
            os.mkdir(self._repo_temp)

    def _get_repositories(self) -> list:
        repositories = []

        if self._api_token:
            headers = {'Authorization': f'token {self._api_token}'}

        page = 1

        while True:
            user_url = f'{GITHUB_API}?q=user:{self._username}&per_page={REPO_PER_PAGE}&page={page}'
            req = requests.get(user_url, headers=headers)

            page += 1

            if req.status_code == 200:
                result = req.json()
                items = result.get('items')

                if items:
                    for repo in items:
                        repositories.append({
                            'name': repo['name'],
                            'pushed_at': repo['pushed_at'],
                            'clone_url': repo['ssh_url']
                        })
                else:
                    break

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

    def _split_repositories(self, repositories: list) -> list:
        num = int(len(repositories) / 4)
        split_list = [repositories[i:i + num] for i in range(0, len(num), num)]
        return split_list
