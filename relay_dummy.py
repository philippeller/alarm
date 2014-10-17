#!/usr/bin/python
# -*- coding: utf-8 -*-
import Pyro4

class dummy(object):
    def __init__(self):
        self.state = False
    def get_state(self):
        return self.state
    def set_state(self, val):
        self.state = val

class relay(object):
    def __init__(self):
        self.relay = dummy()

    @Pyro4.expose
    @property
    def state(self):
        return self.relay.get_state()

    @Pyro4.expose
    @state.setter
    def state(self,val):
        if val:
            self.relay.set_state(False)
        else:
            self.relay.set_state(True)

    def switch(self):
        self.state = not self.state

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
uri = daemon.register(relay())
ns.register("relay", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()

