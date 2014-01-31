import serial
import time
class projector():
    def __init__(self):
        self.ser = serial.Serial('/dev/tty.usbserial', 9600, timeout=1)
        #self.stat = 'PWR=00'
    def _send(self, msg):
        self.ser.write('%s\r'%msg)
        #time.sleep(0.5)
        #lines = self.ser.readlines()
        #print lines
        #line = lines[-1]
        #line.strip('\r:')
        #print line
        #return line
    def on(self):
        #self.stat = 
        self._send('PWR ON')
    def off(self):
        #self.stat = 
        self._send('PWR OFF')
    #def switch(self):
    #    if self.stat == 'PWR=00':
    #        self.on()
    #    else:
    #        self.off()

if __name__=='__main__':
    beamer = projector()
