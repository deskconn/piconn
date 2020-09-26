#!/usr/bin/env python3

import argparse
import os
import sys

from autobahn.twisted.component import Component, run
from autobahn.wamp import ApplicationError
from twisted.internet.endpoints import UNIXClientEndpoint
from twisted.internet import reactor


if __name__ == '__main__':
    parser = argparse.ArgumentParser('pigpio command line')
    parser.add_argument("state", choices=('on', 'off'))
    parser.add_argument("pin", type=int)
    args = parser.parse_args()

    if os.environ.get("SNAP_NAME") != "piconn":
        sock_dir = os.path.expandvars('$HOME')
    else:
        sock_dir = os.path.join(os.path.expandvars('$SNAP_COMMON'), 'deskconn-sock-dir')

    sock_path = os.path.join(sock_dir, 'deskconnd.sock')
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
    async def joined(session, _details):
        if args.state == 'on':
            procedure = 'org.deskconn.piconn.gpio.set_out_high'
        else:
            procedure = 'org.deskconn.piconn.gpio.set_out_low'

        try:
            await session.call(procedure, args.pin)
        except ApplicationError as e:
            print(e)
            pass
        finally:
            session.leave()

    @component.on_connectfailure
    async def failed(comp, reason):
        print("Failed to connect to server")
        comp.stop()

    run([component])
