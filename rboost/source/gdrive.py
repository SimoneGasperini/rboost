import os
import sys
import io
import pickle

import networkx as nx
import pandas as pd
import colorama
from tqdm import tqdm

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient import discovery


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
      colorama.init()
      message = 'FAIL: The connection to Google Drive service failed'
      print('>>> \033[91m' + message + '\033[0m')
      sys.exit()


  def _reset (self):
    '''
    Reset the Google Drive database
    '''

    response = self.service.files().list().execute()
    files = [file['id'] for file in response.get('files')]

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


  def get_id (self, name):
    '''
    Get the ID code of a file/folder on the drive


    Parameters
    ----------
    name : str
      File/folder name

    Returns
    -------
    ID : str
      File/folder ID
    '''

    query = f'name = "{name}"'
    response = self.service.files().list(q=query).execute()
    ID = response.get('files')[0]['id']

    return ID


  def get_mimetype (self, name):
    '''
    Get the mimetype of a file/folder on the drive


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


  def create_folder (self, foldername):
    '''
    Create a folder on the drive


    Parameters
    ----------
    foldername : str
      Folder name
    '''

    mimetype = self.mimetypes['folder']

    file_metadata = {'name'     : foldername,
                     'mimeType' : mimetype}

    self.service.files().create(body=file_metadata).execute()


  def list_folder (self, foldername, field='name'):
    '''
    List all the contents of a folder on the drive


    Parameters
    ----------
    foldername : str
      Folder name

    field : str, default='name'
      Metadata to be returned

    Returns
    -------
    contents : list of str
      Folder contents
    '''

    folder_id = self.get_id(foldername)
    query = f'parents = "{folder_id}"'

    response = self.service.files().list(q=query).execute()
    contents = [file[field] for file in response.get('files')]

    return contents


  def upload_file (self, filepath, foldername=None):
    '''
    Upload a local file into a folder on the drive


    Parameters
    ----------
    filepath : str
      Local path to the file

    foldername : str, default=None
      Name of the destination folder on the drive
    '''

    filename = os.path.basename(filepath)
    file_metadata = {'name' : filename}

    if foldername is not None:
      folder_id = self.get_id(foldername)
      file_metadata['parents'] = [folder_id]

    mimetype = self.get_mimetype(filename)
    media = MediaFileUpload(filename=filepath, mimetype=mimetype)

    self.service.files().create(body=file_metadata, media_body=media).execute()


  def update_file (self, filepath):
    '''
    Update the file on the drive by using the local file with same name


    Parameters
    ----------
    filepath : str
      Local path to the file
    '''

    filename = os.path.basename(filepath)
    file_id = self.get_id(filename)
    file_metadata = self.service.files().get(fileId=file_id).execute()
    del file_metadata['id']

    mimetype = self.get_mimetype(filename)
    media = MediaFileUpload(filename=filepath, mimetype=mimetype)

    self.service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()


  def download_file (self, filename, subdir=None):
    '''
    Download a file on the drive to the local downloads directory


    Parameters
    ----------
    filename : str
      File name

    subdir : str, default=None
      Optional local sub-directory
    '''

    file_id = self.get_id(filename)
    request = self.service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False
    while not done:
      status, done = downloader.next_chunk()

    directory = self.downloads_path
    if subdir is not None:
      directory += (subdir + '/')

    with open(directory + filename, 'wb') as file:
      file.write(fh.getvalue())


  def download_folder (self, foldername):
    '''
    Download a folder on the drive to the local downloads directory


    Parameters
    ----------
    foldername : str
      Folder name
    '''

    local_dir = self.downloads_path + foldername
    os.makedirs(local_dir)

    for filename in self.list_folder(foldername):
      self.download_file(filename, subdir=foldername)
