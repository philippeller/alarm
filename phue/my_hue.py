#!/usr/bin/python
from phue import Bridge
import sys
import time

class my_hue(object):
    def __init__(self):
        self.b = Bridge('192.168.1.53') # Enter bridge IP here.
        #print b.get_api()
        #If running for the first time, press button on bridge and run with b.connect() uncommented
        #self.b.connect()
        self.lights = self.b.get_light_objects()
        print self.lights

    def set(self, name, **kwargs):
        for key, value in kwargs.iteritems():
            for light in self.lights:
                if name == 'all' or light.name == name:
                    setattr(light,key,value)

    def on(self, name='all'):
        self.set(name,on=True)

    def off(self, name='all'):
        self.set(name,on=False)

    def status(self,name='all'):
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

    #def set_temp(self,temp):
    #    for light in self.lights:
    #        light.brightness = 254
    #        light.colortemp_k = int(temp)


    #def tv(self):
    #    self.lights[0].on = False
    #    self.lights[1].on = False
    #    self.lights[2].brightness = 100
    #    self.lights[2].saturation = 255
    #    self.lights[2].hue = 0

    #def tv_dinner(self):
    #    self.lights[0].brightness = 40
    #    self.lights[0].saturation = 255
    #    self.lights[0].hue = 48000
    #    self.lights[1].on = False
    #    self.lights[2].brightness = 100
    #    self.lights[2].saturation = 255
    #    self.lights[2].hue = 0

    #def dark_red(self):
    #    for light in self.lights:
    #        light.brightness = 80
    #        light.hue = 0
    #        light.saturation = 254


if __name__ == '__main__':
    room = my_hue()
    #room.on()
    #time.sleep(2)
    #room.tv()
    room.fade_in()
    #room.set('all',on=True)
    room.set('all',on=False)
    #room.fade_in('Bed')
