#!/usr/bin/python
# -*- coding: utf-8 -*-
import Pyro4
import sys
import time
from phue.phue import Bridge

class lights(object):

    def __init__(self):
        self._b = Bridge('192.168.1.53') # Enter bridge IP here.
        print self._b
        #print b.get_api()
        #If running for the first time, press button on bridge and run with b.connect() uncommented
        #self.b.connect()
        self.lights = self._b.get_light_objects()

    def set(self, name, **kwargs):
        for key, value in kwargs.iteritems():
            for light in self.lights:
                if name == 'all' or light.name == name:
                    setattr(light,key,value)

    def status(self, attr='on'):
        status = []
        for light in self.lights:
            status.append(getattr(light, attr))
        return status

    def on(self, name='all'):
        self.set(name,on=True)

    def off(self, name='all'):
        self.set(name,on=False)

    def any_all(self,name='all'):
        status = []
        for light in self.lights:
            if light.name == name:
                return light.on
            else:
                status.append(light.on)
        if all(status): return True
        if not any(status): return False
        else: return 'unknown'

    def fade_in(self,name='all'):
        self.set(name,on=True,brightness=0)
        for i in range(0,255):
            self.set(name,brightness=i)
            time.sleep(0.1)

    def set_temp(self,temp):
        for light in self.lights:
            light.brightness = 254
            light.colortemp_k = int(temp)


    def tv(self):
        self.lights[0].on = False
        self.lights[1].on = False
        self.lights[2].brightness = 100
        self.lights[2].saturation = 255
        self.lights[2].hue = 0

    def tv_dinner(self):
        self.lights[0].brightness = 40
        self.lights[0].saturation = 255
        self.lights[0].hue = 48000
        self.lights[1].on = False
        self.lights[2].brightness = 100
        self.lights[2].saturation = 255
        self.lights[2].hue = 0

    def dark_red(self):
        for light in self.lights:
            light.brightness = 80
            light.hue = 0
            light.saturation = 254

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
ns.list()
uri = daemon.register(lights())
ns.register("lights", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()

