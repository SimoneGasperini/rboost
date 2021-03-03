import os
import sys
import pickle

import colorama

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery


class GDrive ():

  client_secret_file = 'client_secret_file.json'
  api_name = 'drive'
  api_version = 'v3'
  scopes = ['https://www.googleapis.com/auth/drive']


  def __init__ (self, path):

    self.path = path + '/rboost/drive/'
    self.service = self._create_service()


  def _create_service (self):

    cred = None
    pickle_file = self.path + f'token_{self.api_name}_{self.api_version}.pkl'

    if os.path.exists(pickle_file):
      with open(pickle_file, 'rb') as token:
        cred = pickle.load(token)

    if not cred or not cred.valid:
      if cred and cred.expired and cred.refresh_token:
        cred.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(self.path + self.client_secret_file,
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


  def create_folder (self, name):

    file_metadata = {'name'     : name,
                     'mimeType' : 'application/vnd.google-apps.folder'}

    self.service.files().create(body=file_metadata).execute()
