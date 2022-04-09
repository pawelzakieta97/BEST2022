#!/usr/bin/env sh
DIR=$(dirname $0)
export PYTHONPATH=$PYTHONPATH:$DIR/../
python $DIR/RpiServer.py
