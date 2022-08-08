import argeasy

from .repockup import Repockup
from .__init__ import __version__


def main():
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
