from plumbum import cli

from rboost.cli.rboost import RBoost


@RBoost.subcommand('show-network')
class ShowNetwork (RBoost):
    """
    Show the RBoost network
    """

    _labtype = None
    _number = None

    @cli.switch('--labtype', str)
    def labtype(self, labtype):
        """
        Selects labels with the specified type
        """

        self._labtype = labtype

    @cli.switch('--number', int)
    def number(self, number):
        """
        Selects a fixed number of labels
        """

        self._number = number

    def main(self):

        nodelist = self.get_nodelist()
        filepath = self.downloads_path + 'RBoost_network.html'

        self.network.show(filepath=filepath, nodelist=nodelist)
        print('>>> Html file successfully downloaded to "RBoost_Data/My_Downloads"')

    def get_nodelist(self):

        nodelist = self.labnames

        if self._labtype is not None:
            nodelist = self.filter_by_type(nodelist)

        if self._number is not None:
            nodelist = self.select_number(nodelist)

        return nodelist

    def filter_by_type(self, nodelist):

        nodelist = [self.network.graph.nodes[n]['label'].name for n in nodelist
                    if self._labtype in self.network.graph.nodes[n]['label'].types]

        return nodelist

    def select_number(self, nodelist):

        if len(nodelist) > self._number:

            labels = sorted([self.network.graph.nodes[n]['label']
                            for n in nodelist], reverse=True)
            nodelist = [lab.name for lab in labels[:self._number]]

        return nodelist
