#!/usr/bin/python3

import os

from autobahn.twisted.component import Component, run
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor

BASE_GPIO = '/sys/class/gpio'
PATH_GPIO = os.path.join(BASE_GPIO, 'gpio{}')


def _turn(pin_number, value):
    path = PATH_GPIO.format(pin_number)
    if os.path.exists(path):
        with open(os.path.join(path, 'direction'), 'w') as file:
            file.write('out')
        with open(os.path.join(path, 'value'), 'w') as file:
            file.write(str(value))
    else:
        print("Path {} does not exist".format(path))


def turn_on(pin_number):
    _turn(pin_number, 0)


def turn_off(pin_number):
    _turn(pin_number, 1)


def get_state(pin_number):
    path = PATH_GPIO.format(pin_number)
    with open(os.path.join(path, 'direction')) as file:
        direction = file.read().strip()
    with open(os.path.join(path, 'value')) as file:
        value = file.read().strip()

    return {
        'pin_number': pin_number,
        'direction': direction,
        'value': value,
        'value_verbose': 'on' if value == '0' else 'off'
    }


def get_states():
    def is_gpio(item):
        return item.startswith('gpio') and 'chip' not in item

    return [get_state(int(pin.replace('gpio', ''))) for pin in filter(is_gpio, os.listdir(BASE_GPIO))]


if __name__ == '__main__':
    if os.environ.get("SNAP_NAME") != "pigpio":
        os.environ['SNAP_COMMON'] = os.path.expandvars('$HOME')

    transport = {
        "type": "rawsocket",
        "url": "ws://localhost/ws",
        "endpoint": UNIXClientEndpoint(reactor, os.path.join(os.environ['SNAP_COMMON'], 'deskconn.sock'))
    }

    component = Component(transports=[transport], realm="deskconn")


    @component.on_join
    def join(session, details):
        print("Joined session....")
        session.register(turn_on, "org.deskconn.gpio.turn_on")
        session.register(turn_off, "org.deskconn.gpio.turn_off")
        session.register(get_state, "org.deskconn.gpio.get_state")
        session.register(get_states, "org.deskconn.gpio.get_states")

    run([component])
