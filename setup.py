import os

from shutil import copy

from setuptools import setup
from setuptools import find_packages

import nltk


RBOOST_DATA_PATH = os.path.expanduser('~/Desktop/RBoost_Data/').replace('\\', '/')
CLIENT_SECRETS   = './client_secrets.json'
CREDENTIALS      = './credentials.txt'
REQUIREMENTS     = './requirements.txt'


directories = ['My_Documents/pdfs',
               'My_Documents/notebooks',
               'My_Documents/remarks',
               'My_Downloads']
for directory in directories:
  os.makedirs(RBOOST_DATA_PATH + directory, exist_ok=True)


copy(src=CLIENT_SECRETS, dst=RBOOST_DATA_PATH)
copy(src=CREDENTIALS, dst=RBOOST_DATA_PATH)


nltk.download('wordnet')


with open(REQUIREMENTS, 'r') as file:
  requirements = file.read().splitlines()

setup (

  name = 'rboost',
  version = '0.0.1',

  author = 'Simone Gasperini',
  author_email = 'simone.gasperini2@studio.unibo.it',

  description = 'rboost software',
  url = 'https://github.com/SimoneGasperini/rboost.git',

  packages = find_packages(),

  install_requires = requirements,

  entry_points = {
    'console_scripts': [
      'rboost = rboost.__main__:RBoost',
    ]
  },

  python_requires = '>=3.8',

)
