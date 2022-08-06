import os
import shutil

import requests

GITHUB_API = 'https://api.github.com/users'


class Repockup(object):
    def __init__(self, username: str, api_token: str = None) -> None:
        self._api_token = api_token
        self._username = username
