import nltk
from gensim.summarization import keywords


class Document ():


  def __init__ (self, path, name, filetype):

    self.path = path
    self.name = name
    self.filetype = filetype

    self.state = True


  def __repr__ (self):

    class_name = self.__class__.__qualname__
    params = list(self.__init__.__code__.co_varnames)
    params.remove('self')
    args = ', '.join([f'{key}={getattr(self, key)}' for key in params])

    return f'{class_name}({args})'


  def get_text (self):

    raise NotImplementedError


  def get_keywords (self, text, ratio):

    if not self.state:
      return None

    raw_kws = keywords(text, ratio=ratio, scores=True, lemmatize=True, split=True)
    l = nltk.wordnet.WordNetLemmatizer()
    kws = {l.lemmatize(word) : round(score,3) for (word, score) in raw_kws}

    return kws


  def get_data (self):

    raise NotImplementedError
