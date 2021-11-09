import pandas as pd
from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFormLayout,
    QTableView,
    QPushButton,
    QComboBox,
    QHeaderView
)

from rboost.gui.utils.pandasmodel import PandasModel


class ListDocumentsWindow(QWidget):

    def __init__(self, rboost):
        super().__init__()
        self.rboost = rboost

        self.layout = QVBoxLayout()
        self._add_forms_layout()
        self._add_buttons_layout()
        self.table_view = None
        self._add_table_view_layout()
        self.setLayout(self.layout)

    def _add_forms_layout(self):
        self.forms_layout = QHBoxLayout()
        user_form = self._create_user_form()
        doctype_form = self._create_doctype_form()
        self.forms_layout.addLayout(user_form)
        self.forms_layout.addLayout(doctype_form)
        self.layout.addLayout(self.forms_layout)

    def _add_buttons_layout(self):
        self.buttons_layout = QHBoxLayout()
        show_button = QPushButton('Show list')
        show_button.clicked.connect(self.show_table)
        clear_button = QPushButton('Clear list')
        clear_button.clicked.connect(self.clear_table)
        self.buttons_layout.addWidget(show_button)
        self.buttons_layout.addWidget(clear_button)
        self.layout.addLayout(self.buttons_layout)

    def _add_table_view_layout(self, df=None):
        self.table_view_layout = QHBoxLayout()
        if self.table_view is not None:
            self.table_view_layout.removeWidget(self.table_view)
            self.table_view.deleteLater()
        self.table_view = self._create_table_view(df=df)
        self.table_view_layout.addWidget(self.table_view)
        self.layout.addLayout(self.table_view_layout)

    def _create_user_form(self):
        user_form = QFormLayout()
        items = [None] + sorted(list(self.rboost.users))
        self.user_combobox = QComboBox()
        self.user_combobox.addItems(items)
        user_form.addRow('User/author', self.user_combobox)
        return user_form

    def _create_doctype_form(self):
        doctype_form = QFormLayout()
        items = [None] + sorted(list(self.rboost.doctypes))
        self.doctype_combobox = QComboBox()
        self.doctype_combobox.addItems(items)
        doctype_form.addRow('Document type', self.doctype_combobox)
        return doctype_form

    def _create_table_view(self, df):
        if df is None:
            df = pd.DataFrame()
        model = PandasModel(df)
        table_view = QTableView()
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return table_view

    def _filter_data(self, df):
        user = str(self.user_combobox.currentText())
        if user:
            colname = self.rboost.dataframe_columns['user']
            df = df.loc[df[colname] == user]
        doctype = str(self.doctype_combobox.currentText())
        if doctype:
            colname = self.rboost.dataframe_columns['doctype']
            df = df.loc[df[colname] == doctype]
        return df

    def show_table(self):
        df = self.rboost.database.dataframe
        filtered_df = self._filter_data(df)
        self._add_table_view_layout(df=filtered_df)
        self.setLayout(self.layout)

    def clear_table(self):
        empty_df = pd.DataFrame()
        self._add_table_view_layout(df=empty_df)
        self.setLayout(self.layout)
