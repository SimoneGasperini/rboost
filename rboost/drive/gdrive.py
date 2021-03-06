import os
import sys
import io
import pickle

import networkx as nx
import pandas as pd
import colorama

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient import discovery


class GDrive ():

  client_secret_file = 'client_secret_file.json'
  api_name = 'drive'
  api_version = 'v3'
  scopes = ['https://www.googleapis.com/auth/drive']

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

    self.gdrive_path = gdrive_path
    self.gdrive_folders = gdrive_folders
    self.database_pkl = database_pkl
    self.network_pkl = network_pkl
    self.downloads_path = downloads_path

    self.service = self._create_service()


  def _create_service (self):

    cred = None
    pickle_file = self.gdrive_path + f'token_{self.api_name}_{self.api_version}.pkl'

    if os.path.exists(pickle_file):
      with open(pickle_file, 'rb') as token:
        cred = pickle.load(token)

    if not cred or not cred.valid:
      if cred and cred.expired and cred.refresh_token:
        cred.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(self.gdrive_path + self.client_secret_file,
                                                         self.scopes)
        cred = flow.run_local_server()

      with open(pickle_file, 'wb') as token:
        pickle.dump(cred, token)

    try:
      service = discovery.build(self.api_name, self.api_version, credentials=cred)
      return service

    except:
      colorama.init()
      message = 'FAIL: The connection to Google Drive service failed'
      print('>>> \033[91m' + message + '\033[0m')
      sys.exit()


  def _clear (self):

    response = self.service.files().list().execute()
    files = [file['id'] for file in response.get('files')]

    for file in files:
      self.service.files().delete(fileId=file).execute()


  def _reset (self):

    self._clear()

    for foldername in self.gdrive_folders:
      self.create_folder(foldername)

    df = pd.DataFrame(columns=['DATE','AUTHOR','DOCNAME','DOCTYPE','REFERENCE'])
    df.to_pickle(self.database_pkl)
    self.upload_file(self.database_pkl)
    os.remove(self.database_pkl)

    nx.readwrite.write_gpickle(nx.Graph(), self.network_pkl)
    self.upload_file(self.network_pkl)
    os.remove(self.network_pkl)


  def get_id (self, name):

    query = f'name = "{name}"'
    response = self.service.files().list(q=query).execute()
    file_id = response.get('files')[0]['id']

    return file_id


  def get_mimetype (self, filename):

    extension = filename.split('.')[-1]
    mimetype = self.mimetypes[extension]

    return mimetype


  def create_folder (self, foldername):

    mimetype = self.mimetypes['folder']

    file_metadata = {'name'     : foldername,
                     'mimeType' : mimetype}

    self.service.files().create(body=file_metadata).execute()


  def list_folder (self, foldername, field='name'):

    folder_id = self.get_id(foldername)
    query = f'parents = "{folder_id}"'

    response = self.service.files().list(q=query).execute()
    files = [file[field] for file in response.get('files')]

    return files


  def upload_file (self, filepath, foldername=None):

    filename = os.path.basename(filepath)
    file_metadata = {'name' : filename}

    if foldername is not None:
      folder_id = self.get_id(foldername)
      file_metadata['parents'] = [folder_id]

    mimetype = self.get_mimetype(filename)
    media = MediaFileUpload(filename=filepath, mimetype=mimetype)

    self.service.files().create(body=file_metadata, media_body=media).execute()


  def update_file (self, filepath, foldername=None):

    filename = os.path.basename(filepath)
    file_id = self.get_id(filename)
    file_metadata = self.service.files().get(fileId=file_id).execute()
    del file_metadata['id']

    if foldername is not None:
      folder_id = self.get_id(foldername)
      file_metadata['parents'] = [folder_id]

    mimetype = self.get_mimetype(filename)
    media = MediaFileUpload(filename=filepath, mimetype=mimetype)

    self.service.files().update(fileId=file_id, body=file_metadata, media_body=media).execute()


  def download_file (self, filename, directory=None):

    file_id = self.get_id(filename)
    request = self.service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd=fh, request=request)

    done = False
    while not done:
      status, done = downloader.next_chunk()

    if directory is None:
      directory = self.downloads_path

    with open(directory + filename, 'wb') as file:
      file.write(fh.getvalue())


  def download_folder (self, foldername):

    os.makedirs(self.downloads_path + foldername, exist_ok=True)

    filenames = self.list_folder(foldername)
    for fname in filenames:
      self.download_file(fname, directory=foldername)
