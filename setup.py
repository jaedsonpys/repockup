from setuptools import setup
from repockup import __version__

with open('README.md', 'r') as reader:
    readme = reader.read()

setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='repockup',
    version=__version__,
    description='Clone all your repositories with Repockup',
    long_description=readme,
    long_description_content_type='text/markdown',
    packages=['repockup'],
    url='https://github.com/jaedsonpys/repockup',
    keywords=['backup', 'github', 'git', 'repositories'],
    install_requires=['requests']
)
