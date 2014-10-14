# -*- coding: utf-8 -*-
from Foundation import *
from ScriptingBridge import *
import Pyro4
from pool import pool
 
class itunes(object):
        
    def __init__(self):
        self.app = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
        self.playlists = self.app.sources()[0].playlists()
        self.playlist_names = [item.name() for item in self.playlists]

    @pool
    def play_playlist(self,name):
        try:
            index = self.playlist_names.index(name)
        except:
            return False
        #maybe?
        try:
            self.currentPlaylist.shuffle = True
        except:
            pass
        self.playlists[index].playOnce_(False)
        return True

    @Pyro4.expose
    @property
    def status(self):
        NSAutoreleasePool.alloc().init()
        if self.app.playerState() == 1800426320:
            return "playing"
        elif self.app.playerState() == 1800426352:
            return "paused"
        else:
            return "unknown"
    
    @Pyro4.expose
    @property
    def current_track(self):
        NSAutoreleasePool.alloc().init()
        return self.app.currentTrack().name()
   
    @Pyro4.expose
    @property
    def current_artist(self):
        NSAutoreleasePool.alloc().init()
        return self.app.currentTrack().artist()

    @Pyro4.expose
    @property
    def current_album(self):
        NSAutoreleasePool.alloc().init()
        return self.app.currentTrack().album()

    @Pyro4.expose
    @property
    def volume(self):
        NSAutoreleasePool.alloc().init()
        return self.app.soundVolume()

    @Pyro4.expose
    @volume.setter
    def volume(self, level):
        NSAutoreleasePool.alloc().init()
        self.app.setSoundVolume_(level)
        
    @pool
    def pause(self):
        self.app.pause()
    
    @pool
    def play(self):
        if self.status == "paused":
            self.app.playpause()
    
    @pool
    def next(self):
        self.app.nextTrack()

    @pool
    def previous(self):
        self.app.previousTrack()

daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
uri = daemon.register(itunes())
ns.register("itunes", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()
