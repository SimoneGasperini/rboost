from rboost.cli.rboost import RBoost
from rboost.utils.autocomplete import AutoComplete
from rboost.utils.exceptions import Exceptions


@RBoost.subcommand('show-labels')
class ShowLabels (RBoost):
    """
    Show a set of labels within RBoost network
    """

    def main(self):

        nodelist = self.get_nodelist()
        filepath = self.downloads_path + 'RBoost_labels.html'

        self.network.show(filepath=filepath, nodelist=nodelist)
        print('>>> Html file successfully downloaded to "RBoost_Data/My_Downloads"')

    def get_nodelist(self):

        number = int(input('>>> Number of labels : '))
        order = int(input('>>> Neighbors order : '))
        all_nodes = self.labnames
        nodelist = []

        for i in range(number):

            with AutoComplete(options=all_nodes):
                node = input(f'>>> Label_{i+1} name : ')

            if node not in all_nodes:
                e = Exceptions(state='failure',
                               message=f'The label "{node}" was not found in RBoost network')
                e.throw()

            nodelist += self.network.get_kth_neighbors(node=node, k=order)

        nodelist = list(set(nodelist))

        return nodelist
