#!/usr/bin/python
tfile = open("/sys/bus/w1/devices/28-0000039bddd2/w1_slave")
text = tfile.read() 
tfile.close()
secondline = text.split("\n")[1] 
temperaturedata = secondline.split(" ")[9] 
temperature = float(temperaturedata[2:]) 
temperature = temperature / 1000 
if not temperature == 0: print temperature
