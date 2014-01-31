import time
from pool import pool

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

