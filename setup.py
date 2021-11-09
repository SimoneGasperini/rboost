from setuptools import setup, find_packages


NAME = 'rboost'
VERSION = '0.2.0'
AUTHOR = 'SimoneGasperini'
AUTHOR_EMAIL = 'simone.gasperini2@studio.unibo.it'
REPO_URL = 'https://github.com/SimoneGasperini/rboost.git'
PYTHON_VERSION = '>=3.8'


def get_requirements():
    with open('./requirements.txt', 'r') as f:
        reqs = f.read().splitlines()
    return reqs


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=REPO_URL,
    python_requires=PYTHON_VERSION,
    packages=find_packages(),
    install_requires=get_requirements(),
    entry_points={'console_scripts': ['rboost=rboost.gui.__main:rboost']},
    include_package_data=True
)
