#!/usr/bin/env sh
DIR=$(dirname $0)
export PYTHONPATH=$PYTHONPATH:$DIR/../
python3 $DIR/RpiServer.py
