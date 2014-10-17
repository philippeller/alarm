import Pyro4
ns = Pyro4.locateNS(host='muffin',port=9090)

lights_uri = ns.lookup('lights')
lights = Pyro4.Proxy(lights_uri)

uri = ns.lookup('itunes')
itunes = Pyro4.Proxy(uri)

uri = ns.lookup('projector')
projector = Pyro4.Proxy(uri)

uri = ns.lookup('alarm')
alarm = Pyro4.Proxy(uri)

uri = ns.lookup('relay')
relay = Pyro4.Proxy(uri)


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

@pool
def wake(self):
    self.counter = 0
    #set system volume
    os.system('osascript -e "set volume 2.5"')
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
    self.counter = 0
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
    self.counter = 0
    print 'alarm off'
    self.player.pause()
    self.relay.power_off()
    self.player.volume = self.vol
    self.alarm_on = False
    self.alarm_set = False


