import os
import json
from pkg_resources import resource_stream
from pkg_resources import resource_listdir, resource_filename


def get_config_install():
    filepath = 'data/config/config_install.json'
    with resource_stream(__name__, filepath) as stream:
        config_install = json.load(stream)
    return config_install


def get_client_secrets():
    filepath = 'data/config/client_secrets.json'
    client_secrets = resource_filename(__name__, filepath)
    return client_secrets


def get_icons():
    dirpath = 'data/icons/'
    basedir = resource_filename(__name__, dirpath)
    filenames = resource_listdir(__name__, dirpath)
    icons = {filename.split('.')[0]: os.path.join(basedir, filename)
             for filename in filenames}
    return icons
