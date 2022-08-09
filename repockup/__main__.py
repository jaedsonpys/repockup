import os

import argeasy

from .repockup import Repockup
from .__init__ import __version__


def main() -> bool:
    parser = argeasy.ArgEasy(
        project_name='Repockup',
        description='Clone all your repositories with Repockup quickly and simply!',
        version=__version__
    )

    parser.add_argument('backup', 'Clone all repositories', action='store_true')
    parser.add_flag('--username', 'Username from GitHub')
    parser.add_flag('--token', 'API token from GitHub (to clone private repositories)')
    parser.add_flag('--dest', 'Destination of the repositories ZIP file')

    args = parser.get_args()

    if args.backup:
        username = args.username
        api_token = args.token
        file_dest = args.dest

        if not username:
            print('fatal: username is required')
            return True

        if file_dest:
            if not os.path.isdir(file_dest):
                print(f'fatal: "{file_dest}" is a non-existent directory')
                return True
        else:
            print('fatal: file destination is required')

        repockup = Repockup(username, dest_dir=file_dest, api_token=api_token)        
        status = repockup.backup()

        if status:
            print('OK')
        else:
            print('\033[31mThere are no repositories to clone\033[m')

    return False
