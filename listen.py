#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..","..","Sources"))
from yocto_api import *
from yocto_relay import *
from iremote import IRemote
from iTunes import *
import signal
import time
from threading import Timer
from Foundation import *
from threading import Thread
#ToDo: make sure iTunes is running for Wecker

#def handler(signum, frame):
#    #cleanup_stop_thread()
#    alarm.exit()
#    iremote.exit()
#    try:
#       t.cancel()
#    except:
#        pass
#    print 'bye bye!'
#    sys.exit()

#signal.signal(signal.SIGINT, handler)

#pool decorator
def pool(fn):
    def pool_wrapper(*args,**kwargs):
        pool = NSAutoreleasePool.alloc().init()
        fn(*args,**kwargs)
        del pool
    return pool_wrapper

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

class sleeptimer(object):
    def __init__(self,player,relay):
        self.active = False
        self.player = player
        self.relay = relay

    @pool
    def ramp_down(self):
        vol = int(self.player.volume)
        for i in range(vol,-1,-1):
            self.player.volume = int(i)
            time.sleep(1)
        self.player.pause()
        self.relay.power_off()
        #restore
        self.active = False
        self.player.volume = vol

class wecker(Thread):
    def __init__(self,player,relay):
        Thread.__init__(self)
        self.alarm_on = False
        self.player = player
        self.relay = relay
        self.alarm_set = False
        self.snoozing = False

    def set_time(self, settime):
        self.alarm_set = True
        self.time = [int(i) for i in settime.split(':')]
        print 'waking at %s:%s'%(self.time[0],self.time[1])

    def run(self):
        while True:
            if self.alarm_set and not self.alarm_on and not self.snoozing:
                if self.check_time():
                    self.wake()
            time.sleep(10)

    def check_time(self):
        return self.time == [time.localtime().tm_hour,time.localtime().tm_min]

    @pool
    def wake(self):
        #set system volume
        os.system('osascript -e "set volume 3"')
        self.player.pause()
        print 'good morning!'
        self.alarm_on = True
        self.relay.power_on()
        time.sleep(3)
        self.vol = int(self.player.volume)
        self.player.volume = 0
        self.player.play_playlist('morning')
        for i in range(0,100):
            self.player.volume = int(i)
            time.sleep(0.05)

    @pool
    def snooze(self, minutes):
        self.alarm_set = False
        self.snoozing = True
        print 'snoozing -.-'
        for i in range(int(minutes*60)):
            if self.alarm_on:
                time.sleep(1)
            else:
                return False
        self.relay.power_on()
        self.player.volume = 0
        self.player.play()
        for i in range(0,100):
            self.player.volume = int(i)
            time.sleep(0.02)
        self.alarm_on = True
        self.snoozing = False

    @pool
    def stop_alarm(self):
        print 'alarm off'
        self.player.pause()
        self.relay.power_off()
        self.player.volume = self.vol
        self.alarm_on = False
        self.alarm_set = False

@pool
def my_iremote_handler(event):
    if event == IRemote.MENU:
        try:
            t.cancel()
            print 'timer canceled'
        except:
            pass
        if alarm.alarm_on:
            alarm.alarm_on = False
            alarm.stop_alarm()
        else:
            if player.status == 'playing':
                player.pause()
            theRelay.switch_state()

    if event == IRemote.PLAY_PAUSE:
        if alarm.alarm_on:
            alarm.snooze(7)
        else:
            if not theRelay.state and player.status == 'paused': theRelay.power_on()

iremote = IRemote()
iremote.add_listener(my_iremote_handler)
iremote.start()
theRelay = relay()
player = iTunes()
alarm = wecker(player,theRelay)
alarm.start()
theTimer = sleeptimer(player,theRelay)
print 'Remote catch up and running'

while True:
    inp = raw_input('>> ')
    listinp = inp.split(' ')
    if listinp[0] == '-T':
        theTimer.active = True
        t = Timer(float(listinp[1])*60 ,theTimer.ramp_down)
        t.start()
    if listinp[0] == '-C':
        try:
            t.cancel()
            print 'timer cacled'
        except:
            pass
        if alarm.alarm_set:
            alarm.alarm_set = False
            print 'alarm cacled'
    if listinp[0] == '-A':
        alarm.set_time(listinp[1])
    if listinp[0] == 'on':
        theRelay.power_on()
    if listinp[0] == 'off':
        theRelay.power_off()
