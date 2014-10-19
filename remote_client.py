import Pyro4
import subprocess, sys
ns = Pyro4.locateNS(host='muffin',port=9090)

itunes_uri = ns.lookup('itunes')
alarm_uri = ns.lookup('alarm')
relay_uri = ns.lookup('relay')

NEXT = "0x18 depressed"
PREV = "0x19 depressed"
PLAY_PAUSE = "0x17 depressed"
VOL_UP = "01f depressed"
VOL_DOWN = "0x20 depressed"
MENU = "0x16 depressed"
    
proc = subprocess.Popen(
    './iremoted',
   shell=True,
   stdout=subprocess.PIPE,
   stderr=subprocess.PIPE,
)
while proc.poll() is None:
    output = proc.stdout.readline()
    event = output[:-1]

    if event == MENU:
        with Pyro4.Proxy(alarm_uri) as alarm:
            if alarm.playing:
                alarm.stop()
            else:
                with Pyro4.Proxy(itunes_uri) as itunes:
                    if itunes.status == 'playing':
                        itunes.pause()
                with Pyro4.Proxy(relay_uri) as relay:
                    relay.set_state(not relay.state)

    if event == PLAY_PAUSE:
        with Pyro4.Proxy(alarm_uri) as alarm:
            if alarm.playing:
                alarm.snooze()
            else:
                with Pyro4.Proxy(itunes_uri) as itunes:
                    if itunes.status == 'paused':
                        with Pyro4.Proxy(relay_uri) as relay:
                            if not relay.state:
                                relay.set_state(not relay.state)
