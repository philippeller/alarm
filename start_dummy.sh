#!/bin/bash
./kill_dummy.sh
sleep 1
#spawn dummys
pyro4-ns -n muffin  &
./itunes_dummy.py &
./light_dummy.py &
./projector_dummy.py &
./relay_dummy.py &
./alarm_dummy.py &
