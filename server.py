#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from iremote import IRemote
from iTunes import *
import signal
import time
from threading import Timer
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import thread
from pool import pool
from relay import relay
from wecker import wecker
from sleeptimer import sleeptimer
from projector import projector
from phue import my_hue

PORT_NUMBER = 8080

relay_state = False
relay_request = False
alarm_on = False
alarm_set = False
alarm_time = '00:00'
beamer_on = False
beamer_off = False
lights_on = False
lights_off = False
bed_on = False
sofa_on = False
bar_on = False
relax = False
dimm = False
read = False
work = False
cinema = False
dinner = False
shutdown = False
goodnight = False

class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):
        if not alarm_set:
            message = 'no alarm set'
        else:
            message = 'set to %s'%alarm_time
        if relay_state:
            status_audio = 'off'
        else:
            status_audio = 'on'
        if bed_on:
            status_bed = 'off'
        else:
            status_bed = 'on'
        if sofa_on:
            status_sofa = 'off'
        else:
            status_sofa = 'on'
        if bar_on:
            status_bar = 'off'
        else:
            status_bar = 'on'

        try:
            mimetype='text/html'
            self.send_response(200)
            self.send_header('Content-type',mimetype)
            self.end_headers()
            self.wfile.write('''
            <html>
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
            </head>
            <header>
            <title>Remote</title>
            </header>
            <h1>Remote</h1>
            <form method="POST" action="/set">
            <!--Alarm-->
            <table width="320" border="0">
              <tr>
                <td colspan="4" bgcolor="#6699FF"><strong>Alarm Clock</strong></td>
              </tr>
              <tr>
                <td bgcolor="#6699FF"><input name="time" type="text" size="5" maxlength="5"/></td>
                <td bgcolor="#6699FF"><input type="submit" name='alarm' value="set"/></td>
                <td bgcolor="#6699FF"><input type="submit" name='alarm' value="cancel"/></td>
                <td bgcolor="#6699FF">%(message)s</td>
              </tr>
            <!--Audio/Video-->
              <tr>
                <td colspan="4"><strong>Entertainment</strong></td>
              </tr>
              <tr>
                <td>Audio</td>
                <td><input type="submit" name='audio' value=%(status_audio)s /></td>
                <td>Video</td>
                <td><input type="submit" name='video' value="on"/> <input type="submit" name='video' value="off"/></td>
              </tr>
            <!--all Light-->
              <tr>
                <td colspan="4" bgcolor="#FFFF99"><strong>Lights</strong></td>
              </tr>
              <tr>
                <td bgcolor="#FFFF99">All<br /><input type="submit" name='lights' value="on"/> <input type="submit" name='lights' value="off"/></td>
                <td bgcolor="#FFFF99">Bed<br /><input type="submit" name='bed' value=%(status_bed)s /></td>
                <td bgcolor="#FFFF99">Sofa<br /><input type="submit" name='sofa' value=%(status_sofa)s /></td>
                <td bgcolor="#FFFF99">Bar<br /> <input type="submit" name='bar' value=%(status_bar)s /></td>
              </tr>
              <tr>
                <td colspan="4" bgcolor="#CCCCCC"><strong>Presets</strong></td>
              </tr>
              <tr>
                <td bgcolor="#CCCCCC"><input type="submit" name='presets' value="normal"/></td>
                <td bgcolor="#CCCCCC"><input type="submit" name='presets' value="work"/></td>
                <td bgcolor="#CCCCCC"><input type="submit" name='presets' value="relax"/></td>
                <td bgcolor="#CCCCCC"><input type="submit" name='presets' value="dimm"/></td>
              </tr>
              <tr>
                <td bgcolor="#CCCCCC"><input type="submit" name='presets' value="goodnight"/></td>
                <td bgcolor="#CCCCCC"><input type="submit" name='presets' value="read"/></td>
                <td bgcolor="#CCCCCC"><input type="submit" name='presets' value="cinema"/></td>
                <td bgcolor="#CCCCCC"><input type="submit" name='presets' value="shutdown"/></td>
              </tr>
            </table>

            </form>
            </body>
            </html> 
            '''%{'message':message,'status_audio':status_audio,'status_bed':status_bed,'status_sofa':status_sofa,'status_bar':status_bar})
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        global relay_state 
        global relay_request
        global alarm_set
        global alarm_time
        global beamer_on
        global beamer_off
        global lights_on
        global lights_off
        global bed_on
        global sofa_on
        global bar_on
        global relax
        global dimm
        global read 
        global work 
        global cinema 
        global dinner 
        global shutdown
        global goodnight

        if self.path=="/set":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })

            try:
                if (form["alarm"].value=="set"):
                    if not alarm_set:
                        try:
                            alarm_time = form["time"].value
                            print 'got request to set alarm to %s'%alarm_time
                            alarm_set = True
                        except:
                            pass
                if (form["alarm"].value=="cancel"):
                        alarm_set = False
                        print 'got request to cancel alarm'
            except KeyError:
                pass

            def switch(name,var):
                try:
                    if (form[name].value == "on"):
                        exec('%s = True'%var) in globals()
                        print 'got request to turn on %s'%name
                    if (form[name].value == "off"):
                        exec('%s = False'%var) in globals()
                        print 'got request to turn off %s'%name
                except KeyError:
                    pass

            def change(name,var,state):
                try:
                    if (form[name].value == state):
                        exec('%s = True'%var) in globals()
                        print 'got request to turn %s %s'%(state,name)
                except KeyError:
                    pass

            change('lights','lights_on','on')
            change('lights','lights_off','off')

            change('video','beamer_on','on')
            change('video','beamer_off','off')

            change('presets','relax','relax')
            change('presets','dimm','dimm')
            change('presets','work','work')
            change('presets','read','read')
            change('presets','cinema','cinema')
            change('presets','goodnight','goodnight')
            change('presets','shutdown','shutdown')

            change('audio','relay_request','on')
            change('audio','relay_request','off')

            switch('bed','bed_on')
            switch('sofa','sofa_on')
            switch('bar','bar_on')

            #Redirect the browser on the main page 
            self.send_response(302)
            self.send_header('Location','/')
            self.end_headers()
            return


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

