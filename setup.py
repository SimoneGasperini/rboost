import os
from glob import glob
from stat import S_IREAD, S_IRGRP, S_IROTH


def set_abspath ():
  with open(file='./rboost/cli/__path.py', mode='w') as file:
    line = 'PATH = ' + '"' + os.getcwd() + '"'
    file.write(line.replace('\\','/'))


def download_wordnet ():
  import nltk
  nltk.download('wordnet')


def make_readonly ():
  txt_files = [obj for obj in glob('./rboost/database/**', recursive=True)
               if os.path.isfile(obj) and obj.endswith('.txt')]
  for file in txt_files:
    os.chmod(file, S_IREAD|S_IRGRP|S_IROTH)


set_abspath()
download_wordnet()
make_readonly()




from setuptools import setup
from setuptools import find_packages


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
