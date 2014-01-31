# -*- coding: utf-8 -*-
import os,sys
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
        if self.relay is None: self._die('no device connected')
        if not(self.relay.isOnline()):self._die('device not connected')

    def _die(msg):
        sys.exit(msg+' (check USB cable)')

    @property
    def state(self):
        return self.relay.get_state()

    def switch_state(self):
        if self.state > 0:
            self.relay.set_state(YRelay.STATE_A)
        else:
            self.relay.set_state(YRelay.STATE_B)

    def power_off(self):
        self.relay.set_state(YRelay.STATE_A)

    def power_on(self):
        self.relay.set_state(YRelay.STATE_B)