#This is a thread that runs the web server 
def WebServerThread():
    try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Started httpserver on port ' , PORT_NUMBER

        #Wait forever for incoming htto requests
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()


# Runs the web server thread
thread.start_new_thread(WebServerThread,())
iremote = IRemote()
iremote.add_listener(my_iremote_handler)
iremote.start()
theRelay = relay()
player = iTunes()
alarm = wecker(player,theRelay)
alarm.start()
beamer = projector()
room = my_hue()
#theTimer = sleeptimer(player,theRelay)
print 'Remote catch up and running'

while True:
    try:
        if alarm_set and not alarm.alarm_set:
            alarm.set_time(alarm_time)
            #alarm_set = True
            #alarm_on = True
        if not alarm_set and alarm.alarm_set:
            alarm.alarm_set = False
            print 'alarm caceled'
            #alarm_set = False
        alarm_set = alarm.alarm_set

        if relay_request:
            theRelay.switch_state()
            relay_state = theRelay.state
            relay_request = False

        if beamer_on:
            beamer.on()
            beamer_on = False
        if beamer_off:
            beamer.off()
            beamer_off = False

        if lights_on == True and room.status != True:
            bed_on = True
            sofa_on = True
            bar_on = True
            lights_on = False
            room.set('all',on=True)

        if lights_off == True and room.status != False:
            bed_on = False
            sofa_on = False
            bar_on = False
            lights_off = False
            room.set('all',on=False)

        if not bed_on == room.status('Bed'):
            room.set('Bed',on=bed_on)

        if not sofa_on == room.status('Sofa'):
            room.set('Sofa',on=sofa_on)

        if not bar_on == room.status('Bar'):
            room.set('Bar',on=bar_on)

        if work:
            bed_on = True
            sofa_on = True
            bar_on = True
            room.set('all',on=True,brightness=254,colortemp_k=3800)
            work = False

        if read:
            bed_on = False
            sofa_on = True
            bar_on = False
            room.set('Sofa',on=True,brightness=200,colortemp_k=3000)
            room.set('Bed',on=False)
            room.set('Bar',on=False)
            read = False

        if relax:
            bed_on = True
            sofa_on = True
            bar_on = True
            room.set('all',on=True,brightness=254,colortemp_k=2700)
            relax = False

        if dimm:
            room.set('all',brightness=100)
            dimm = False

        if cinema:
            bed_on = False
            sofa_on = True
            bar_on = True
            room.set('Bed',on=False)
            room.set('Sofa',on=True,brightness=50,colortemp_k=2500)
            room.set('Bar',on=True,brightness=50,colortemp_k=2500)
            beamer.on()
            relay_state = True
            theRelay.power_on()
            cinema = False

        if goodnight:
            beamer_off = True
            lights_off = True
            relay_state = False
            theRelay.power_off()
            goodnight = False

        if shutdown:
            beamer_off = True
            alarm_set = False
            lights_off = True
            relay_state = False
            theRelay.power_off()
            shutdown = False

        time.sleep(1)
    except:
        pass
    # try:
    #     inp = raw_input('>> ')
    #     listinp = inp.split(' ')
    #     if listinp[0] == '-T':
    #         theTimer.active = True
    #         t = Timer(float(listinp[1])*60 ,theTimer.ramp_down)
    #         t.start()
    #     if listinp[0] == '-C':
    #         try:
    #             t.cancel()
    #             print 'timer cacled'
    #         except:
    #             pass
    #         if alarm.alarm_set:
    #             alarm.alarm_set = False
    #             print 'alarm cacled'
    #     if listinp[0] == '-A':
    #         alarm.set_time(listinp[1])
    #     if listinp[0] == 'on':
    #         theRelay.power_on()
    #     if listinp[0] == 'off':
    #         theRelay.power_off()
    # except KeyboardInterrupt:
    #     try:
    #         t.cancel()
    #         alarm.stop()
    #     except:
    #         pass
    #     sys.exit(0)
