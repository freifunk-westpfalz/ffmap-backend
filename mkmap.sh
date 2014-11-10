#!/bin/bash

set -e

DEST=$1
FIRMWARE=$2

export PATH=/home/admin/bin:$PATH

[ "$DEST" ] || exit 1

cd "$(dirname "$0")"/

./bat2nodes.py -c mainz -a aliases-mz.json -m mzBAT -s /var/run/alfred-mz.sock -f $FIRMWARE -d $DEST
#./bat2nodes.py -c wiesbaden -a aliases-wi.json -m wiBAT -s /var/run/alfred-wi.sock -f $FIRMWARE -d $DEST
#./bat2nodes.py -c mwu -a aliases-mz.json -a aliases-wi.json -m mzBAT -m wiBAT -s /var/run/alfred-mz.sock -s /var/run/alfred-wi.sock -f $FIRMWARE -d $DEST

