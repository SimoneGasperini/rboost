from rboost.cli.rboost import RBoost

from rboost.cli.welcome import Welcome

from rboost.cli.download import Download

from rboost.cli.upload.uploadpdfs import UploadPdfs
from rboost.cli.upload.writenotebook import WriteNotebook
from rboost.cli.upload.writeremark import WriteRemark

from rboost.cli.list.listdocuments import ListDocuments
from rboost.cli.list.listlabels import ListLabels

from rboost.cli.visualize.shownetwork import ShowNetwork
from rboost.cli.visualize.showlabels import ShowLabels
from rboost.cli.visualize.printlabel import PrintLabel
from rboost.cli.visualize.loclabel import LocLabel
from rboost.cli.visualize.findpath import FindPath


if __name__ == '__main__':

  RBoost.run()
