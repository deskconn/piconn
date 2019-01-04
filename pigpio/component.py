from autobahn.twisted import wamp
from twisted.internet import threads
from twisted.internet.defer import inlineCallbacks, returnValue

from pigpio import controller
from pigpio import wamp_controller


class ClientSession(wamp.ApplicationSession):
    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("Connected:  {details}", details=details)
        gpio_controller = wamp_controller.GPIOController(self)
        yield self.register(gpio_controller.turn_on, "io.crossbar.pigpio-wamp.turn_on")
        yield self.register(gpio_controller.turn_off, "io.crossbar.pigpio-wamp.turn_off")
        yield self.register(controller.get_state, "io.crossbar.pigpio-wamp.get_state")
        yield self.register(controller.get_states, "io.crossbar.pigpio-wamp.get_states")

    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()


class ServiceDiscoverySession(wamp.ApplicationSession):
    def __init__(self, config=None):
        super().__init__(config)
        self.discovery = controller.ServiceDiscovery()

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info('session joined: {}'.format(details))
        res = yield threads.deferToThread(self.discovery.start_publishing)
        returnValue(res)

    def onLeave(self, details):
        self.log.info('session left: {}'.format(details))
        self.discovery.stop_publishing()
        self.disconnect()

