from rboost.cli.rboost import RBoost
from rboost.utils.autocomplete import AutoComplete
from rboost.utils.exceptions import Exceptions


@RBoost.subcommand('loc-label')
class LocLabel (RBoost):
    """
    Localize a label within RBoost network
    """

    def main(self):

        node = self.get_node()
        distance = float(input('>>> Maximum distance : '))

        nodelist = self.network.get_nearest_nodes(node=node, distance=distance)
        filepath = self.downloads_path + 'RBoost_labels.html'

        self.network.show(filepath=filepath, nodelist=nodelist)
        print('>>> Html file successfully downloaded to "RBoost_Data/My_Downloads"')

    def get_node(self):

        all_nodes = self.labnames
        with AutoComplete(options=all_nodes):
            node = input('>>> Label name : ')

        if node not in all_nodes:
            e = Exceptions(state='failure',
                           message=f'The label "{node}" was not found in RBoost network')
            e.throw()

        return node
