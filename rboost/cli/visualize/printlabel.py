from rboost.cli.rboost import RBoost
from rboost.source.network import Network
from rboost.utils.exception import RBException


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
        RBException(state='failure', message=f'The label "{name}" was not found in RBoost network')
