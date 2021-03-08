from plumbum import cli

from rboost.cli.rboost import RBoost
from rboost.source.network import Network


@RBoost.subcommand ('show-network')
class ShowNetwork (RBoost):
  '''
  Show the RBoost network
  '''

  _num = None

  @cli.switch ('--num', int)
  def num (self, num):
    '''
    Selects a fixed number of the most important labels
    '''

    self._num = num


  def main (self):

    if self._num is None:
      self.show_full()

    else:
      self.show_sub(num=self._num)


  @staticmethod
  def show_full ():

    with Network() as net:

      net.show()


  @staticmethod
  def show_sub (num):

    with Network() as net:

      labels = net.get_labels(sort=True)
      nodelist = [lab.name for lab in labels[:num]]

    net.show(nodelist=nodelist)
