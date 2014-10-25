
from json import loads, dumps
from argparse import ArgumentParser

def readin(filename):
    with open(filename, 'r') as f:
        return loads(f.read())

def writeout(filename, content):
    if content:
        with open(filename, 'w') as f:
            return f.write(dumps(content))

if __name__ == '__main__':
    p = ArgumentParser(prog='mergenodesjson', description='merge two ffmap nodes.jsons together', epilog='-.-')
    p.add_argument('input', action='store', nargs='*', help='input jsons (use many!)')
    p.add_argument('output', action='store', help='output json')
    p = p.parse_args()

    res = {'meta': dict(), 'nodes': list(), 'links': list()}
    o = 0

    for c in p.input:

        j = readin(c)
        res['meta'].update(j['meta'])
        res['nodes'] += j['nodes']

        [x.update({
            'source': x['source'] + o,
            'target': x['target'] + o
        }) for x in j['links']]
        # pointer fun with blinky!
        res['links'] += j['links']
        o += len(res['nodes'])

    writeout(p.output, res)
