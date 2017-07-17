#!/usr/bin/env python3

import configparser
import os

from autobahn.twisted.wamp import ApplicationRunner

from pigpio import component as gpio

NAME_CONF_FILE = '.pigpio.conf'
DIR_SNAP_COMMON = 'SNAP_COMMON'


def get_config_path():
    if DIR_SNAP_COMMON in os.environ:
        return os.path.join(os.environ[DIR_SNAP_COMMON], NAME_CONF_FILE)
    return os.path.join(os.path.expanduser('~'), NAME_CONF_FILE)


def main():
    config = configparser.ConfigParser()
    config.read(get_config_path())
    runner = ApplicationRunner(url=config.get('config', 'crossbar'), realm=config.get('config', 'realm'))
    runner.run(gpio.ClientSession, auto_reconnect=True)


if __name__ == '__main__':
    main()
