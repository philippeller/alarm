#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_relay import *

def die(msg):
    sys.exit(msg+' (check USB cable)')

if len(sys.argv)<2 :  usage()

# Setup the API to use local USB devices
errmsg=YRefParam()
if YAPI.RegisterHub("usb", errmsg)!= YAPI.SUCCESS:
    sys.exit("init error"+errmsg.value)

# retreive any Relay
relay = YRelay.FirstRelay()
if relay is None: die('no device connected')

if not(relay.isOnline()):die('device not connected')

if state == 'A' :
    relay.set_state(YRelay.STATE_A)
else:
    relay.set_state(YRelay.STATE_B)
