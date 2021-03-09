import readline


class RBAutoComplete ():


  def __init__ (self, options):

    self.options = options

    readline.parse_and_bind('tab: complete')
    readline.set_completer(self.complete)


  def complete (self, text, state):

    for name in self.options:

      if name.startswith(text):
        if state == 0: return name
        else: state -= 1
