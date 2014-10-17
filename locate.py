import Pyro4
ns = Pyro4.locateNS(host='muffin',port=9090)

uri = ns.lookup('lights')
lights = Pyro4.Proxy(uri)

uri = ns.lookup('itunes')
itunes = Pyro4.Proxy(uri)

uri = ns.lookup('projector')
projector = Pyro4.Proxy(uri)

uri = ns.lookup('alarm')
alarm = Pyro4.Proxy(uri)

uri = ns.lookup('relay')
relay = Pyro4.Proxy(uri)
