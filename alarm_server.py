#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import cgi
import thread
import time

PORT_NUMBER = 8080

on = False
Atime = '3:33'
#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):



    
    #Handler for the GET requests
    def do_GET(self):

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
            <title>Alarm Clock</title>
            </header>
            <h1>Alarm Clock</h1>
            <p>
            wake-up time is %s:
            </p>
            <form method="POST" action="/set">
            <input name="time" type="text" size="30" value="%s" maxlength="30"/>
            <input type="submit" name='cmd' value="set alarm clock"/>
            <input type="submit" name='cmd' value="on/off"/>
            </form>
            </body>
            </html> 
            '''%(Atime,Atime))
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    #Handler for the POST requests
    def do_POST(self):
        global Atime
        global on
        if self.path=="/set":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            print form["cmd"].value
            if (form["cmd"].value=="set alarm clock"):
                try:
                    Atime = form["time"].value
                except:
                    pass
            if (form["cmd"].value=="on/off"):
                if on:
                    on = False
                else:
                    on = True

            #Redirect the browser on the main page 
            self.send_response(302)
            self.send_header('Location','/')
            self.end_headers()
            return          
            
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

# Use the L1 led on Daisy11 module
#ledL1=ablib.Daisy11("D2","L1")

#Forever loop
while True:
    try:
        print on
        print Atime
    except:
        pass
    time.sleep(2)
#    # Check the blink flag
#    if blink==True: 
#        #ledL1.on()i
#        print 'x'
#        time.sleep(2)
#        #ledL1.off()
#        print 'o'
#        time.sleep(2)
#    else: 
#        pass
#        #ledL1.off()
