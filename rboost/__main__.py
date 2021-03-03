from rboost.cli.rboost import RBoost

from rboost.cli.welcome import Welcome

from rboost.cli.uploading.uploadpdfs import UploadPdfs
from rboost.cli.uploading.writenotebook import WriteNotebook
from rboost.cli.uploading.writeremark import WriteRemark

from rboost.cli.listing.listdocuments import ListDocuments
from rboost.cli.listing.listlabels import ListLabels

from rboost.cli.visualizing.shownetwork import ShowNetwork
from rboost.cli.visualizing.showlabel import ShowLabel



if __name__ == '__main__':

  RBoost.run()
