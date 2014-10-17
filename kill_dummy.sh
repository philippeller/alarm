#!/bin/bash
echo 'killing running dummies'
kill $(ps aux | grep '[p]ython /usr/local/bin/pyro4-ns' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./itunes_dummy.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./light_dummy.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./projector_dummy.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./relay_dummy.py' | awk '{print $2}')
kill $(ps aux | grep '[p]ython ./alarm_dummy.py' | awk '{print $2}')
