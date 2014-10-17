#!/usr/bin/python
# -*- coding: utf-8 -*-
import Pyro4
import sys
import signal
import time
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import thread

PORT_NUMBER = 8888
ns = Pyro4.locateNS(host='muffin',port=9090)

uri_lights = ns.lookup('lights')
uri_itunes = ns.lookup('itunes')
uri_projector = ns.lookup('projector')
uri_alarm = ns.lookup('alarm')
uri_relay = ns.lookup('relay')


class myHandler(BaseHTTPRequestHandler):
    #Handler for the GET requests
    def do_GET(self):

        with Pyro4.Proxy(uri_alarm) as alarm:
            if not alarm.set:
                message = 'no alarm set'
            else:
                message = 'set to {0}:{1}'.format(*alarm.time)

        with Pyro4.Proxy(uri_relay) as relay:
            if relay.state:
                status_audio = 'off'
            else:
                status_audio = 'on'

        with Pyro4.Proxy(uri_lights) as lights:
            Bar_on = lights.any_all('Bar')
            Bed_on = lights.any_all('Bed')
            Sofa_on = lights.any_all('Sofa')
            if Bed_on:
                status_Bed = 'off'
            else:
                status_Bed = 'on'
            if Sofa_on:
                status_Sofa = 'off'
            else:
                status_Sofa = 'on'
            if Bar_on:
                status_Bar = 'off'
            else:
                status_Bar = 'on'

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
                <td bgcolor="#FFFF99">Bed<br /><input type="submit" name='Bed' value=%(status_Bed)s /></td>
                <td bgcolor="#FFFF99">Sofa<br /><input type="submit" name='Sofa' value=%(status_Sofa)s /></td>
                <td bgcolor="#FFFF99">Bar<br /> <input type="submit" name='Bar' value=%(status_Bar)s /></td>
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
            '''%{'message':message,'status_audio':status_audio,'status_Bed':status_Bed,'status_Sofa':status_Sofa,'status_Bar':status_Bar})
            return
        #except IOError:
        except:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):

        if self.path=="/set":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })

            try:
                if (form["alarm"].value=="set"):
                    with Pyro4.Proxy(uri_alarm) as alarm:
                        try:
                            alarm_time = form["time"].value
                            print 'got request to set alarm to %s'%alarm_time
                            alarm.set_time(alarm_time)
                        except:
                            pass
                if (form["alarm"].value=="cancel"):
                    with Pyro4.Proxy(uri_alarm) as alarm:
                        alarm.reset()
                        print 'got request to cancel alarm'
            except KeyError:
                pass
           
            try:
                with Pyro4.Proxy(uri_lights) as lights:
                    if (form['lights'].value == "on"):
                        lights.on()
                    if (form['lights'].value == "off"):
                        lights.off()
            except KeyError:
                pass

            for light in ['Bar','Bed','Sofa']:
                try:
                    with Pyro4.Proxy(uri_lights) as lights:
                        if (form[light].value == "on"):
                            lights.on(light)
                        if (form[light].value == "off"):
                            lights.off(light)
                except KeyError:
                    pass


            #def switch(name,var):
            #    try:
            #        if (form[name].value == "on"):
            #            exec('%s = True'%var) in globals()
            #            print 'got request to turn on %s'%name
            #        if (form[name].value == "off"):
            #            exec('%s = False'%var) in globals()
            #            print 'got request to turn off %s'%name
            #    except KeyError:
            #        pass

            #def change(name,var,state):
            #    try:
            #        if (form[name].value == state):
            #            exec('%s = True'%var) in globals()
            #            print 'got request to turn %s %s'%(state,name)
            #    except KeyError:
            #        pass

            #change('lights','lights_on','on')
            #change('lights','lights_off','off')

            #change('video','beamer_on','on')
            #change('video','beamer_off','off')

            #change('presets','relax','relax')
            #change('presets','dimm','dimm')
            #change('presets','work','work')
            #change('presets','read','read')
            #change('presets','cinema','cinema')
            #change('presets','goodnight','goodnight')
            #change('presets','shutdown','shutdown')

            #change('audio','relay_request','on')
            #change('audio','relay_request','off')

            #switch('Bed','Bed_on')
            #switch('Sofa','Sofa_on')
            #switch('Bar','Bar_on')

            ##Redirect the browser on the main page 
            self.send_response(302)
            self.send_header('Location','/')
            self.end_headers()
            return


server = HTTPServer(('muffin', PORT_NUMBER), myHandler)
print 'Started httpserver on port ' , PORT_NUMBER

try:
    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
