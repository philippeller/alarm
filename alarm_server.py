#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import Pyro4
import time

class alarm(object):
    def __init__(self):
        self._set = False
        self._playing = False
        self._snoozing = False
        self._counter = 0
        self._time = None

    def reset(self):
        self.__init__()

    @Pyro4.expose
    @property
    def set(self):
        return self._set

    @Pyro4.expose
    @property
    def playing(self):
        return self._playing

    @Pyro4.expose
    @property
    def snoozing(self):
        return self._snoozing

    @Pyro4.expose
    @property
    def counter(self):
        return self._counter

    @Pyro4.expose
    @property
    def time(self):
        return self._time

    def snooze(self):
        self._snooze = True
        self._counter += 1

    def play(self):
        self._playing = True

    def stop(self):
        self._playing = False
        self._snoozing = False
        self._counter = 0

    def set_time(self, settime):
        self._set = True
        self._time = [int(i) for i in settime.split(':')]
        print 'waking at %s:%s'%(self.time[0],self.time[1])

    def check_alarm(self):
        if self._set:
            return self.time == [time.localtime().tm_hour,time.localtime().tm_min]
        else:
            return False

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
uri = daemon.register(alarm())
ns.register("alarm", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()

