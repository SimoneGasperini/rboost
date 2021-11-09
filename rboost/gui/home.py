from PySide2.QtWidgets import QWidget, QLabel, QGridLayout
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QFont


class HomeWindow(QWidget):

    def __init__(self, rboost):
        super().__init__()
        self.rboost = rboost

        self.layout = QGridLayout()
        self._display_welcome()
        self._display_logo()
        self.setLayout(self.layout)

    def _display_welcome(self):
        message1 = QLabel('Welcome to RBoost!')
        message1.setFont(QFont('Arial', 48))
        message2 = QLabel('The network of science')
        message2.setFont(QFont('Arial', 30))
        self.layout.addWidget(message1, 0, 0, Qt.AlignCenter)
        self.layout.addWidget(message2, 1, 0, Qt.AlignCenter)

    def _display_logo(self):
        logo = QLabel()
        pixmap = QPixmap(self.rboost.logo)
        logo.setPixmap(pixmap)
        self.layout.addWidget(logo, 2, 0, Qt.AlignCenter)
