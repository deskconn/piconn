import os

from autobahn.twisted.component import Component, run
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor

import pygpio


if __name__ == '__main__':
    if os.environ.get("SNAP_NAME") != "gpiod":
        os.environ['SNAP_COMMON'] = os.path.expandvars('$HOME')

    transport = {
        "type": "rawsocket",
        "url": "ws://localhost/ws",
        "endpoint": UNIXClientEndpoint(reactor,
                                       os.path.join(os.path.expandvars('$SNAP_COMMON/deskconnd-sock-dir'),
                                                    'deskconnd.sock')),
        "serializer": "cbor",
    }

    component = Component(transports=[transport], realm="deskconn")


    @component.on_join
    def join(session, _):
        print("Joined session....")
        session.register(pygpio.turn_on, "org.deskconn.gpio.turn_on")
        session.register(pygpio.turn_off, "org.deskconn.gpio.turn_off")
        session.register(pygpio.get_state, "org.deskconn.gpio.get_state")
        session.register(pygpio.get_states, "org.deskconn.gpio.get_states")

    run([component])
