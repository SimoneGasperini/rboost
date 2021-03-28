class Link:
  """
  Class for the link object


  Parameters
  ----------
  node1 : str
    First node name

  node2 : str
    Second node name

  labels : dict
    Labels objects by node name
  """

  def __init__ (self, node1, node2, labels):

    self.node1 = node1
    self.node2 = node2
    self.labels = labels

    self.mentions = self.get_mentions()

  def __repr__ (self):
    """
    Link object representation


    Returns
    -------
    string : str
      Representation
    """

    string = f'{self.node1.upper()}<-->{self.node2.upper()}\n\n'
    for mention in self.mentions:
      string += f'- {mention}\n'

    return string

  def to_html (self):
    """
    Get the link string representation in html format


    Returns
    -------
    html : str
      Html representation
    """

    string = self.__repr__()
    html = '<p>' + string.replace('\n', '<br>') + '</p>'

    return html

  def get_mentions (self):
    """
    Get all the common mentions of the two nodes connected by the link


    Returns
    -------
    mentions : set of str
      Common mentions
    """

    mentions1 = set(self.labels[self.node1].mentions['DOCNAME'])
    mentions2 = set(self.labels[self.node2].mentions['DOCNAME'])

    mentions = mentions1 & mentions2

    return mentions
