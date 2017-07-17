import os
from urllib.parse import urlparse


NAME_CONF_FILE = '.pigpio.conf'
DIR_SNAP_COMMON = 'SNAP_COMMON'


def get_config_path():
    if DIR_SNAP_COMMON in os.environ:
        return os.path.join(os.environ[DIR_SNAP_COMMON], NAME_CONF_FILE)
    return os.path.join(os.path.expanduser('~'), NAME_CONF_FILE)


# Stolen from https://github.com/aaugustin/websockets
def validate_websocket_uri(uri):
    uri = urlparse(uri)
    try:
        assert uri.scheme in ('ws', 'wss')
        assert uri.params == ''
        assert uri.fragment == ''
        assert uri.username is None
        assert uri.password is None
        assert uri.hostname is not None
    except AssertionError:
        raise RuntimeError("Invalid WebSocket URI")
