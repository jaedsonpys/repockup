import argeasy

from .repockup import Repockup
from .__init__ import __version__


def main():
    parser = argeasy.ArgEasy(
        project_name='Repockup',
        description='Clone all your repositories with Repockup quickly and simply!',
        version=__version__
    )
