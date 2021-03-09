import sys
import colorama


class RBException ():

  color = {'failure' : lambda msg: '\033[91mFAILURE: ' + msg + '\033[0m',
           'warning' : lambda msg: '\033[93mWARNING: ' + msg + '\033[0m'}


  def __init__ (self, state, message, args=None):

    self.state = state
    self.message = message

    if args is not None:
      self.message += '/n/t'.join(args)

    self.throw()


  def throw (self):

    colorama.init()
    colored_message = self.color[self.state](self.message)
    print('>>> ' + colored_message)

    if self.state == 'failure':
      sys.exit()
