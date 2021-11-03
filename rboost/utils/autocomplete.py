import readline


class AutoComplete:

    def __init__(self, options):

        self.options = options

        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.complete)

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.options = []

    def complete(self, text, state):

        for name in self.options:

            if name.startswith(text):
                if state == 0:
                    return name
                else:
                    state -= 1
