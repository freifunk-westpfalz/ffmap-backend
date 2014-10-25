
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
    p.add_argument('left', action='store', help='left nodes.json')
    p.add_argument('right', action='store', help='right nodes.json')
    p.add_argument('out', action='store', help='write merged result into file')
    p = p.parse_args()

    res = {'meta': dict(), 'nodes': list(), 'links': list()}

    for c in [p.left, p.right]:

        j = readin(c)
        res['meta'].update(j['meta'])
        res['nodes'] += j['nodes']
        res['links'] += j['links']

    writeout(p.out, res)
