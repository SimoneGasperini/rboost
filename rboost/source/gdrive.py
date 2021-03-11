import os
from tqdm import tqdm
import pandas as pd
import networkx as nx

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from rboost.utils.exception import RBException


class GDrive ():

  mimetypes = {'folder' : 'application/vnd.google-apps.folder',
               'pkl'    : 'application/octet-stream',
               'json'   : 'application/json',
               'pdf'    : 'application/pdf',
               'txt'    : 'text/plain',
               'tif'    : 'image/tiff',
               'tiff'   : 'image/tiff',
               'png'    : 'image/png',
               'jpg'    : 'image/jpeg',
               'jpeg'   : 'image/jpeg',
               'gif'    : 'image/gif',
               'svg'    : 'image/svg+xml',
               'bmp'    : 'image/bmp'}


  def __init__ (self, client_secrets_file, credentials_file,
                gd_folders, downloads_path, database_pkl, network_pkl):

    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_file
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile(credentials_file)

    if gauth.credentials is None:
      gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
      gauth.Refresh()
    else:
      gauth.Authorize()

    gauth.SaveCredentialsFile(credentials_file)

    self.service = GoogleDrive(gauth)

    self.gd_folders = gd_folders
    self.downloads_path = downloads_path
    self.database_pkl = database_pkl
    self.network_pkl = network_pkl


  def get_ID_from_name (self, name):
    '''
    Get the file/folder Google Drive ID from its name


    Parameters
    ----------
    name : str
      File/folder name

    Returns
    -------
    ID : str
      File/folder ID
    '''

    ID = None

    if name == 'root':
      ID = 'root'

    else:
      query = f'title = "{name}"'
      files_list = self.service.ListFile({'q':query}).GetList()

      if len(files_list) == 0:
        RBException(state='failure', message=f'No file/folder named "{name}" exists on Google Drive')
      elif len(files_list) > 1:
        RBException(state='failure', message=f'More that one file/folder named "{name}" exists on Google Drive')
      else:
        ID = files_list[0]['id']

    return ID


  def reset (self):
    '''
    Reset the Google Drive database
    '''

    files_list = self.service.ListFile().GetList()

    for file in tqdm(files_list, desc='Deleting files', ncols=80):
      file.Delete()

    for foldername in self.gd_folders:
      self.create_folder(foldername=foldername)

    df = pd.DataFrame(columns=['DATE','USER/AUTHOR','DOCNAME','DOCTYPE'])
    df.to_pickle(self.database_pkl)
    self.upload_file(self.database_pkl)
    os.remove(self.database_pkl)

    nx.readwrite.write_gpickle(nx.Graph(), self.network_pkl)
    self.upload_file(self.network_pkl)
    os.remove(self.network_pkl)


  def create_folder (self, foldername, parent_folder='root'):
    '''
    If not exists yet, create a new folder in the specified parent folder


    Parameters
    ----------
    foldername : str
      Folder name

    parent_folder : str, default='root'
      Parent folder name
    '''

    exists = foldername in self.list_folder(foldername=parent_folder, field='title')

    if not exists:

      parent_folder_id = self.get_ID_from_name(name=parent_folder)
  
      folder = self.service.CreateFile({'title'    : foldername,
                                        'parents'  : [{'id':parent_folder_id}],
                                        'mimeType' : self.mimetypes['folder']})
      folder.Upload()


  def list_folder (self, foldername, field=None):
    '''
    List the contents of a folder selecting the specified field if passed


    Parameters
    ----------
    foldername : str
      Folder name

    field : str, default=None
      Specific field

    Returns
    -------
    contents : list of str
      Folder contents
    '''

    folder_id = self.get_ID_from_name(name=foldername)
    query = f'"{folder_id}" in parents'
    contents = self.service.ListFile({'q':query}).GetList()

    if field is not None:
      contents = [file[field] for file in contents]

    return contents


  def upload_file (self, filepath, parent_folder='root'):
    '''
    Create/update a file uploading a local file in the specified parent folder


    Parameters
    ----------
    filepath : str
      Local file path

    parent_folder : str, default='root'
      Parents folder name
    '''

    filename = os.path.basename(filepath)
    exists = filename in self.list_folder(foldername=parent_folder, field='title')

    if exists:
      file_id = self.get_ID_from_name(name=filename)
      file = self.service.CreateFile({'id' : file_id})

    else:
      extension = filename.split('.')[-1]
      parent_folder_id = self.get_ID_from_name(name=parent_folder)
      file = self.service.CreateFile({'title'    : filename,
                                      'parents'  : [{'id':parent_folder_id}],
                                      'mimeType' : self.mimetypes[extension]})

    file.SetContentFile(filepath)
    file.Upload()


  def download_file (self, filename, parent_folder='root', subdir=None):
    '''
    Download a file in the specified parent folder to the local downloads sub-directory


    Parameters
    ----------
    filename : str
      File name

    parent_folder : str, default='root'
      Parent folder name

    subdir : str, default=None
      Optional sub-directory
    '''

    parent_folder_id = self.get_ID_from_name(name=parent_folder)
    query = f'title = "{filename}" and "{parent_folder_id}" in parents'
    file = self.service.ListFile({'q':query}).GetList()[0]

    subdir = subdir + '/' if subdir is not None else ''
    file.GetContentFile(self.downloads_path + subdir + filename)


  def download_folder (self, foldername):
    '''
    Download a folder to the local downloads directory


    Parameters
    ----------
    foldername : str
      Folder name
    '''

    os.makedirs(self.downloads_path + foldername, exist_ok=True)

    filenames = self.list_folder(foldername, field='title')

    for filename in tqdm(filenames, desc='Downloading files', ncols=80):
      self.download_file(filename, parent_folder=foldername, subdir=foldername)
