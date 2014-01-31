#!/usr/bin/python
from phue import Bridge
import random
import sys
import time
import math

b = Bridge('192.168.1.67') # Enter bridge IP here.


#print b.get_api()
#If running for the first time, press button on bridge and run with b.connect() uncommented
b.connect()

lights = b.get_light_objects()

print lights

for light in lights:
    light.on = True
    light.brightness = 254
    light.colortemp_k = int(sys.argv[1])


#i=0
#while True:
#    i=i%360
#    j=0
#    for light in lights:
#        light.brightness = int( (math.sin(math.radians(i+(j*120)))+1)*128)
#        j+=1
#    i+=1
#    time.sleep(0.003)
