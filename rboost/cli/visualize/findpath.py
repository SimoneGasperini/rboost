from rboost.cli.rboost import RBoost
from rboost.utils.autocomplete import AutoComplete
from rboost.utils.exceptions import Exceptions


@RBoost.subcommand ('find-path')
class FindPath (RBoost):
  """
  Find a path between two labels in RBoost network
  """

  def main (self):

    source = self.get_node(msg='>>> Source label name : ')
    target = self.get_node(msg='>>> Target label name : ')

    path = self.network.get_path(source=source, target=target)
    self.print_path(path)

  def get_node (self, msg):

    all_nodes = self.labnames_list
    with AutoComplete(options=all_nodes):
      node = input(msg)

    if node not in all_nodes:
      e = Exceptions(state='failure',
                     message=f'The label "{node}" was not found in RBoost network')
      e.throw()

    return node

  def get_middle_node (self):

    print(f'>>> Do you want a specific label to be included in the path?')
    answer = input('>>> (y/n) ')

    if answer == 'y':
      middle = self.get_node(msg='>>> Label name : ')
      return middle

    if answer == 'n':
      middle = None
      return middle

    e = Exceptions(state='failure', message=f'Invalid answer')
    e.throw()

  @staticmethod
  def print_path (path):

    path[0] = path[0].upper()
    path[-1] = path[-1].upper()

    path_string = ' --> '.join(path)
    print(path_string)
