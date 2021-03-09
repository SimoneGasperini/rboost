import os
import io
import pickle
import networkx as nx
import pandas as pd
from tqdm import tqdm

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient import discovery

from rboost.utils.exception import RBException


class GDrive ():
  '''
  Class to handle Google Drive database


  Parameters
  ----------
    gdrive_path : str
      Local path to the client and token files

    gdrive_folders : list of str
      Google Drive folders

    database_pkl : str
      Local path to the database pickle file

    network_pkl : str
      Local path to the network pickle file

    downloads_path : str
      Local path to the downloads folder
  '''

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


  def __init__ (self, gdrive_path, gdrive_folders, database_pkl, network_pkl, downloads_path):

    self.pickle_file = gdrive_path + 'token.pkl'
    self.client_secret_file = gdrive_path + 'client.json'
    self.scopes = ['https://www.googleapis.com/auth/drive']

    self.gdrive_folders = gdrive_folders
    self.database_pkl = database_pkl
    self.network_pkl = network_pkl
    self.downloads_path = downloads_path

    self.service = self._create_service()


  def _create_service (self):
    '''
    Authenticate to Google Drive RBoost's account and create the service
    '''

    cred = None

    if os.path.exists(self.pickle_file):
      with open(self.pickle_file, 'rb') as token:
        cred = pickle.load(token)

    if not cred or not cred.valid:
      if cred and cred.expired and cred.refresh_token:
        cred.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_file,
                                                         self.scopes)
        cred = flow.run_local_server()

      with open(self.pickle_file, 'wb') as token:
        pickle.dump(cred, token)

    try:
      service = discovery.build('drive', 'v3', credentials=cred)
      return service

    except:
      RBException(state='failure', message='The connection to Google Drive service failed')


  def reset (self):
    '''
    Reset the Google Drive database
    '''

    response = self.service.files().list().execute()
    files = [file['id'] for file in response['files']]

    for file in tqdm(files, desc='Deleting files', ncols=80):
      self.service.files().delete(fileId=file).execute()

    for foldername in self.gdrive_folders:
      self.create_folder(foldername)

    df = pd.DataFrame(columns=['DATE','USER/AUTHOR','DOCNAME','DOCTYPE','REFERENCE TO'])
    df.to_pickle(self.database_pkl)
    self.upload_file(self.database_pkl)
    os.remove(self.database_pkl)

    nx.readwrite.write_gpickle(nx.Graph(), self.network_pkl)
    self.upload_file(self.network_pkl)
    os.remove(self.network_pkl)


  def get_id (self, name, parents=None):
    '''
    Get the ID code of a file/folder in the specified parents folder


    Parameters
    ----------
    name : str
      File/folder name

    parents : str, default=None
      Parents folder name

    Returns
    -------
    ID : str
      File/folder ID
    '''

    ID = None
    if name == 'root': return 'root'

    if parents is None:
      query = f'name = "{name}"'

    else:
      folder_id = self.get_id(name=parents)
      query = f'name = "{name}" and parents = "{folder_id}"'

    response = self.service.files().list(q=query).execute()
    filelist = response['files']

    if filelist:
      ID = filelist[0]['id']

    return ID


  def exists (self, name, parents=None):
    '''
    Check if a file/folder exists in the specified parents folder


    Parameters
    ----------
    name : str
      File/folder name

    parents : str, default=None
      Parents folder name

    Returns
    -------
    exists : bool
    '''

    exists = True if self.get_id(name, parents) is not None else False

    return exists


  def get_mimetype (self, name):
    '''
    Get the Google Drive mimetype of a file/folder


    Parameters
    ----------
    name : str
      File/folder name

    Returns
    -------
    mimetype : str
      File/folder mimetype
    '''

    if '.' not in name:
      return self.mimetypes['folder']

    extension = name.split('.')[-1]
    mimetype = self.mimetypes[extension]

    return mimetype


  def create_folder (self, foldername, parents='root'):
    '''
    If not exists yet, create a folder in the specified parents folder


    Parameters
    ----------
    foldername : str
      Folder name

    parents : str, default='root'
      Parents folder name
    '''

    if self.exists(foldername, parents): return

    file_metadata = {'name'     : foldername,
                     'mimeType' : self.mimetypes['folder'],
                     'parents'  : [self.get_id(name=parents)]}

    self.service.files().create(body=file_metadata).execute()


  def list_folder (self, foldername, parents=None, field='name'):
    '''
    List all the contents of a folder with the specified parents folder


    Parameters
    ----------
    foldername : str
      Folder name

    parents : str, default=None
      Parents folder name

    field : str, default='name'
      Metadata to be returned

    Returns
    -------
    contents : list of str
      Folder contents
    '''

    folder_id = self.get_id(foldername, parents)
    query = f'parents = "{folder_id}"'

    response = self.service.files().list(q=query).execute()
    contents = [file[field] for file in response['files']]

    return contents


  def upload_file (self, filepath, parents='root'):
    '''
    Create/update a file uploading a local file in the specified parents folder


    Parameters
    ----------
    filepath : str
      Local file path

    parents : str, default='root'
      Parents folder name
    '''

    filename = os.path.basename(filepath)

    if self.exists(filename, parents):
      self.update_file(filepath, parents)
      return

    file_metadata = {'name'    : filename,
                     'parents' : [self.get_id(name=parents)]} 

    mimetype = self.get_mimetype(filename)
    media = MediaFileUpload(filename=filepath, mimetype=mimetype)

    self.service.files().create(body=file_metadata, media_body=media).execute()


  def update_file (self, filepath, parents='root'):
    '''
    Update an uploaded file by using the local file with same name


    Parameters
    ----------
    filepath : str
      Local file path

    parents : str, default='root'
      Parents folder name
    '''

    filename = os.path.basename(filepath)
    file_id = self.get_id(filename, parents)

    file_metadata = self.service.files().get(fileId=file_id).execute()
    del file_metadata['id']

    mimetype = self.get_mimetype(filename)
    media = MediaFileUpload(filename=filepath, mimetype=mimetype)

    self.service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()


  def download_file (self, filename, parents='root', subdir=None):
    '''
    Download a file in the specified parents folder to the local downloads sub-directory


    Parameters
    ----------
    filename : str
      File name

    parents : str, default='root'
      Parents folder name

    subdir : str, default=None
      Optional sub-directory
    '''

    file_id = self.get_id(filename, parents)
    request = self.service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False
    while not done:
      status, done = downloader.next_chunk()

    subdir = (subdir + '/') if subdir is not None else ''
    local_dir = self.downloads_path + subdir
    os.makedirs(local_dir, exist_ok=True)

    with open(local_dir + filename, 'wb') as file:
      file.write(fh.getvalue())
