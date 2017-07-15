from pigpio import controller


class GPIOController:
    def __init__(self, session):
        self.session = session

    def turn_on(self, pin_number):
        controller.turn_on(pin_number)
        # yield self.session.publish('io.crossbar.gpio.turned_on', pin_number)

    def turn_off(self, pin_number):
        controller.turn_off(pin_number)
        # yield self.session.publish('io.crossbar.gpio.turned_off', pin_number)
