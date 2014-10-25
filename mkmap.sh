#!/bin/bash

set -e

DEST=$1

export PATH=/home/admin/bin:$PATH

[ "$DEST" ] || exit 1

cd "$(dirname "$0")"/

./bat2nodes.py -a aliases-mz.json -m mzBAT -s /var/run/alfred-mz.sock -f 0.1 -d $DEST
