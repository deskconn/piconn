import os
import socket

from zeroconf import ServiceInfo, Zeroconf

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


def get_local_address():
    # FIXME: depends on the internet, hence breaks the "edge" usecase.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("www.google.com", 80))
    res = s.getsockname()[0]
    s.close()
    return res


class ServiceDiscovery:
    def __init__(self, type_='_crossbar._tcp', name='Screen brightness server', address='0.0.0.0', port=5020):
        super().__init__()

        self.type_ = type_
        self.info = ServiceInfo(
            type_="{}.local.".format(type_),
            name="{}.{}.local.".format(name, type_),
            address=socket.inet_aton(get_local_address() if address == '0.0.0.0' else address),
            port=port,
            properties={}
        )

        self.zeroconf = Zeroconf()

    def start_publishing(self):
        print("Registering service: {}".format(self.type_))
        self.zeroconf.register_service(self.info)
        print("Registered service: {}".format(self.type_))

    def stop_publishing(self):
        print("Unregistering service: {}".format(self.type_))
        self.zeroconf.unregister_service(self.info)
        print("Unregistered service: {}".format(self.type_))

