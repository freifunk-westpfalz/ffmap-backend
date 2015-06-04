import os
import subprocess
import datetime

from lib.RRD import DS, RRA, RRD

now = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
prettynow = now.replace(":", "\:")

class NodeRRD(RRD):
    ds_list = [
        DS('upstate', 'GAUGE', 120, 0, 1),
        DS('clients', 'GAUGE', 120, 0, float('NaN')),
    ]
    rra_list = [
        # 2 hours of  1 minute samples
        RRA('AVERAGE', 0.5, 1, 120),
        #  5 days  of  5 minute samples
        RRA('AVERAGE', 0.5, 5, 1440),
        # 30 days  of  1 hour   samples
        RRA('AVERAGE', 0.5, 60, 720),
        #  1 year  of 12 hour   samples
        RRA('AVERAGE', 0.5, 720, 730),
        # 2 hours of  1 minute samples
        RRA('MAX', 0.5, 1, 120),
        #  5 days  of  5 minute samples
        RRA('MAX', 0.5, 5, 1440),
        # 30 days  of  1 hour   samples
        RRA('MAX', 0.5, 60, 720),
        #  1 year  of 12 hour   samples
        RRA('MAX', 0.5, 720, 730),
    ]

    def __init__(self, filename, node=None):
        """
        Create a new RRD for a given node.

        If the RRD isn't supposed to be updated, the node can be omitted.
        """
        self.node = node
        super().__init__(filename)
        self.ensure_sanity(self.ds_list, self.rra_list, step=60)

    @property
    def imagename(self):
        return "{basename}.png".format(
            basename=os.path.basename(self.filename).rsplit('.', 2)[0])

    # TODO: fix this, python does not support function overloading
    def update(self):
        super().update({'upstate': int(self.node['flags']['online']),
                        'clients': self.node['statistics']['clients']})

    def graph(self, directory, timeframe):
        """
        Create a graph in the given directory. The file will be named
        basename.png if the RRD file is named basename.rrd
        """
        args = ['rrdtool', 'graph', os.path.join(directory, self.imagename),
                '-s', '-' + timeframe,
                '-w', '800',
                '-h', '400',
                '-l', '0',
                '-y', '1:1',
                '--slope-mode',
                '--font', 'DEFAULT:7:',
                '--lower-limit', '0',
                '--right-axis', '1:0',
                '--x-grid', 'MINUTE:10:HOUR:1:MINUTE:120:0:%R',
                '--vertical-label', 'Anzahl Clients',
                '--watermark=' 'Freifunk MWU',
                'DEF:clients=' + self.filename + ':clients:AVERAGE',
                'AREA:clients#558020B0:Online Clients  ',
                'LINE1:clients#558020',
                'GPRINT:clients:LAST:now\: %4.0lf',
                'GPRINT:clients:MIN:min\: %4.0lf',
                'GPRINT:clients:AVERAGE:avg\: %4.0lf',
                'GPRINT:clients:MAX:max\: %4.0lf\\l',
                'COMMENT:Last Update\: ' + prettynow + '\\r',
        ]
        subprocess.check_output(args)
