#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import Pyro4
import time
from threading import Thread

class clock(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.alarm_on = False
        self.alarm_set = False
        self.snoozing = False
        self.ns = Pyro4.locateNS(host='muffin',port=9090)
        self.uri_relay = self.ns.lookup('relay')
        self.uri_itunes = self.ns.lookup('itunes')
        self.counter = 0

    def set_time(self, settime):
        self.alarm_set = True
        self.time = settime

    def run(self):
        while True:
            if self.alarm_set and not self.alarm_on and not self.snoozing:
                if self.check_time():
                    self.wake()
            if self.alarm_on:
                self.counter += 1
            #safety feature
            if self.counter > 100:
                self.stop_alarm()
            time.sleep(10)

    def check_time(self):
        return self.time == [time.localtime().tm_hour,time.localtime().tm_min]

    def wake(self):
        self.counter = 0
        #set system volume
        os.system('osascript -e "set volume 2.5"')
        with Pyro4.Proxy(self.uri_itunes) as itunes:
            itunes.pause()
        print 'good morning!'
        self.alarm_on = True
        with Pyro4.Proxy(self.uri_relay) as relay:
            relay.set_state(True)
        time.sleep(3)
        with Pyro4.Proxy(self.uri_itunes) as itunes:
            self.vol = int(itunes.volume)
            itunes.volume = 0
            itunes.play_playlist('morning')
            for i in range(0,100):
                itunes.volume = int(i)
                time.sleep(0.05)

    def snooze(self, minutes):
        self.counter = 0
        self.alarm_set = False
        self.snoozing = True
        print 'snoozing -.-'
        for i in range(int(minutes*60)):
            if self.alarm_on:
                time.sleep(1)
            else:
                return False
        with Pyro4.Proxy(self.uri_relay) as relay:
            relay.set_state(True)
        with Pyro4.Proxy(self.uri_itunes) as itunes:
            itunes.volume
            itunes.volume = 0
            itunes.play()
            for i in range(0,100):
                itunes.volume = int(i)
                time.sleep(0.02)
        self.alarm_on = True
        self.snoozing = False

    def stop_alarm(self):
        self.counter = 0
        if self.alarm_on:
            print 'alarm off'
            with Pyro4.Proxy(self.uri_itunes) as itunes:
                itunes.pause()
            with Pyro4.Proxy(self.uri_relay) as relay:
                relay.set_state(False)
            with Pyro4.Proxy(self.uri_itunes) as itunes:
                itunes.volume
                itunes.volume = self.vol
            self.alarm_on = False

    def stop(self):
            self.stopped = True

class alarm(object):
    def __init__(self):
        self._set = False
        self._playing = False
        self._snoozing = False
        self._time = None
        self.clock = clock()
        self.clock.start()

    def reset(self):
        self.clock.stop_alarm()
        self.clock.alarm_set = False
        self.clock.stop()
        del self.clock
        self.__init__()

    def stop(self):
        self.clock.stop()

    @Pyro4.expose
    @property
    def playing(self):
        return self.clock.alarm_on

    @Pyro4.expose
    @property
    def set(self):
        return self._set

    @Pyro4.expose
    @property
    def snoozing(self):
        return self._snoozing

    @Pyro4.expose
    @property
    def time(self):
        return self._time

    def snooze(self):
        self._snoozing = True
        self.clock.snooze(7)

    def stop(self):
        self._playing = False
        self._snoozing = False
        self.clock.stop_alarm()

    def set_time(self, settime):
        self._set = True
        self._time = [int(i) for i in settime.split(':')]
        self.clock.set_time(self._time)
        print 'waking at %s:%s'%(self.time[0],self.time[1])

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
uri = daemon.register(alarm())
ns.register("alarm", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()


