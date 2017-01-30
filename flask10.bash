#!/bin/bash

# flask10.bash

# This script should run a python script which then starts a web server.

export FLASK_DEBUG=1
export PORT=5010
~/anaconda3/bin/python keras10.py

# curl localhost:5000/k10/SPY/2016/25

exit
