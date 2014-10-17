#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Pyro4
 
class itunes(object):

    def __init__(self):
        self._vol = 50
        self._status = 'paused'
        
    def play_playlist(self,name):
        pass

    @Pyro4.expose
    @property
    def status(self):
        return self._status
    
    @Pyro4.expose
    @property
    def current_track(self):
        return 'track'
   
    @Pyro4.expose
    @property
    def current_artist(self):
        return 'artist'

    @Pyro4.expose
    @property
    def current_album(self):
        return 'album'

    @Pyro4.expose
    @property
    def volume(self):
        return self._vol

    @Pyro4.expose
    @volume.setter
    def volume(self, level):
        self._vol = level
        
    def pause(self):
        self._status = 'paused'
    
    def play(self):
        self._status = 'playing'
    
    def next(self):
        pass

    def previous(self):
        pass

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
uri = daemon.register(itunes())
ns.register("itunes", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()
