#!/bin/bash

set -e

export PATH=/home/admin/bin:$PATH

WORKDIR="/home/admin/clones/ffmap-backend-intern-mz"
WWWDIRINTERN="/var/www/meshviewer-intern-mz"
WWWDIREXTERN="/var/www/meshviewer-extern-mz"

cd "$(dirname "$0")"/

/usr/bin/python3 $WORKDIR/backend.py --with-rrd --prune 45 -m mzBAT:/var/run/alfred-mz.sock --vpn 02:00:0a:25:00:17 02:00:0a:25:00:07 02:00:0a:25:00:d0 02:00:0a:25:00:e7 02:00:0a:25:00:2a -d $WORKDIR/data/

/usr/bin/jq '.nodes = (.nodes | with_entries(del(.value.nodeinfo.owner)))' < $WORKDIR/data/nodes.json > $WORKDIR/data/nodes-internet.json
cp -r $WORKDIR/data/* $WWWDIRINTERN/build/data/

cp $WORKDIR/data/nodes-internet.json $WWWDIREXTERN/build/data/nodes.json
cp $WORKDIR/data/graph.json $WWWDIREXTERN/build/data/
cp $WORKDIR/data/nodelist.json $WWWDIREXTERN/build/data/
cp -r $WORKDIR/data/nodes $WWWDIREXTERN/build/data/

# Provide nodes.json in old ffmap-d3 format just for freifunk-karte.de
/usr/bin/jq -n -f ffmap-d3.jq --argfile nodes data/nodes-internet.json --argfile graph data/graph.json > $WWWDIREXTERN/build/nodes.json
