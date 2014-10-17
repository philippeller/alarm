#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import Pyro4
import time
class projector(object):
    def __init__(self):
        self.ser = serial.Serial('/dev/tty.usbserial', 9600, timeout=1)
    def _send(self, msg):
        self.ser.write('%s\r'%msg)
    def on(self):
        self._send('PWR ON')
    def off(self):
        self._send('PWR OFF')

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
uri = daemon.register(projector())
ns.register("projector", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()

