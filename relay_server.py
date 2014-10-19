#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
import Pyro4
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_relay import *

class relay(object):
    def __init__(self):
        errmsg=YRefParam()
        if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
            sys.exit("init error"+errmsg.value)
        self.relay = YRelay.FirstRelay()
        if self.relay is None: sys.exit('no device connected')
        if not(self.relay.isOnline()):sys.exit('device not connected')

    @Pyro4.expose
    @property
    def state(self):
        return self.relay.get_state()

    def set_state(self,val):
        if val:
            self.relay.set_state(YRelay.STATE_B)
        else:
            self.relay.set_state(YRelay.STATE_A)

    def switch(self):
        self.state = not self.state

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
uri = daemon.register(relay())
ns.register("relay", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()

