#!/bin/bash
echo 'killing running servers'
kill $(ps aux | grep '[/]usr/bin/python /usr/local/bin/pyro4-ns' | awk '{print $2}')
kill $(ps aux | grep '[/]usr/bin/python ' | awk '{print $2}')
kill $(ps aux | grep '[/]usr/bin/python ./itunes_server.py' | awk '{print $2}')
kill $(ps aux | grep '[/]usr/bin/python ./light_server.py' | awk '{print $2}')
kill $(ps aux | grep '[/]usr/bin/python ./projector_server.py' | awk '{print $2}')
kill $(ps aux | grep '[/]usr/bin/python ./relay_server.py' | awk '{print $2}')
kill $(ps aux | grep '[/]usr/bin/python ./alarm_server.py' | awk '{print $2}')
sleep 1
#spawn servers
pyro4-ns -n muffin  &
./itunes_server.py &
./light_server.py &
./projector_server.py &
./relay_server.py &
./alarm_server.py &