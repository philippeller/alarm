#!/bin/bash
echo 'killing running servers'
./kill.sh
sleep 1
#spawn servers
pyro4-ns -n muffin  &
./itunes_server.py &
./light_server.py &
./projector_server.py &
./relay_server.py &
./alarm_server.py &
