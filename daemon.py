#!/usr/bin/env python3

import os
import time

from autobahn import wamp
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.component import Component, run
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor
import txaio

txaio.use_twisted()
log = txaio.make_logger()

BASE_GPIO = '/sys/class/gpio'
PATH_GPIO = os.path.join(BASE_GPIO, 'gpio{}')
GPIO_OUT_ON = 0
GPIO_OUT_OFF = 1


class GPIOComponent(ApplicationSession):
    async def onJoin(self, details):
        self.register(self, prefix='org.deskconn.gpio.')

    def _set(self, direction, pin_number, value):
        path = PATH_GPIO.format(pin_number)
        if os.path.exists(path):
            with open(os.path.join(path, 'direction'), 'w') as file:
                file.write(direction)
            with open(os.path.join(path, 'value'), 'w') as file:
                file.write(str(value))
            return True
        else:
            print("Path {} does not exist".format(path))
            return False

    @wamp.register(None)
    def set_out_high(self, pin_number):
        done = self._set('out', pin_number, GPIO_OUT_ON)
        if done:
            self.publish('org.deskconn.gpio.on_out_high', pin_number)

    @wamp.register(None)
    def set_out_low(self, pin_number):
        done = self._set('out', pin_number, GPIO_OUT_OFF)
        if done:
            self.publish('org.deskconn.gpio.on_out_low', pin_number)

    @wamp.register(None)
    def get_state(self, pin_number):
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

    @wamp.register(None)
    def get_states(self):
        def is_gpio(item):
            return item.startswith('gpio') and 'chip' not in item

        return [self.get_state(int(pin.replace('gpio', ''))) for pin in filter(is_gpio, os.listdir(BASE_GPIO))]


def assemble():
    transport = {
        "type": "rawsocket",
        "url": "ws://localhost/ws",
        "endpoint": UNIXClientEndpoint(reactor, sock_path),
        "serializer": "cbor",
    }
    component = Component(transports=[transport], realm="deskconn", session_factory=GPIOComponent)
    component._transports[0].max_retries = 0
    return component


if __name__ == '__main__':
    if os.environ.get("SNAP_NAME") != "gpiod":
        os.environ['SNAP_COMMON'] = os.path.expandvars('$HOME')

    sock_path = os.path.join(os.path.expandvars('$SNAP_COMMON/deskconnd-sock-dir'), 'deskconnd.sock')
    print("finding deskconnd...")
    while not os.path.exists(sock_path):
        time.sleep(1)
    print("found, now connecting.")

    run([assemble()])
