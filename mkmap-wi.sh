#!/bin/bash

set -e

export PATH=/home/admin/bin:$PATH

WORKDIR="/home/admin/clones/ffmap-backend-wi"
WWWDIRINTERN="/var/www/meshviewer-intern-wi"
WWWDIREXTERN="/var/www/meshviewer-extern-wi"

if [ ! -d $WWWDIRINTERN/build/data ]; then
  mkdir $WWWDIRINTERN/build/data
fi

if [ ! -d $WWWDIREXTERN/build/data ]; then
  mkdir $WWWDIREXTERN/build/data
fi

cd "$(dirname "$0")"/

/usr/bin/python3 $WORKDIR/backend.py --with-rrd --prune 45 -m wiBAT:/var/run/alfred-wi.sock --vpn 02:00:0a:38:00:17 02:00:0a:38:00:07 02:00:0a:38:00:d0 02:00:0a:38:00:e7 02:00:0a:38:00:2a -d $WORKDIR/data/

/usr/bin/jq '.nodes = (.nodes | with_entries(del(.value.nodeinfo.owner)))' < $WORKDIR/data/nodes.json > $WORKDIR/data/nodes-internet.json
cp -r $WORKDIR/data/* $WWWDIRINTERN/build/data/

cp $WORKDIR/data/nodes-internet.json $WWWDIREXTERN/build/data/nodes.json
cp $WORKDIR/data/graph.json $WWWDIREXTERN/build/data/
cp $WORKDIR/data/nodelist.json $WWWDIREXTERN/build/data/
cp -r $WORKDIR/data/nodes $WWWDIREXTERN/build/data/
