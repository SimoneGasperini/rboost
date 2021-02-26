import pandas as pd


class Label ():


  def __init__ (self,
                name,
                types         = [],
                queries_count = 0,
                uploads_count = 0,
                mentions      = pd.DataFrame(columns=['FILENAME','TYPE','SCORE'])):

    self.name = name
    self.types = types
    self.queries_count = queries_count
    self.uploads_count = uploads_count
    self.mentions = mentions


  def update (self, labinfo):

    self.queries_count += labinfo['queries_count']
    self.uploads_count += labinfo['uploads_count']

    self.mentions = self.mentions.append(labinfo['mentions'], ignore_index=True)
    self.mentions.sort_values(by=['SCORE'], ascending=False, ignore_index=True, inplace=True)

    self.types = list(self.mentions['TYPE'].unique())


  def show (self):

    parameters = list(self.__init__.__code__.co_varnames)
    parameters.remove('self')

    print('\n\n'.join([key.upper() + ' =\n' + str(getattr(self, key)) for key in parameters]))



if __name__== '__main__':

  from rboost.source.network import Network

  with Network(path='./../database/pickles/', name='network.pkl') as net:
    label = net.graph.nodes['quantum']['label']
    label.show()
