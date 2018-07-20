#!/bin/bash

port=12060
mazeDim=100

python server.py $port $mazeDim &
sleep 1

python client.py 1 $port $mazeDim &
python client.py 2 $port $mazeDim &
python client.py 3 $port $mazeDim &
python client.py 4 $port $mazeDim