import os
import argparse

from autobahn.twisted.component import Component, run
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor


if __name__ == '__main__':
    parser = argparse.ArgumentParser('pigpio command line')
    parser.add_argument("state", choices=('on', 'off'))
    parser.add_argument("pin", type=int)
    args = parser.parse_args()

    if os.environ.get("SNAP_NAME") != "pigpio":
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
    async def join(session, _):
        if args.state == 'on':
            procedure = 'org.deskconn.gpio.turn_on'
        else:
            procedure = 'org.deskconn.gpio.turn_off'

        d = session.call(procedure, args.pin)
        d.addCallback(session.leave)
        d.addErrback(session.leave)

    run([component])
