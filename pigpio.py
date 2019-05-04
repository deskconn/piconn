import argparse
import os

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
    parser = argparse.ArgumentParser('pigpio command line')
    subparsers = parser.add_subparsers()

    on = subparsers.add_parser('on')
    on.add_argument('pin_on', type=int)

    off = subparsers.add_parser('off')
    off.add_argument('pin_off', type=int)

    args = parser.parse_args()
    if hasattr(args, 'pin_off'):
        turn_off(args.pin_off)
    elif hasattr(args, 'pin_on'):
        turn_on(args.pin_on)
    else:
        print("Unexpected code path reached")
