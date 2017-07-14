import os
import shlex
import subprocess

from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

PATH_GPIO = "/sys/class/gpio/gpio{}"


def _turn(pin_number, value):
    path = PATH_GPIO.format(pin_number)
    if os.path.exists(path):
        subprocess.check_call(shlex.split("echo out > {}".format(os.path.join(path, 'direction'))))
        subprocess.check_call(shlex.split("echo {} > {}".format(value, os.path.join(path, 'value'))))


def turn_on(pin_number):
    _turn(pin_number, 0)


def turn_off(pin_number):
    _turn(pin_number, 1)


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
        yield self.register(turn_on, "io.crossbar.gpio.turn_on")
        yield self.register(turn_off, "io.crossbar.gpio.turn_off")

    def onLeave(self, details):
        self.log.info("Router session closed ({details})", details=details)
        self.disconnect()

    def onDisconnect(self):
        self.log.info("Router connection closed")
        try:
            reactor.stop()
        except ReactorNotRunning:
            pass


if __name__ == '__main__':
    runner = ApplicationRunner(url="ws://192.168.1.3:8080/ws", realm="realm1")
    runner.run(ClientSession, auto_reconnect=True)