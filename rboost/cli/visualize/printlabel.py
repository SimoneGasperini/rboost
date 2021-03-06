import sys

import colorama

from rboost.cli.rboost import RBoost
from rboost.source.network import Network


@RBoost.subcommand ('print-label')
class PrintLabel (RBoost):
  '''
  Print the infos about a label in RBoost database
  '''


  def main (self):

    label = input('>>> Label name : ')
    self.print_label(name=label)


  @staticmethod
  def print_label (name):

    with Network() as net:

      if name in net.graph.nodes:
        label = net.graph.nodes[name]['label']
        label.show()

      else:
        colorama.init()
        message = f'FAIL: Label "{name}" not found in RBoost database'
        print('>>> \033[91m' + message + '\033[0m')
        sys.exit()
