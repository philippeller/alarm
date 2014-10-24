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

    def switch(self):
        self.state = not self.state

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
        self.clear()
        self.LATCH.tick()
        bits = []
        for pos in range(0,self.BITS):
            bits.append(bool(val>>pos & 1))
        self.clear()
        for bit in bits:
            #self.DATA.state = bool(val>>pos & 1)
            self.DATA.set(bit)
            self.CLK.tick()
        self.LATCH.tick()

    def __del__(self):
        self.clear()
        self.LATCH.tick()


class display(object):

    def __init__(self):
        self.home = False
        self.alarm = False
        self.snooze = False
        self.sound = False
        self.relay1 = False
        self.relay2 = False


    def _get_bin(self,digits):
        A = {'a':20,'b':37,'c':21,'d':35,'e':36,'f':38,'g':None}
        B = {'a':17,'b':18,'c':32,'d':33,'e':19,'f':34,'g':16}
        C = {'a':28,'b':29,'c':14,'d':12,'e':27,'f':13,'g':30}
        D = {'a': 9,'b':10,'c':24,'d':25,'e':11,'f':26,'g': 8}

        displays = [A,B,C,D]
        

        total = 0

        for i in range(len(digits)):
            digit = digits[i]
            disp = displays[i]
            for bar in digit:
                if disp[bar]:
                    total += 2**disp[bar]

        return total

    def _get_char(self,chars):
        char_dict = {'0':'acdefg','1':'fd','2':'cfbea','3':'abcdf','4':'gdfb','5':'cgbda','6':'cgeadb','7':'cfd','8':'abcdefg','9':'abcdfg','A':'bcdefg','a':'abcdef','b':'abdeg','c':'eab','C':'cgea','d':'abdef','E':'abceg','F':'egbc','G':'cgead','H':'egbdf','h':'egbd','I':'fd','J':'afd','L':'gea','n':'ebd','O':'acdefg','o':'abed','P':'gecbf','q':'cbgfd','r':'eb','S':'cgbda','t':'geba','u':'ead','y':'gbfda','*':'gcbf'}

        dots = 2**22

        total = 0

        digits = []

        for char in chars:
            if char == ':':
                total += dots
            else:
                try:
                    digits.append(char_dict[char])
                except:
                    digits.append('')

        total += self._get_bin(digits)

        if self.alarm:
            total += 2**6
        if self.sound:
            total += 2**4
        if self.snooze:
            total += 2**5
        if self.home:
            total += 2**3

        return total

    def _get_time(self,chars):
        if chars[0] == '0':
            chars = ' ' + chars[1:]
        return self._get_char(chars)

    def _get_temp(self,temp):
        #chars = '%.1f'%temp + 'c'
        #chars = chars.replace('.','')
        chars = '%.0f'%temp + '*C'
        return self._get_char(chars)


if __name__ == '__main__':

    from time import localtime, strftime
    reg = register(27,22,4,17)
    my_display = display()

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
            r1.switch()
        elif channel == 23:
            r2.switch()

    def temp(channel):
        tfile = open("/sys/bus/w1/devices/28-0000039bddd2/w1_slave")
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = (temperature / 1000) - 3.5
        if not temperature == 0:
            num = my_display._get_temp(temperature)
            reg.set(num)


    bounce = 400

    GPIO.add_event_detect(11, GPIO.RISING, callback=switch, bouncetime=bounce)
    GPIO.add_event_detect(7, GPIO.RISING, callback=hello, bouncetime=bounce)
    GPIO.add_event_detect(8, GPIO.RISING, callback=hello, bouncetime=bounce)
    GPIO.add_event_detect(25, GPIO.RISING, callback=hello, bouncetime=bounce)
    GPIO.add_event_detect(24, GPIO.RISING, callback=temp, bouncetime=bounce)
    GPIO.add_event_detect(23, GPIO.RISING, callback=switch, bouncetime=bounce)

    reg.set(2**40-1)
    time = '00:00'
    num = my_display._get_time(time)
    reg.set(num)  
    sleep(1)

    while True:
        now = strftime("%H:%M", localtime())
        print now
        if now == time:
            pass
        else:
            time = now
            num = my_display._get_time(time)
            reg.set(num)
        sleep(1)
