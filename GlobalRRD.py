import os
import subprocess
from RRD import RRD, DS, RRA
import datetime

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
        RRA('AVERAGE', 0.5, 1, 120),    #  2 hours of 1 minute samples
        RRA('AVERAGE', 0.5, 60, 168),   #  7 days  of 1 hour   samples
        RRA('AVERAGE', 0.5, 60, 744),   # 31 days  of 1 hour   samples
        RRA('AVERAGE', 0.5, 1440, 1780),# ~5 years of 1 day    samples
        RRA('MAX', 0.5, 1, 120),    #  2 hours of 1 minute samples
        RRA('MAX', 0.5, 60, 168),   #  7 days  of 1 hour   samples
        RRA('MAX', 0.5, 60, 744),   # 31 days  of 1 hour   samples
        RRA('MAX', 0.5, 1440, 1780),# ~5 years of 1 day    samples
    ]

    def __init__(self, directory):
        super().__init__(os.path.join(directory, "nodes.rrd"))
        self.ensureSanity(self.ds_list, self.rra_list, step=60)

    def update(self, nodeCount, clientCount):
        super().update({'nodes': nodeCount, 'clients': clientCount})

    def graph(self, filename, timeframe):
        args = ["rrdtool", 'graph', filename,
                '-s', '-' + timeframe,
                '-w', '800',
                '-h' '400',
                '--watermark=' 'Freifunk MWU',
                'DEF:nodes=' + self.filename + ':nodes:AVERAGE',
                'LINE2:nodes#0066FF:nodes    ',
                'GPRINT:nodes:AVERAGE:avg\: %2.0lf',
                'GPRINT:nodes:MAX:max\: %2.0lf\\l',
                'DEF:clients=' + self.filename + ':clients:AVERAGE',
                'AREA:clients#33CC33:clients  ',
                'GPRINT:clients:AVERAGE:avg\: %2.0lf',
                'GPRINT:clients:MAX:max\: %2.0lf\\l',
                'COMMENT:Last Update\: ' + prettynow + '\\r',
        ]
        subprocess.check_output(args)
