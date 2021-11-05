import sys

import click
from PySide2.QtWidgets import QApplication

from rboost.rboost import RBoost
from rboost.gui.mainwindow import MainWindow


@click.command()
def rboost():
    app = QApplication(sys.argv)
    window = MainWindow(rboost=RBoost())
    window.show()
    sys.exit(app.exec_())
