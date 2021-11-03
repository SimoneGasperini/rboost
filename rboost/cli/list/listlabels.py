import pandas as pd
from plumbum import cli

from rboost.cli.rboost import RBoost


@RBoost.subcommand('list-labels')
class ListLabels (RBoost):
    """
    List the labels in RBoost network
    """

    _labtype = None

    @cli.switch('--labtype', str)
    def labtype(self, labtype):
        """
        Selects labels with the specified type
        """

        self._labtype = labtype

    def main(self):

        labels = self.get_labels()

        df = self.create_dataframe(labels)
        self.show_dataframe(df, full=True)

    def get_labels(self):

        labels = [self.network.graph.nodes[n]['label']
                  for n in self.network.graph.nodes]
        if self._labtype is not None:
            labels = [label for label in labels if self._labtype in label.types]
        labels.sort()

        return labels

    @staticmethod
    def create_dataframe(labels):

        columns = ['LABEL', 'TYPES', 'QUERIES', 'UPLOADS']
        data = [[lab.name, lab.types, lab.queries_count, lab.uploads_count]
                for lab in labels]
        df = pd.DataFrame(data=data, columns=columns)

        return df
