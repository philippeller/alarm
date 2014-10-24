#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
import signal
import sys
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#def signal_handler(signal, frame):
#    print '\nciao!'
#    sys.exit(0)
#signal.signal(signal.SIGINT, signal_handler)

class output(object):
    def __init__(self,pin,ini=False):
        self._pin = pin
        self._state = ini
        GPIO.setup(self._pin,GPIO.OUT)
        GPIO.output(self._pin,self._state)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self,val):
        if not val == self._state:
            self._state = val
            GPIO.output(self._pin,self._state)

    def set(self,val):
        GPIO.output(self._pin,val)
        self._state = val

    def tick(self):
        GPIO.output(self._pin,True)
        GPIO.output(self._pin,False)

    def __repr__(self):
        return 'pin %s, state %s'%(self._pin,self._state)



if __name__ == '__main__':

    r1 = output(9)
    r2 = output(10)

    GPIO.setup(11, GPIO.IN)
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(8, GPIO.IN)
    GPIO.setup(25, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(23, GPIO.IN)
    def hello(channel):
        print '%s has been pressed'%channel


    def switch(channel):
        if channel == 11:
            s = r1
        elif channel == 23:
            s = r2
        else:
            s = None
        if s.state == True:
            s.state = False
        else:
            s.state = True

    GPIO.add_event_detect(11, GPIO.RISING, callback=switch, bouncetime=200)
    GPIO.add_event_detect(7, GPIO.RISING, callback=hello, bouncetime=200)
    GPIO.add_event_detect(8, GPIO.RISING, callback=hello, bouncetime=200)
    GPIO.add_event_detect(25, GPIO.RISING, callback=hello, bouncetime=200)
    GPIO.add_event_detect(24, GPIO.RISING, callback=hello, bouncetime=200)
    GPIO.add_event_detect(23, GPIO.RISING, callback=switch, bouncetime=200)
    while True:
        sleep(1)
