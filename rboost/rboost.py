import os
import warnings
import webbrowser
from datetime import datetime

import pandas as pd
import networkx as nx
import nltk

from rboost.__config import get_config_install, get_client_secrets, get_icons, get_logo
from rboost.source.gdrive import GDrive
from rboost.source.database import Database
from rboost.source.network import Network


class RBoost:

    def __init__(self):
        self.CONFIG_INSTALL = get_config_install()
        self.CLIENT_SECRETS = get_client_secrets()
        self.icons = get_icons()
        self.logo = get_logo()
        self._configure()

    def _configure(self):
        self._set_python_warnings()
        self._set_data_dir_path()
        self._set_sub_dirs_paths()
        self._create_dirs()
        self._set_documents_df_cols()
        self._set_labels_df_cols()
        self._download_nltk_wordnet()
        self._set_gdrive_folders()
        self._set_gdrive_object()
        self._set_database_object()
        self._set_network_object()
        self._set_external_links()

    def _set_python_warnings(self):
        self.warnings_level = self.CONFIG_INSTALL['python_warnings']
        warnings.filterwarnings(self.warnings_level)

    def _set_data_dir_path(self):
        data_dir = self.CONFIG_INSTALL['data_dir']
        self.data_dir_path = os.path.expanduser(data_dir)

    def _set_sub_dirs_paths(self):
        sub_dirs = self.CONFIG_INSTALL['sub_dirs']
        self.pdfs_dir_path = os.path.expanduser(sub_dirs['pdfs_dir'])
        self.notebooks_dir_path = os.path.expanduser(sub_dirs['notebooks_dir'])
        self.remarks_dir_path = os.path.expanduser(sub_dirs['remarks_dir'])
        self.downloads_dir_path = os.path.expanduser(sub_dirs['downloads_dir'])

    def _create_dirs(self):
        os.makedirs(self.data_dir_path, exist_ok=True)
        os.makedirs(self.pdfs_dir_path, exist_ok=True)
        os.makedirs(self.notebooks_dir_path, exist_ok=True)
        os.makedirs(self.remarks_dir_path, exist_ok=True)
        os.makedirs(self.downloads_dir_path, exist_ok=True)

    def _set_documents_df_cols(self):
        self.documents_df_cols = self.CONFIG_INSTALL['documents_df_cols']

    def _set_labels_df_cols(self):
        self.labels_df_cols = self.CONFIG_INSTALL['labels_df_cols']

    def _download_nltk_wordnet(self):
        nltk.download('wordnet', quiet=True)

    def _set_gdrive_folders(self):
        self.gdrive_folders = self.CONFIG_INSTALL['gdrive_folders']

    def _set_gdrive_object(self):
        credentials_file = self.data_dir_path + 'credentials.txt'
        self.gdrive = GDrive(client_secrets_file=self.CLIENT_SECRETS,
                             credentials_file=credentials_file,
                             downloads_path=self.downloads_dir_path)

    def _set_database_object(self):
        filepath = self.downloads_dir_path + 'database.pkl'
        self.database = Database(filepath=filepath, gdrive=self.gdrive)

    def _set_network_object(self):
        filepath = self.downloads_dir_path + 'network.pkl'
        self.network = Network(filepath=filepath, gdrive=self.gdrive)

    def _set_external_links(self):
        self.source_code_url = self.CONFIG_INSTALL['source_code_url']
        self.online_docs_url = self.CONFIG_INSTALL['online_docs_url']

    @property
    def today(self):
        return datetime.today().strftime('%d-%m-%Y')

    @property
    def users(self):
        colname = self.documents_df_cols['user']
        return set(self.database.dataframe[colname])

    @property
    def docnames(self):
        colname = self.documents_df_cols['docname']
        return set(self.database.dataframe[colname])

    @property
    def doctypes(self):
        colname = self.documents_df_cols['doctype']
        return set(self.database.dataframe[colname])

    @property
    def labnames(self):
        return set(self.network.graph)

    @property
    def labtypes(self):
        labtypes_list = [self.network.graph.nodes[node]['label'].types
                         for node in self.network.graph.nodes]
        return set().union(*labtypes_list)

    def reset_gdrive(self):
        self.empty_gdrive()
        self.init_database_gdrive()
        self.init_network_gdrive()

    def empty_gdrive(self):
        for file in self.gdrive.service.ListFile().GetList():
            file.Delete()

    def init_database_gdrive(self):
        for foldername in self.gdrive_folders:
            self.gdrive.create_folder(foldername)
        df_cols = list(self.documents_df_cols.values())
        dataframe = pd.DataFrame(df_cols)
        dataframe.to_pickle(self.database.filepath)
        self.gdrive.upload_file(self.database.filepath)
        os.remove(self.database.filepath)

    def init_network_gdrive(self):
        graph = nx.Graph()
        nx.readwrite.write_gpickle(graph, self.network.filepath)
        self.gdrive.upload_file(self.network.filepath)
        os.remove(self.network.filepath)

    def go_to_source_code(self):
        webbrowser.open(self.source_code_url)

    def go_to_online_docs(self):
        webbrowser.open(self.online_docs_url)
