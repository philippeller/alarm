# -*- coding: utf-8 -*-
from Foundation import *
from ScriptingBridge import *
 
class iTunes(object):
    """
    A helper class for interacting with iTunes on Mac OS X via Scripting 
    Bridge framework.

    To use this, launch iTunes and make sure a playlist or an album is ready.
    
    Usage:
    
    >>> player = iTunes()
    >>> player.status
    'playing'
    >>> player.current_track
    u'Maison Rilax'
    >>> player.current_album
    u'Maison Rilax'
    >>> player.current_artist
    u'Lemonator'
    >>> player.pause()
    >>> player.status
    'paused'
    >>> player.play()
    >>> player.next()
    >>> player.current_track
    u'Not Your Game'

    """
        
    def __init__(self):
        self.app = SBApplication.applicationWithBundleIdentifier_("com.apple.iTunes")
        self.playlists = self.app.sources()[0].playlists()
        self.playlist_names = [item.name() for item in self.playlists]

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

    @property
    def status(self):
        if self.app.playerState() == 1800426320:
            return "playing"
        elif self.app.playerState() == 1800426352:
            return "paused"
        else:
            return "unknown"
    
    @property
    def current_track(self):
        return self.app.currentTrack().name()
   
    @property
    def current_artist(self):
        return self.app.currentTrack().artist()

    @property
    def current_album(self):
        return self.app.currentTrack().album()

    @property
    def volume(self):
        return self.app.soundVolume()

    @volume.setter
    def volume(self, level):
        self.app.setSoundVolume_(level)
        
    def pause(self):
        self.app.pause()
    
    def play(self):
        # According to AppleScript documentatin there should be a .play() 
        # method, but apparently there isn't. So we fake it :)
        if self.status == "paused":
            self.app.playpause()
    
    def next(self):
        self.app.nextTrack()

    def previous(self):
        self.app.previousTrack()
