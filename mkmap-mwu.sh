#!/bin/bash

set -e

export PATH=/home/admin/bin:$PATH

WORKDIR="/home/admin/clones/ffmap-backend-intern-mwu"
WWWDIRINTERN="/var/www/meshviewer-intern-mwu"
WWWDIREXTERN="/var/www/meshviewer-extern-mwu"

cd "$(dirname "$0")"/

/usr/bin/python3 $WORKDIR/backend.py --prune 45 -m wiBAT:/var/run/alfred-wi.sock mzBAT:/var/run/alfred-mz.sock --vpn 02:00:0a:38:00:17 02:00:0a:38:00:05 02:00:0a:38:00:07 02:00:0a:38:00:d0 02:00:0a:38:00:e7 02:00:0a:25:00:17 02:00:0a:25:00:05 02:00:0a:25:00:07 02:00:0a:25:00:d0 02:00:0a:25:00:e7 -d $WORKDIR/data/

/usr/bin/jq '.nodes = (.nodes | with_entries(del(.value.nodeinfo.owner)))' < $WORKDIR/data/nodes.json > $WORKDIR/data/nodes-internet.json
cp $WORKDIR/data/* $WWWDIRINTERN/build/data/

cp $WORKDIR/data/nodes-internet.json $WWWDIREXTERN/build/data/nodes.json
cp $WORKDIR/data/graph.json $WWWDIREXTERN/build/data/
cp $WORKDIR/data/nodelist.json $WWWDIREXTERN/build/data/

