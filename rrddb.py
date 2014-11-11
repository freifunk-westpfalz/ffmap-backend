#!/usr/bin/env python3
import subprocess
import time
import os
from GlobalRRD import GlobalRRD
from NodeRRD import NodeRRD

class rrd:
  def __init__( self
              , databaseDirectory
              , imagePath
              , displayTimeGlobal = "7d"
              , displayTimeGlobal30d = "30d"
              , displayTimeGlobal365d = "365d"
              , displayTimeNode = "1d"
              , displayTimeNode7d = "7d"
              , displayTimeNode30d = "30d"
              ):
    self.dbPath = databaseDirectory
    self.globalDb = GlobalRRD(self.dbPath)
    self.imagePath = imagePath
    self.displayTimeGlobal = displayTimeGlobal
    self.displayTimeGlobal30d = displayTimeGlobal30d
    self.displayTimeGlobal365d = displayTimeGlobal365d
    self.displayTimeNode = displayTimeNode
    self.displayTimeNode7d = displayTimeNode7d
    self.displayTimeNode30d = displayTimeNode30d

    self.currentTimeInt = (int(time.time())/60)*60
    self.currentTime    = str(self.currentTimeInt)

    try:
      os.stat(self.imagePath)
    except:
      os.mkdir(self.imagePath)

  def update_database(self,db):
    nodes = db.get_nodes()
    clientCount = sum(map(lambda d: d.clientcount, nodes))

    curtime = time.time() - 60
    self.globalDb.update(len(list(filter(lambda x: x.lastseen >= curtime, nodes))), clientCount)
    for node in nodes:
      rrd = NodeRRD(
        os.path.join(self.dbPath, str(node.id).replace(':', '') + '.rrd'),
        node
      )
      rrd.update()

  def update_images(self):
    """ Creates an image for every rrd file in the database directory.
    """

    self.globalDb.graph(os.path.join(self.imagePath, "globalGraph.png"), self.displayTimeGlobal)
    self.globalDb.graph(os.path.join(self.imagePath, "globalGraph_30d.png"), self.displayTimeGlobal30d)
    self.globalDb.graph(os.path.join(self.imagePath, "globalGraph_365d.png"), self.displayTimeGlobal365d)

    nodeDbFiles = os.listdir(self.dbPath)

    for fileName in nodeDbFiles:
      if not os.path.isfile(os.path.join(self.dbPath, fileName)):
        continue

      nodeName = os.path.basename(fileName).split('.')
      if nodeName[1] == 'rrd' and not nodeName[0] == "nodes":
        rrd1d = NodeRRD(os.path.join(self.dbPath, fileName))
        rrd1d.graph(self.imagePath, self.displayTimeNode)
        rrd7d = NodeRRD(os.path.join(self.dbPath, fileName))
        rrd7d.graph(self.imagePath, self.displayTimeNode7d)
        rrd30d = NodeRRD(os.path.join(self.dbPath, fileName))
        rrd30d.graph(self.imagePath, self.displayTimeNode30d)
