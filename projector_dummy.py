#!/usr/bin/python
# -*- coding: utf-8 -*-
import Pyro4

class projector(object):
    def __init__(self):
        pass
    def _send(self, msg):
        pass
    def on(self):
        pass
    def off(self):
        pass

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
uri = daemon.register(projector())
ns.register("projector", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()

