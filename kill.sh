#!/bin/bash
echo 'killing running servers'
kill $(ps aux | grep '[p]ython /usr/local/bin/pyro4-ns' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./itunes_server.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./light_server.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./projector_server.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./relay_server.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./alarm_server.py' | awk '{print $2}')
