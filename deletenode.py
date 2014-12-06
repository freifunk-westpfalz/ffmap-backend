#!/usr/bin/env python3                                                               

import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--statefile', action='store',
                  help='state file you want to modify',required=True)

parser.add_argument('-id', '--identifier', action='store',
                  help='node id you want to delete',required=True)

args = parser.parse_args()
options = vars(args)

obj  = json.load(open(options['statefile']))

for i in range(len(obj)):
    if obj[i]["id"] == options['identifier']:
        obj.pop(i)
        break

# Output the updated file with pretty JSON                                      
open(options['statefile'], "w").write(
    json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': '))
)
