from rboost.cli.rboost import RBoost
from rboost.utils.autocomplete import AutoComplete
from rboost.utils.exceptions import Exceptions


@RBoost.subcommand ('print-label')
class PrintLabel (RBoost):
  """
  Print all the info about a label in RBoost network
  """

  def main (self):

    label = self.get_label()
    label.show()

  def get_label (self):

    all_nodes = self.labnames
    with AutoComplete(options=all_nodes):
      node = input('>>> Label name : ')

    if node not in all_nodes:
      e = Exceptions(state='failure',
                     message=f'The label "{node}" was not found in RBoost network')
      e.throw()

    label = self.network.graph.nodes[node]['label']

    return label
