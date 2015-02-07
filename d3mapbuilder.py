import json
import datetime

class D3MapBuilder:
  def __init__(self, db, firmware):
    self._db = db
    self.firmware = firmware

  def build(self):
    output = dict()

    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    nodes = self._db.get_nodes()

    output['nodes'] = [{'name': x.name, 'id': x.id,
                        'geo': [float(x) for x in x.gps.split(" ")] if x.gps else None,
                        'hardware': x.hardware,
                        'firmware': x.firmware,
                        'gluon_base': x.gluon_base,
                        'autoupdater_state': x.autoupdater_state,
                        'autoupdater_branch': x.autoupdater_branch,
                        'batman_version': x.batman,
                        'batman_gwmode': x.batman_gwmode,
                        'uptime': x.uptime,
                        'gateway': x.gateway,
                        'addresses': x.addresses,
                        'lastseen': x.lastseen,
                        'flags': x.flags,
                        'clientcount': x.clientcount,
                        'role': x.role
                       } for x in nodes]

    links = self._db.get_links()

    output['links'] = [{'source': x.source.id, 'target': x.target.id,
                        'quality': x.quality,
                        'type': x.type,
                        'id': x.id
                       } for x in links]

    output['meta'] = {
                      'timestamp': now,
                      'gluon_release': str(self.firmware)
                     }

    return json.dumps(output)

