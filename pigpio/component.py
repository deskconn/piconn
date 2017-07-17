from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession

from pigpio import controller
from pigpio import wamp_controller


class ClientSession(ApplicationSession):
    def onConnect(self):
        self.log.info("Client connected: {klass}", klass=ApplicationSession)
        self.join(self.config.realm, [u'anonymous'])

    def onChallenge(self, challenge):
        self.log.info("Challenge for method {authmethod} received", authmethod=challenge.method)
        raise Exception("We haven't asked for authentication!")

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

    def onDisconnect(self):
        self.log.info("Router connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass
