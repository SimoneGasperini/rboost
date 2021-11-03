import os

from tqdm import tqdm
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from rboost.utils.exceptions import Exceptions


class GDrive:

    mimetypes = {'folder': 'application/vnd.google-apps.folder',
                 'pkl': 'application/octet-stream',
                 'json': 'application/json',
                 'pdf': 'application/pdf',
                 'txt': 'text/plain',
                 'tif': 'image/tiff',
                 'tiff': 'image/tiff',
                 'png': 'image/png',
                 'jpg': 'image/jpeg',
                 'jpeg': 'image/jpeg',
                 'gif': 'image/gif',
                 'svg': 'image/svg+xml',
                 'bmp': 'image/bmp'}

    def __init__(self, client_secrets_file, credentials_file, downloads_path):

        GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_file
        gauth = GoogleAuth()

        def _authenticate():
            gauth.LoadCredentialsFile(credentials_file)
            gauth.Authorize()

        try:
            _authenticate()
        except:
            if os.path.exists(credentials_file):
                os.remove(credentials_file)
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile(credentials_file)
            _authenticate()

        self.service = GoogleDrive(gauth)
        self.downloads_path = downloads_path

    def get_id_from_name(self, name):
        """
        Get the file/folder Google Drive ID from its name


        Parameters
        ----------
        name : str
          File/folder name

        Returns
        -------
        id_code : str
          File/folder id
        """

        id_code = None

        if name == 'root':
            id_code = 'root'

        else:
            query = f'title = "{name}"'
            files_list = self.service.ListFile({'q': query}).GetList()

            if len(files_list) == 0:
                e = Exceptions(state='failure',
                               message=f'No file/folder named "{name}" exists on Google Drive')
                e.throw()

            elif len(files_list) > 1:
                e = Exceptions(state='failure',
                               message=f'More that one file/folder named "{name}" exists on Google Drive')
                e.throw()

            else:
                id_code = files_list[0]['id']

        return id_code

    def create_folder(self, foldername, parent_folder='root'):
        """
        If not exists yet, create a new folder in the specified parent folder


        Parameters
        ----------
        foldername : str
          Folder name

        parent_folder : str, default='root'
          Parent folder name
        """

        exists = foldername in self.list_folder(
            foldername=parent_folder, field='title')

        if not exists:
            parent_folder_id = self.get_id_from_name(name=parent_folder)
            folder = self.service.CreateFile({'title': foldername,
                                              'parents': [{'id': parent_folder_id}],
                                              'mimeType': self.mimetypes['folder']})
            folder.Upload()

    def list_folder(self, foldername, field=None):
        """
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
        """

        folder_id = self.get_id_from_name(name=foldername)
        query = f'"{folder_id}" in parents'
        contents = self.service.ListFile({'q': query}).GetList()

        if field is not None:
            contents = [file[field] for file in contents]

        return contents

    def upload_file(self, filepath, parent_folder='root'):
        """
        Create/update a file uploading a local file in the specified parent folder


        Parameters
        ----------
        filepath : str
          Local file path

        parent_folder : str, default='root'
          Parents folder name
        """

        filename = os.path.basename(filepath)
        exists = filename in self.list_folder(
            foldername=parent_folder, field='title')

        if exists:
            file_id = self.get_id_from_name(name=filename)
            file = self.service.CreateFile({'id': file_id})

        else:
            extension = filename.split('.')[-1]
            parent_folder_id = self.get_id_from_name(name=parent_folder)
            file = self.service.CreateFile({'title': filename,
                                            'parents': [{'id': parent_folder_id}],
                                            'mimeType': self.mimetypes[extension]})
        file.SetContentFile(filepath)
        file.Upload()

    def download_file(self, filename, parent_folder='root'):
        """
        Download a file in the specified parent folder to the local downloads directory


        Parameters
        ----------
        filename : str
          File name

        parent_folder : str, default='root'
          Parent folder name
        """

        parent_folder_id = self.get_id_from_name(name=parent_folder)
        query = f'title = "{filename}" and "{parent_folder_id}" in parents'
        file = self.service.ListFile({'q': query}).GetList()[0]

        filepath = self.downloads_path + filename
        file.GetContentFile(filepath)

    def download_folder(self, foldername):
        """
        Download a folder to the local downloads directory


        Parameters
        ----------
        foldername : str
          Folder name
        """

        dirpath = self.downloads_path + foldername + '/'
        os.makedirs(dirpath, exist_ok=True)

        parent_folder_id = self.get_id_from_name(name=foldername)
        filenames = self.list_folder(foldername, field='title')

        for filename in tqdm(filenames, desc='Downloading files', ncols=80):

            query = f'title = "{filename}" and "{parent_folder_id}" in parents'
            file = self.service.ListFile({'q': query}).GetList()[0]

            filepath = dirpath + filename
            file.GetContentFile(filepath)
