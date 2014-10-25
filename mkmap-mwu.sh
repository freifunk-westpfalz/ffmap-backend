#!/bin/bash

set -e

export PATH=/home/admin/bin:$PATH

cd "$(dirname "$0")"/

/usr/bin/python3 mergenodesjson.py /var/www/mapmz/build/nodes.json /var/www/mapwi/build/nodes.json /var/www/mapmwu/build/nodes.json
cp /var/www/mapmz/build/nodes/*.png /var/www/mapmwu/build/nodes/
cp /var/www/mapwi/build/nodes/*.png /var/www/mapmwu/build/nodes/
