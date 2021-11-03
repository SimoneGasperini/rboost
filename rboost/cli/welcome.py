from rboost.cli.rboost import RBoost


@RBoost.subcommand('welcome')
class Welcome (RBoost):
    """
    Welcome to RBoost software
    """

    def main(self):

        print('Welcome to RBoost!')
