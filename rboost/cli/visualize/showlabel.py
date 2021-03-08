import sys

import colorama

from rboost.cli.rboost import RBoost
from rboost.source.network import Network


@RBoost.subcommand ('show-label')
class ShowLabel (RBoost):
  '''
  Show a label within the RBoost network
  '''


  def main (self):

    label = input('>>> Label name : ')
    order = int(input('>>> Neighbors order : '))

    self.show_label(name=label, order=order)


  @staticmethod
  def show_label (name, order):

    with Network() as net:

      if name in net.graph.nodes:
        nodelist = net.get_kth_neighbors(node=name, k=order)
        net.show(nodelist=nodelist)

      else:
        colorama.init()
        message = f'FAIL: Label "{name}" not found in RBoost network'
        print('>>> \033[91m' + message + '\033[0m')
        sys.exit()
