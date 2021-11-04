import os
import sys
import warnings
from datetime import datetime

from plumbum import cli
from tqdm import tqdm
import pandas as pd
import networkx as nx
import nltk

from rboost.__config import get_config
from rboost.source.gdrive import GDrive
from rboost.source.database import Database
from rboost.source.network import Network
from rboost.utils.autocomplete import AutoComplete


class RBoost (cli.Application):

    CONFIG_INSTALL, CLIENT_SECRETS = get_config()

    def main(self):
        self.configure()
        if not self.nested_command:
            self.help()

    @property
    def today_date(self):
        return datetime.today().strftime('%d-%m-%Y')

    @property
    def users(self):
        return set(self.database.dataframe['USER/AUTHOR'])

    @property
    def docnames(self):
        return set(self.database.dataframe['DOCNAME'])

    @property
    def doctypes(self):
        return set(self.database.dataframe['DOCTYPE'])

    @property
    def labnames(self):
        return set(self.network.graph)

    @property
    def labtypes(self):
        labtypes_list = [self.network.graph.nodes[node]['label'].types
                         for node in self.network.graph.nodes]
        return set().union(*labtypes_list)

    def configure(self):
        self.set_python_warnings()
        self.set_data_dir_path()
        self.set_subdirs_paths()
        self.create_dirs()
        self.set_dataframe_columns()
        self.download_nltk_wordnet()
        self.set_gdrive_folders()
        self.set_gdrive_object()
        self.set_database_object()
        self.set_network_object()

    def set_python_warnings(self):
        RBoost.PYTHON_WARNINGS = self.CONFIG_INSTALL['python_warnings']
        warnings.filterwarnings(self.PYTHON_WARNINGS)

    def set_data_dir_path(self):
        rboost_data_dir = self.CONFIG_INSTALL['rboost_data_dir']
        RBoost.RBOOST_DATA_DIR = os.path.expanduser(rboost_data_dir)

    def set_subdirs_paths(self):
        sub_dirs = self.CONFIG_INSTALL['sub_dirs']
        RBoost.pdfs_path = os.path.expanduser(sub_dirs['pdfs_dir'])
        RBoost.notebooks_path = os.path.expanduser(sub_dirs['notebooks_dir'])
        RBoost.remarks_path = os.path.expanduser(sub_dirs['remarks_dir'])
        RBoost.downloads_path = os.path.expanduser(sub_dirs['downloads_dir'])

    def create_dirs(self):
        dirpaths = [self.RBOOST_DATA_DIR,
                    self.pdfs_path, self.notebooks_path,
                    self.remarks_path, self.downloads_path]
        for dirpath in dirpaths:
            os.makedirs(dirpath, exist_ok=True)

    def set_dataframe_columns(self):
        RBoost.DATAFRAME_COLUMNS = self.CONFIG_INSTALL['dataframe_columns']

    def download_nltk_wordnet(self):
        nltk.download('wordnet', quiet=True)

    def set_gdrive_folders(self):
        RBoost.GDRIVE_FOLDERS = self.CONFIG_INSTALL['gdrive_folders']

    def set_gdrive_object(self):
        credentials_file = self.RBOOST_DATA_DIR + 'credentials.txt'
        RBoost.gdrive = GDrive(client_secrets_file=self.CLIENT_SECRETS,
                               credentials_file=credentials_file,
                               downloads_path=self.downloads_path)

    def set_database_object(self):
        filepath = self.downloads_path + 'database.pkl'
        RBoost.database = Database(filepath=filepath, gdrive=self.gdrive)

    def set_network_object(self):
        filepath = self.downloads_path + 'network.pkl'
        RBoost.network = Network(filepath=filepath, gdrive=self.gdrive)

    def get_date(self, auto=False):
        if auto:
            date = self.today_date
        else:
            date = input('>>> Date (dd-mm-yyyy) : ')
        return date

    def get_user(self):
        users = self.users
        with AutoComplete(options=users):
            user = input('>>> User/author (name-surname) : ')
        if user not in users:
            print(
                f'>>> The user "{user}" does not exist yet on RBoost, do you want to create it?')
            answer = input('>>> (y/n) ')
            if not answer == 'y':
                sys.exit()
        return user

    def reset_gdrive(self):
        self.empty_gdrive()
        self.init_database_gdrive()
        self.init_network_gdrive()

    def empty_gdrive(self):
        files_list = self.gdrive.service.ListFile().GetList()
        for file in tqdm(files_list, desc='Deleting files', ncols=80):
            file.Delete()
        for foldername in self.GDRIVE_FOLDERS:
            self.gdrive.create_folder(foldername=foldername)

    def init_database_gdrive(self):
        dataframe = pd.DataFrame(columns=self.DATAFRAME_COLUMNS)
        dataframe.to_pickle(self.database.filepath)
        self.gdrive.upload_file(self.database.filepath)
        os.remove(self.database.filepath)

    def init_network_gdrive(self):
        graph = nx.Graph()
        nx.readwrite.write_gpickle(graph, self.network.filepath)
        self.gdrive.upload_file(self.network.filepath)
        os.remove(self.network.filepath)

    @staticmethod
    def show_dataframe(df, full=False):
        pd.set_option('colheader_justify', 'right')
        if full:
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_colwidth', None)
        print(df)
