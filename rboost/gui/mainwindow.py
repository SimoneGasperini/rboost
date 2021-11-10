from PySide2.QtWidgets import QMainWindow, QAction, QMenuBar
from PySide2.QtGui import QIcon

from rboost.gui.home import HomeWindow
from rboost.gui.listdocuments import ListDocumentsWindow
from rboost.gui.listlabels import ListLabelsWindow


class MainWindow(QMainWindow):

    def __init__(self, rboost):
        super().__init__()
        self.rboost = rboost

        self.setWindowTitle('RBoost')
        self.setGeometry(100, 100, 1200, 800)
        self._set_icons()
        self.setWindowIcon(self.icons['rboost'])
        self._create_actions()
        self._create_menu_bar()
        self._connect_actions()

        self.home()

    def _set_icons(self):
        self.icons = {name: QIcon(path)
                      for name, path in self.rboost.icons.items()}

    def _create_actions(self):
        self.home_action = QAction(self.icons['home'], 'Home', self)

        self.search_action = QAction(self.icons['search'], 'Search', self)
        self.list_documents_action = QAction(
            self.icons['documents'], 'List documents', self)
        self.list_labels_action = QAction(
            self.icons['labels'], 'List labels', self)
        self.write_notebook_action = QAction(
            self.icons['notebook'], 'Write notebook', self)
        self.write_remark_action = QAction(
            self.icons['remark'], 'Write remark', self)
        self.upload_pdfs_action = QAction(
            self.icons['upload'], 'Upload PDFs', self)
        self.download_action = QAction(
            self.icons['download'], 'Download', self)

        self.find_path_action = QAction(self.icons['path'], 'Find path', self)
        self.print_label_action = QAction(
            self.icons['print'], 'Print label', self)
        self.loc_label_action = QAction(
            self.icons['loc'], 'Localize label', self)
        self.show_labels_action = QAction(
            self.icons['show'], 'Show labels', self)
        self.show_network_action = QAction(
            self.icons['network'], 'Show network', self)

        self.about_action = QAction(self.icons['about'], 'About', self)
        self.source_code_action = QAction(
            self.icons['code'], 'Source code', self)
        self.online_docs_action = QAction(
            self.icons['docs'], 'Online docs', self)

    def _create_menu_bar(self):
        menuBar = QMenuBar(self)

        home_menu = menuBar.addMenu('Homepage')
        home_menu.addAction(self.home_action)

        workspace_menu = menuBar.addMenu('Workspace')
        workspace_menu.addAction(self.search_action)
        workspace_menu.addAction(self.list_documents_action)
        workspace_menu.addAction(self.list_labels_action)
        workspace_menu.addAction(self.write_notebook_action)
        workspace_menu.addAction(self.write_remark_action)
        workspace_menu.addAction(self.upload_pdfs_action)
        workspace_menu.addAction(self.download_action)

        network_menu = menuBar.addMenu('Network')
        network_menu.addAction(self.find_path_action)
        network_menu.addAction(self.print_label_action)
        network_menu.addAction(self.loc_label_action)
        network_menu.addAction(self.show_labels_action)
        network_menu.addAction(self.show_network_action)

        help_menu = menuBar.addMenu('Help')
        help_menu.addAction(self.about_action)
        help_menu.addAction(self.source_code_action)
        help_menu.addAction(self.online_docs_action)

        self.setMenuBar(menuBar)

    def _connect_actions(self):
        self.home_action.triggered.connect(self.home)

        self.list_documents_action.triggered.connect(self.list_documents)
        self.list_labels_action.triggered.connect(self.list_labels)

        self.source_code_action.triggered.connect(
            self.rboost.go_to_source_code)
        self.online_docs_action.triggered.connect(
            self.rboost.go_to_online_docs)

    def home(self):
        home_window = HomeWindow(rboost=self.rboost)
        self.setCentralWidget(home_window)

    def list_documents(self):
        list_documents_window = ListDocumentsWindow(rboost=self.rboost)
        self.setCentralWidget(list_documents_window)

    def list_labels(self):
        list_labels_window = ListLabelsWindow(rboost=self.rboost)
        self.setCentralWidget(list_labels_window)
