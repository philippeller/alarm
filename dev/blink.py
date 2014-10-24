#!/usr/bin/python
import RPi.GPIO as GPIO
from time import sleep
import signal
import sys
import random

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

leds = [22,23,24,25]

def signal_handler(signal, frame):
    print '\nciao!'
    for led in leds:
        GPIO.output(led,False)
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

for led in leds:
    GPIO.setup(led,GPIO.OUT)
    GPIO.output(led,True)

pattern = [22,23,24,25,24,23]

while True:
    for led in pattern:
        GPIO.output(random.randint(22,25),random.randint(0,1))
        sleep(random.randint(1,100)/500.)
