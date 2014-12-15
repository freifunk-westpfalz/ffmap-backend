#!/usr/bin/env python3                                                               

import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--statefile', nargs='+',
                  help='state file you want to modify',required=True)

parser.add_argument('-id', '--identifier', action='store',
                  help='node id you want to delete')

parser.add_argument('-n', '--name', action='store',
                  help='node name you want to delete')

args = parser.parse_args()
options = vars(args)

statefile = options['statefile']

for s in range(len(statefile)):
    obj  = json.load(open(statefile[s]))

    if options['identifier']:
        for i in range(len(obj)):
            if obj[i]["id"] == options['identifier']:
                obj.pop(i)
                break

    if options['name']:
        for i in range(len(obj)):
            if obj[i]["name"] == options['name']:
                obj.pop(i)
                break

    open(statefile[s], "w").write(
        json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
    )
