#!/usr/bin/env python3

import os
import shelve
import sys

from autobahn.twisted.wamp import ApplicationRunner

from pigpio import component as gpio
from pigpio import utils

LINE_FANCY = "-------------------------------------------------------------------------------"


def setup_config(config_path, fancy=True):
    if fancy:
        print(LINE_FANCY)

    url = input("Please enter WAMP router address that you want to connect to: ")
    utils.validate_websocket_uri(url)
    realm = input("Please enter the name of the realm to connect to: ")

    with shelve.open(config_path) as config_db:
        config_db['url'] = url
        config_db['realm'] = realm

    print("Config done.")
    if fancy:
        print(LINE_FANCY)


def main():
    if len(sys.argv) > 2:
        print("Invalid arguments provided.")
        print("Either run this program without any arguments or use --reconfigure for setup.")
        exit(1)

    reconfigure = len(sys.argv) == 2 and sys.argv[1] == '--reconfigure'

    if len(sys.argv) == 2 and sys.argv[1] != '--reconfigure':
        print("Invalid argument provided.")
        print("Supported argument: --reconfigure")
        print("Example: {} --reconfigure".format(sys.argv[0]))
        exit(1)

    config_path = utils.get_config_path()

    if not os.path.exists(config_path):
        print(LINE_FANCY)
        print("Config missing...\n")
        setup_config(config_path, False)
        print(LINE_FANCY)
    elif reconfigure:
        setup_config(config_path, True)

    with shelve.open(config_path) as config_db:
        url = config_db.get('url')
        realm = config_db.get('realm')

    runner = ApplicationRunner(url=url, realm=realm)
    runner.run(gpio.ClientSession, auto_reconnect=True)


if __name__ == '__main__':
    main()
