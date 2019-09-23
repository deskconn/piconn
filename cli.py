#!/usr/bin/env python3

import argparse
import os
import sys

from autobahn.twisted.component import Component, run
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor


if __name__ == '__main__':
    parser = argparse.ArgumentParser('pigpio command line')
    parser.add_argument("state", choices=('on', 'off'))
    parser.add_argument("pin", type=int)
    args = parser.parse_args()

    if os.environ.get("SNAP_NAME") != "piconn":
        os.environ['SNAP_COMMON'] = os.path.expandvars('$HOME')

    sock_path = os.path.join(os.path.expandvars('$SNAP_COMMON/deskconnd-sock-dir'), 'deskconnd.sock')
    if not os.path.exists(sock_path):
        print("deskconnd not found, please make sure its installed and running.")
        sys.exit(1)

    transport = {
        "type": "rawsocket",
        "url": "ws://localhost/ws",
        "endpoint": UNIXClientEndpoint(reactor, sock_path),
        "serializer": "cbor",
    }

    component = Component(transports=[transport], realm="deskconn")

    @component.on_join
    async def join(session, _):
        if args.state == 'on':
            procedure = 'org.deskconn.piconn.gpio.set_out_high'
        else:
            procedure = 'org.deskconn.piconn.gpio.set_out_low'

        d = session.call(procedure, args.pin)
        d.addCallback(session.leave)
        d.addErrback(session.leave)

    run([component])
