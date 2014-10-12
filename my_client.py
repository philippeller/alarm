import Pyro4

uri = 'PYRONAME:my_room'

my_room = Pyro4.Proxy(uri)
print my_room.audio
my_room.audio = True
print my_room.audio

