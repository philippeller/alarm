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

class register(object):
    BITS = 40

    def __init__(self,clk,clr,data,latch):
        self.CLK = output(clk)
        self.CLR = output(clr)
        self.DATA = output(data)
        self.LATCH = output(latch)
        self.clear()

    def clear(self):
        self.CLR.state = False
        self.CLK.tick()
        self.CLR.state = True

    def set(self,val):
        bits = []
        for pos in range(0,self.BITS):
            bits.append(bool(val>>pos & 1))
        self.clear()
        for bit in bits:
            #self.DATA.state = bool(val>>pos & 1)
            self.DATA.set(bit)
            self.CLK.tick()
        self.LATCH.tick()
        self.clear()

    def __del__(self):
        self.clear()
        self.LATCH.tick()

if __name__ == '__main__':
    r1 = output(9,True)
    r2 = output(10,True)
    sleep(1)
    r1 = output(9,False)
    r2 = output(10,False)
    #def __init__(clk,clr,data,latch):
    # 4 17 27 22
    reg = register(27,22,4,17)
    #pattern = [1,2,128,64,32,16,4,8,4,16,32,64,128,2,255]
    pattern = []
    even = [0,2,4,6,8,10,12,14]
    uneven = [1,3,5,7,9,11,13,15]
    #pattern = [2**16-1-2**i for i in range(4,16)]
    pattern = [2**i for i in range(0,41)]

    #reg.set(2**32-1)
    #while True:
    #    pass
    #i=0
    #while i < 2**16:
    #    reg.set(i)
    #    i+=1
    #    sleep(0.02)
    GPIO.setup(11, GPIO.IN)
    #while True:
    #    print GPIO.input(11)
    #    sleep(0.1)

    while True:
        for p in pattern:
            reg.set(p)
            sleep(0.5)
            #reg.set(2**40-1)
            #sleep(0.01)
    #while True:
    #    reg.set(random.randint(0,256))
    #    #sleep(random.randint(1,500)/1000.)
    #    sleep(0.05)
    #for bit in range(0,256):
    #    reg.set(bit)
    #    sleep(0.05)
