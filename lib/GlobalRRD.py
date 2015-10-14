import os
import subprocess
import datetime

from lib.RRD import DS, RRA, RRD

now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
prettynow = now.replace(":", "\:")

class GlobalRRD(RRD):
    ds_list = [
        # Number of nodes available
        DS('nodes', 'GAUGE', 120, 0, float('NaN')),
        # Number of client available
        DS('clients', 'GAUGE', 120, 0, float('NaN')),
    ]
    rra_list = [
        # 2 hours of 1 minute samples
        RRA('AVERAGE', 0.5, 1, 120),
        # 7 days og 1 hour samples
        RRA('AVERAGE', 0.5, 60, 168),
        # 31 days  of 1 hour samples
        RRA('AVERAGE', 0.5, 60, 744),
        # ~5 years of 1 day samples
        RRA('AVERAGE', 0.5, 1440, 1780),
        # 2 hours of 1 minute samples
        RRA('MAX', 0.5, 1, 120),
        # 7 days og 1 hour samples
        RRA('MAX', 0.5, 60, 168),
        # 31 days  of 1 hour samples
        RRA('MAX', 0.5, 60, 744),
        # ~5 years of 1 day samples
        RRA('MAX', 0.5, 1440, 1780),
    ]

    def __init__(self, directory):
        super().__init__(os.path.join(directory, "nodes.rrd"))
        self.ensure_sanity(self.ds_list, self.rra_list, step=60)

    # TODO: fix this, python does not support function overloading
    def update(self, node_count, client_count):
        super().update({'nodes': node_count, 'clients': client_count})

    def graph(self, filename, timeframe):
        args = ["rrdtool", 'graph', filename,
                '-s', '-' + timeframe,
                '-w', '800',
                '-h' '400',
                '--font', 'DEFAULT:7:',
                '--lower-limit', '0',
                '--right-axis', '1:0',
                '--vertical-label', 'Anzahl Clients/Nodes',
                '--watermark=' 'Freifunk MWU',
                'DEF:clients=' + self.filename + ':clients:AVERAGE',
                'AREA:clients#558020B0:Online Clients  ',
                'LINE1:clients#558020',
                'GPRINT:clients:AVERAGE:avg\: %4.0lf',
                'GPRINT:clients:MAX:max\: %4.0lf\\l',
                'DEF:nodes=' + self.filename + ':nodes:AVERAGE',
                'LINE2:nodes#1566A9:Online Nodes    ',
                'GPRINT:nodes:AVERAGE:avg\: %4.0lf',
                'GPRINT:nodes:MAX:max\: %4.0lf\\l',
                'COMMENT:Last Update\: ' + prettynow + '\\r',
        ]
        subprocess.check_output(args)
