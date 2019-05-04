import argparse

import pygpio


if __name__ == '__main__':
    parser = argparse.ArgumentParser('pigpio command line')
    subparsers = parser.add_subparsers()

    on = subparsers.add_parser('on')
    on.add_argument('pin_on', type=int)

    off = subparsers.add_parser('off')
    off.add_argument('pin_off', type=int)

    args = parser.parse_args()
    if hasattr(args, 'pin_off'):
        pygpio.turn_off(args.pin_off)
    elif hasattr(args, 'pin_on'):
        pygpio.turn_on(args.pin_on)
    else:
        print("Unexpected code path reached")
