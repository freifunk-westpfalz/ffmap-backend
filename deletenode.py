#!/usr/bin/env python3                                                               

import json
import argparse
import os
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-n', '--nodes', action='store',
                  help='nodes file you want to modify',required=True)

parser.add_argument('-id', '--nodeid', action='store',
                  help='node id you want to delete')

args = parser.parse_args()
options = vars(args)

nodes_fn = os.path.realpath(options['nodes'])
rem_node_id = options['nodeid']

# read nodedb state from node.json
try:
    with open(nodes_fn, 'r', encoding=('UTF-8')) as nodedb_handle:
        nodedb = json.load(nodedb_handle)
except IOError:
    nodedb = {'nodes': dict()}

prune = []
for node_id, node in nodedb['nodes'].items():
     if node_id == rem_node_id:
        prune.append(rem_node_id)
        print ("match")
if prune:
    for node_id in prune:
        del nodedb['nodes'][node_id]

    # write processed data to dest dir
    with open(nodes_fn, 'w') as f:
        json.dump(nodedb, f)
