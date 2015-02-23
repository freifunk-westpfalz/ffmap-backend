#!/usr/bin/env python3

import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--statefile', nargs='+', help='state files you want to clean up')

args = parser.parse_args()
options = vars(args)

statefile = options['statefile']

for s in range(len(statefile)):
    object  = json.load(open(statefile[s]))
    newobject = [ node for node in object if node["name"] != "" and node["hardware"] != "" ]
    open(statefile[s], "w").write( json.dumps(newobject, sort_keys=True, indent=4, separators=(',', ': ')) )
