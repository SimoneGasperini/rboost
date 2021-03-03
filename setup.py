import os

from setuptools import setup
from setuptools import find_packages

def set_abspath ():
  with open(file='./rboost/cli/__path.py', mode='w') as file:
    line = 'PATH = ' + '"' + os.getcwd() + '"'
    file.write(line.replace('\\','/'))


def download_wordnet ():
  import nltk
  nltk.download('wordnet')


set_abspath()
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
