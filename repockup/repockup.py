import json
import os
import shutil
import subprocess
from threading import Thread

import requests

GITHUB_API = 'https://api.github.com/search/repositories'
REPO_PER_PAGE = 100


class Repockup(object):
    def __init__(
        self,
        username: str,
        dest_dir: str = None,
        api_token: str = None
    ) -> None:
        self._username = username
        self._api_token = api_token

        self._home_user = os.getenv('HOME')
        self._repo_json = os.path.join(self._home_user, 'repockup.json')
        self._repo_temp = os.path.join(self._home_user, 'repockup_temp')

        if not dest_dir:
            self._dest_dir = self._home_user
        else:
            self._dest_dir = dest_dir

        if not os.path.isdir(self._repo_temp):
            os.mkdir(self._repo_temp)
        else:
            shutil.rmtree(self._repo_temp, ignore_errors=True)
            os.mkdir(self._repo_temp)

    def _get_repositories(self) -> list:
        repositories = []

        if self._api_token:
            headers = {'Authorization': f'token {self._api_token}'}
        else:
            headers = None

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
        split_list = [repositories[i:i + num] for i in range(0, len(repositories), num)]
        return split_list

    def _clone_repositories(self, repositories: list) -> None:
        for repo in repositories:
            url = repo.get('clone_url')
            name = repo.get('name')

            print(f'Cloning "{name}"...')

            process = subprocess.Popen(f'cd {self._repo_temp} && git clone {url} -q', shell=True)
            process.wait()

    def _start_threads(self, repositories: list):
        split_repo = self._split_repositories(repositories)
        threads = []

        for repo in split_repo:
            th = Thread(target=self._clone_repositories, args=(repo,))
            threads.append(th)
            th.start()

        while True:
            alive_list = [i.is_alive() for i in threads]

            if sum(alive_list) == 0:
                break

    def _move_to_dest(self) -> None:
        if not os.path.isdir(self._dest_dir):
            raise FileNotFoundError(f'"{self._dest_dir}" not found')

        base_name = f'{self._username}-repositories'
        file_path = os.path.join(self._home_user, base_name)
        dest_zip_path = os.path.join(self._dest_dir, base_name + '.zip')

        print('Creating ZIP file...')
        shutil.make_archive(file_path, 'zip', self._repo_temp)

        if os.path.isfile(dest_zip_path):
            os.remove(dest_zip_path)

        print(f'Moving ZIP file to "{dest_zip_path}"...')
        shutil.move(file_path + '.zip', self._dest_dir)

    def _has_changed(self, repositories: list, repository: dict) -> bool:
        for repo in repositories:
            if repo['name'] == repository['name']:
                return repo['pushed_at'] != repository['pushed_at']

        return True

    def backup(self) -> None:
        repositories = self._get_repositories()
        repo_json = self._get_repo_json()

        if not repo_json:
            self._start_threads(repositories)
            self._add_repo_json(repositories)
        else:
            to_update = []

            for repo in repositories:
                if self._has_changed(repo_json, repo):
                    to_update.append(repo)

            self._clone_repositories(to_update)
            self._add_repo_json(repositories)

        self._move_to_dest()
        print('OK')
