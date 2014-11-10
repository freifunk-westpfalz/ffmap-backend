#!/usr/bin/env python3
import subprocess
import json
import re

class batman:
  """ Bindings for B.A.T.M.A.N. advanced batctl tool
  """
  def __init__(self,socket,mesh_interface):
    self.socket = socket
    self.mesh_interface = mesh_interface

  def vis_data(self):
    vds = self.vis_data_batadv_vis()
    return vds

  def vis_data_helper(self,lines):
    vd = []
    for line in lines:
      try:
        utf8_line = line.decode("utf-8")
        vd.append(json.loads(utf8_line))
      except e:
        pass
    return vd

  def vis_data_batadv_vis(self):
    """ Parse "batadv-vis -u <alfred-socket> -i <mesh_interface> -f json" into an array of dictionaries.
    """
    for i,(a,m) in enumerate(zip(self.socket,self.mesh_interface)):
      visbucket = subprocess.check_output(["batadv-vis","-u",a,"-i",m,"-f","json"])
      if i == 0:
        output = visbucket
      else:
        output = output + visbucket

    lines = output.splitlines()
    return self.vis_data_helper(lines)

  def gateway_list(self):
    """ Parse "batctl -m <mesh_interface> gwl -n" into an array of dictionaries.
    """
    gw = []

    for m in self.mesh_interface:
      output = subprocess.check_output(["batctl","-m",m,"gwl","-n"])
      output_utf8 = output.decode("utf-8")
      lines = output_utf8.splitlines()
      own_mac = re.match(r"^.*MainIF/MAC: [^/]+/([0-9a-f:]+).*$", lines[0]).group(1)
      gw_mode = self.gateway_mode(m)
      if gw_mode['mode'] == 'server':
        gw.append(own_mac)

      for line in lines:
        gw_line = re.match(r"^(?:=>)? +([0-9a-f:]+) ", line)
        if gw_line:
          gw.append(gw_line.group(1))

    return gw

  def gateway_mode(self,mesh):
    """ Parse "batctl -m <mesh_interface> gw"
    """
    output = subprocess.check_output(["batctl","-m",mesh,"gw"])
    elements = output.decode("utf-8").split()
    mode = elements[0]
    if mode == "server":
        return {'mode': 'server', 'bandwidth': elements[3]}
    else:
        return {'mode': mode}

if __name__ == "__main__":
  bc = batman()
  vd = bc.vis_data()
  gw = bc.gateway_list()
  for x in vd:
    print(x)
  print(gw)
  print(bc.gateway_mode())
