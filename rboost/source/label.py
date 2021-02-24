import pandas as pd


class Label ():


  def __init__ (self,
                name,
                types         = [],
                query_count   = 0,
                reading_count = 0,
                writing_count = 0,
                mentions      = pd.DataFrame(columns=['FILENAME','FILETYPE','SCORE'])):

    self.name = name
    self.types = types
    self.query_count = query_count
    self.reading_count = reading_count
    self.writing_count = writing_count
    self.mentions = mentions


  def update (self, labinfo):

    self.query_count += labinfo['query_count']
    self.reading_count += labinfo['reading_count']
    self.writing_count += labinfo['writing_count']

    self.mentions = self.mentions.append(labinfo['mentions'], ignore_index=True)
    self.mentions.sort_values(by=['SCORE'], ascending=False, ignore_index=True, inplace=True)

    self.types = list(self.mentions['FILETYPE'].unique())


  def show (self):

    parameters = list(self.__init__.__code__.co_varnames)
    parameters.remove('self')

    print('\n\n'.join([key.upper() + ' =\n' + str(getattr(self, key)) for key in parameters]))



if __name__== '__main__':

  from rboost.source.network import Network

  with Network(path='./../database/pickles/', name='network.pkl') as net:
    label = net.graph.nodes['quantum']['label']
    label.show()
