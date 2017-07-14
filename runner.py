#!/usr/bin/python3

from autobahn.twisted.wamp import ApplicationRunner

from pigpio import component as gpio


if __name__ == '__main__':
    runner = ApplicationRunner(url="ws://192.168.1.3:8080/ws", realm="realm1")
    runner.run(gpio.ClientSession, auto_reconnect=True)
