#!/usr/bin/env python3

import json
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--statefile', nargs='+', help='state files you want to clean up')

args = parser.parse_args()
options = vars(args)

statefile = options['statefile']

for s in range(len(statefile)):
    obj  = json.load(open(statefile[s]))

    for i in range(len(obj)):
        if (obj[i]["name"] == "" and
            obj[i]["uptime"] == ""):
            obj.pop(i)
            break

    open(statefile[s], "w").write( json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')) )
