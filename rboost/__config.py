import json
import pkg_resources


CONFIG_INSTALL = \
    json.load(
        pkg_resources.resource_stream(__name__, 'config/config_install.json')
    )


CLIENT_SECRETS = \
    pkg_resources.resource_stream(
        __name__, 'config/client_secrets.json').name


def get_config():
    return CONFIG_INSTALL, CLIENT_SECRETS
