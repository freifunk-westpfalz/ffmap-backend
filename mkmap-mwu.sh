#!/bin/bash

set -e

export PATH=/home/admin/bin:$PATH

cd "$(dirname "$0")"/

php nodes-merger.php
cp /var/www/mapmz/build/nodes/*.png /var/www/mapmwu/build/nodes/
cp /var/www/mapwi/build/nodes/*.png /var/www/mapmwu/build/nodes/
