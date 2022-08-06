import shutil
import os

GITHUB_API = 'https://api.github.com/users'


class Repockup(object):
    def __init__(self, api_token: str = None) -> None:
        self._api_token = api_token
