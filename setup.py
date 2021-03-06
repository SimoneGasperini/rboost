import os

from shutil import copyfile

from setuptools import setup
from setuptools import find_packages

import nltk


PATH = os.path.expanduser('~/Desktop/RBoost_Data').replace('\\','/')
CLIENT = './client.json'
TOKEN = './token.pkl'
REQUIREMENTS = './requirements.txt'


dirs = ['/My_Documents/pdfs','/My_Documents/notebooks','/My_Documents/remarks',
        '/My_Downloads','/client_token']
for d in dirs:
  os.makedirs(PATH + d, exist_ok=True)


copyfile(CLIENT, PATH + dirs[-1] + CLIENT[1:])
copyfile(TOKEN, PATH + dirs[-1] + TOKEN[1:])


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
