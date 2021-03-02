import sys

import colorama
from plumbum import cli

from rboost.cli.rboost import RBoost
from rboost.source.network import Network


@RBoost.subcommand ('show-label')
class ShowLabel (RBoost):
  '''
  Show label whitin the RBoost network
  '''

  _neighbors_order = 1


  @cli.switch ('--neighbors_order', int)
  def neighbors_order (self, order):
    '''
    Specify the maximum neighbors order of the label
    '''

    self._neighbors_order = order


  def main (self, label):

    order = self._neighbors_order
    self.show_label(name=label, order=order)


  @staticmethod
  def show_label (name, order):

    with Network() as net:

      try:
        nodelist = net.get_kth_neighbors(node=name, k=order)

      except:
        colorama.init()
        message = f'FAIL: Label "{name}" not found in RBoost network'
        print('>>> \033[91m' + message + '\033[0m' )
        sys.exit()

      net.show(nodelist=nodelist)
