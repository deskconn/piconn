import argparse

import requests


if __name__ == '__main__':
    parser = argparse.ArgumentParser('pigpio command line')
    subparsers = parser.add_subparsers()

    on = subparsers.add_parser('on')
    on.add_argument('pin_on', type=int)

    off = subparsers.add_parser('off')
    off.add_argument('pin_off', type=int)

    args = parser.parse_args()
    if hasattr(args, 'pin_off'):
        requests.post('http://localhost:5020/call',
                      json={'procedure': 'org.deskconn.gpio.turn_off', 'args': [args.pin_off]})
    elif hasattr(args, 'pin_on'):
        requests.post('http://localhost:5020/call',
                      json={'procedure': 'org.deskconn.gpio.turn_on', 'args': [args.pin_on]})
    else:
        print("Unexpected code path reached")
