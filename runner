#!/usr/bin/python3

import configparser
import os

from autobahn.twisted.wamp import ApplicationRunner

from pigpio import component as gpio


if __name__ == '__main__':
    snap_data = os.environ.get('SNAP_DATA', None)
    if snap_data:
        config = configparser.ConfigParser()
        config.read(os.path.join(snap_data, 'config'))
        runner = ApplicationRunner(url=config.get('config', 'crossbar'), realm=config.get('config', 'realm'))
    else:
        runner = ApplicationRunner(url='ws://localhost:8080/ws', realm='realm1')
    runner.run(gpio.ClientSession, auto_reconnect=True)
