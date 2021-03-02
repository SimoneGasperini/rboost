import pandas as pd


class Label ():
  '''
  Class for the label object


  Parameters
  ----------
    name : str
      Label name

    types : list, default=[]
      All the label types

    queries_count : int, default=0
      Number of times the label occurred in a query

    uploads_count : int, default=0
      Number of times the label occurred in a uploaded document

    mentions : pandas.DataFrame, default=pandas.DataFrame(columns=['DOCNAME','TYPE','SCORE']))
      Table to store the important mentions of the label in the uploaded
      documents, together with their type and their score
  '''

  def __init__ (self,
                name,
                types         = [],
                queries_count = 0,
                uploads_count = 0,
                mentions      = pd.DataFrame(columns=['DOCNAME','TYPE','SCORE'])):

    self.name = name
    self.types = types
    self.queries_count = queries_count
    self.uploads_count = uploads_count
    self.mentions = mentions


  def __lt__ (self, other):
    '''
    Compare the importance of two labels


    Parameters
    ----------
    other : Label
      The second label

    Returns
    -------
    less_than : bool
      Result
    '''

    count1 = self.queries_count + self.uploads_count
    count2 = other.queries_count + other.uploads_count
    less_than = count1 < count2

    return less_than


  def update (self, labinfo):
    '''
    Update the label using the new information contained in labsinfo


    Parameters
    ----------
    labinfo : dict
      New label information
    '''

    self.queries_count += labinfo['queries_count']
    self.uploads_count += labinfo['uploads_count']

    self.mentions = self.mentions.append(labinfo['mentions'], ignore_index=True)
    self.mentions.sort_values(by=['SCORE'], ascending=False, ignore_index=True, inplace=True)

    self.types = list(self.mentions['TYPE'].unique())


  def show (self):
    '''
    Print the label to terminal
    '''

    parameters = list(self.__init__.__code__.co_varnames)
    parameters.remove('self')

    print('\n\n'.join([key.upper() + ' =\n' + str(getattr(self, key)) for key in parameters]))



if __name__== '__main__':

  from rboost.source.network import Network

  with Network() as net:
    label = net.graph.nodes['quantum']['label']
    label.show()
