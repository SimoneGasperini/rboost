import pandas as pd
import Levenshtein as lev
from PySide2.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableView,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QTableView,
    QHeaderView
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QFont

from rboost.gui.utils.pandasmodel import PandasModel


class SearchWindow(QWidget):

    def __init__(self, rboost):
        super().__init__()
        self.rboost = rboost

        self.layout = QVBoxLayout()
        self._add_input_layout()
        self._add_output_layout()
        self.table_view = None
        self._add_table_view_layout()
        self.setLayout(self.layout)

    def _add_input_layout(self):
        self.input_layout = QHBoxLayout()
        self._add_label()
        self._add_input_line()
        search_button = QPushButton('Search')
        search_button.clicked.connect(self.show_results)
        clear_button = QPushButton('Clear')
        clear_button.clicked.connect(self.clear_results)
        self.input_layout.addWidget(search_button)
        self.input_layout.addWidget(clear_button)
        self.layout.addLayout(self.input_layout)

    def _add_label(self):
        label = QLabel('Label:')
        label.setFont(QFont('Arial', 16))
        label.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.input_layout.addWidget(label)

    def _add_input_line(self):
        self.layout = QVBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setFont(QFont('Arial', 20))
        self.input_line.setMaximumWidth(800)
        self.input_layout.addWidget(self.input_line)

    def _add_output_layout(self):
        self.output_layout = QVBoxLayout()
        self.label_not_found = QLabel()
        self.label_not_found.setFont(QFont('Times', 12))
        self.label_not_found.setStyleSheet('QLabel {color : red}')
        self.similar_labels = QLabel()
        self.similar_labels.setFont(QFont('Times', 12))
        self.output_layout.addWidget(self.label_not_found)
        self.output_layout.addWidget(self.similar_labels)
        self.layout.addLayout(self.output_layout)

    def _add_table_view_layout(self, df=None):
        self.table_view_layout = QHBoxLayout()
        if self.table_view is not None:
            self.table_view_layout.removeWidget(self.table_view)
            self.table_view.deleteLater()
        self.table_view = self._create_table_view(df=df)
        self.table_view_layout.addWidget(self.table_view)
        self.layout.addLayout(self.table_view_layout)

    def _create_table_view(self, df):
        if df is None:
            df = pd.DataFrame()
        model = PandasModel(df)
        table_view = QTableView()
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return table_view

    def _get_dataframe(self, label):
        dframe = self.rboost.database.dataframe
        colname = self.rboost.documents_df_cols['keywords']
        df = dframe[dframe[colname].apply(
            lambda keywords: label in keywords)]
        return df

    def _get_messages(self, label, df):
        msg1 = f'Label "{label}" not found in RBoost!' if df.empty else ''
        similar_labels = [lab for lab in self.rboost.labnames
                          if 0 < lev.distance(label, lab) < 3]
        msg2 = 'Similar labels found: "' + '", "'.join(similar_labels) + '"' \
            if similar_labels else 'Similar labels found: None'
        return msg1, msg2

    def show_results(self):
        label = self.input_line.text()
        df = self._get_dataframe(label=label)
        msg1, msg2 = self._get_messages(label=label, df=df)
        self.label_not_found.setText(msg1)
        self.similar_labels.setText(msg2)
        self._add_table_view_layout(df=df)
        self.setLayout(self.layout)

    def clear_results(self):
        self.input_line.clear()
        self.label_not_found.clear()
        self.similar_labels.clear()
        empty_df = pd.DataFrame()
        self._add_table_view_layout(df=empty_df)
        self.setLayout(self.layout)
