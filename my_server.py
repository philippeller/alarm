import Pyro4

class my_room(object):
    def __init__(self):
        self._audio = False

    @Pyro4.expose
    @property
    def audio(self):
        return self._audio

    @Pyro4.expose
    @audio.setter
    def audio(self,val):
        print 'setting'
        self._audio = val


daemon = Pyro4.Daemon(host='muffin')
ns = Pyro4.locateNS()
ns.list()
uri = daemon.register(my_room())
ns.register("my_room", uri)
print("server object uri:", uri)
print("attributes server running.")
daemon.requestLoop()
