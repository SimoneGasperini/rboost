import os

import nltk

from setuptools import setup
from setuptools import find_packages


def set_abspath ():

  with open(file='./rboost/cli/__path.py', mode='w') as file:
    line = 'PATH = "' + os.path.dirname(os.getcwd()).replace('\\','/') + '"'
    file.write(line)


def create_dirs ():

  path = os.path.dirname(os.getcwd()).replace('\\','/') + '/RBoost_Data/'
  dirs = ['My_Documents/pdfs','My_Documents/notebooks','My_Documents/remarks','My_Downloads']

  for d in dirs:
    os.makedirs(path + d, exist_ok=True)


def download_wordnet ():

  nltk.download('wordnet')


set_abspath()
create_dirs()
download_wordnet()



def get_requirements ():
  with open(file='./requirements.txt', mode='r') as file:
    reqs = file.read().splitlines()
  return reqs

setup (

  name = 'rboost',
  version = '0.0.1',

  author = 'Simone Gasperini',
  author_email = 'simone.gasperini2@studio.unibo.it',

  description = 'rboost software',
  url = 'https://github.com/SimoneGasperini/rboost.git',

  packages = find_packages(),

  install_requires = get_requirements(),

  entry_points = {
    'console_scripts': [
      'rboost = rboost.__main__:RBoost',
    ]
  },

  python_requires = '>=3.8',

)
