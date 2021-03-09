from rboost.cli.rboost import RBoost
from rboost.source.network import Network
from rboost.utils.exception import RBException


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
        RBException(state='failure', message=f'The label "{name}" was not found in RBoost network')
