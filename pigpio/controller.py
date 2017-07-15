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
    all_exported_pins = list(filter(None, [i.replace('gpio', '') for i in os.listdir(PATH_GPIO)]))
    return [get_state(pin) for pin in all_exported_pins]
