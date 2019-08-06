import os
import time

from autobahn.twisted.component import Component, run
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor
import txaio

import pygpio

txaio.use_twisted()
log = txaio.make_logger()


def assemble(sock, reactor):
    transport = {
        "type": "rawsocket",
        "url": "ws://localhost/ws",
        "endpoint": UNIXClientEndpoint(reactor, sock),
        "serializer": "cbor",
    }
    component = Component(transports=[transport], realm="deskconn")
    component._transports[0].max_retries = 0

    @component.on_join
    def join(session, _):
        log.info("connected to deskconnd")
        session.register(pygpio.turn_on, "org.deskconn.gpio.turn_on")
        session.register(pygpio.turn_off, "org.deskconn.gpio.turn_off")
        session.register(pygpio.get_state, "org.deskconn.gpio.get_state")
        session.register(pygpio.get_states, "org.deskconn.gpio.get_states")

    @component.on_leave
    def left(session, _):
        log.info("disconnected from deskconnd")
        enter_loop()
    return component


def enter_loop():
    while not os.path.exists(sock_path):
        time.sleep(1)
        log.debug("deskconnd not found, please make sure its installed and running.")

    run([assemble(sock_path, reactor)])


if __name__ == '__main__':
    if os.environ.get("SNAP_NAME") != "gpiod":
        os.environ['SNAP_COMMON'] = os.path.expandvars('$HOME')

    sock_path = os.path.join(os.path.expandvars('$SNAP_COMMON/deskconnd-sock-dir'), 'deskconnd.sock')
    enter_loop()
