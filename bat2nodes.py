#!/usr/bin/env python3

import json
import fileinput
import argparse
import os
import time

from batman import batman
from alfred import alfred
from rrddb import rrd
from nodedb import NodeDB
from d3mapbuilder import D3MapBuilder

# Force encoding to UTF-8
import locale                                  # Ensures that subsequent open()s
locale.getpreferredencoding = lambda _=None: 'UTF-8'  # are UTF-8 encoded.

import sys
#sys.stdin = open('/dev/stdin', 'r')
#sys.stdout = open('/dev/stdout', 'w')
#sys.stderr = open('/dev/stderr', 'w')

parser = argparse.ArgumentParser()

parser.add_argument('-a', '--aliases',
                  help='read aliases from FILE',
                  action='append',
                  metavar='FILE')

parser.add_argument('-m', '--mesh', action='append',
                  help='batman mesh interface')

parser.add_argument('-s', '--socket', action='append',
                  help='alfred sockets')

parser.add_argument('-f', '--firmware', action='store',
                  help='current firmware')

parser.add_argument('-c', '--community', action='store',
                  help='unique name of community')

parser.add_argument('-d', '--destination-directory', action='store',
                  help='destination directory for generated files',required=True)

args = parser.parse_args()

options = vars(args)

if not options['mesh']:
  options['mesh'] = ['bat0']

if not options['socket']:
  options['socket'] = ['/var/run/alfred.sock']

if not options['firmware']:
  options['firmware'] = None

if not options['community']:
  options['community'] = None
  statefile = "state.json"
  nodesjson = "nodes.json"
  rrddir = "/nodedb/"
else:
  statefile = 'state_' + options['community'] + '.json'
  nodesjson = 'nodes_' + options['community'] + '.json'
  rrddir = '/nodedb_' + options['community'] + '/'

db = NodeDB(int(time.time()))

bm = batman(options['socket'],options['mesh'])
db.parse_vis_data(bm.vis_data())
for gw in bm.gateway_list():
  db.mark_gateway(gw)

if options['aliases']:
  for aliases in options['aliases']:
    db.import_aliases(json.load(open(aliases)))

af = alfred(options['socket'])
db.import_aliases(af.aliases())

db.load_state(statefile)

# remove nodes that have been offline for more than 30 days
db.prune_offline(time.time() - 90*86400)

db.dump_state(statefile)

scriptdir = os.path.dirname(os.path.realpath(__file__))

m = D3MapBuilder(db,options['firmware'])

#Write nodes json
nodes_json = open(options['destination_directory'] + '/' + nodesjson + '.new','w')
nodes_json.write(m.build())
nodes_json.close()

#Move to destination
os.rename(options['destination_directory'] + '/' + nodesjson + '.new',options['destination_directory'] + '/' + 'nodes.json')

try:
    os.stat(scriptdir + rrddir)
except:
    os.mkdir(scriptdir + rrddir)

rrd = rrd(scriptdir +  rrddir, options['destination_directory'] + "/nodes")
rrd.update_database(db)
rrd.update_images()
