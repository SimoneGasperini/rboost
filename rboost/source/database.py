import os
import pandas as pd


class Database:
    """
    Class for RBoost's documents database


    Parameters
    ----------
    filepath : str
      Local path to the database pickle file

    gdrive : gdrive.GDrive
      RBoost's Google Drive object
    """

    def __init__(self, filepath, gdrive):

        self.filepath = filepath
        self.gdrive = gdrive

        self.gdrive.download_file(filename=os.path.basename(self.filepath))
        self.dataframe = pd.read_pickle(self.filepath)

        os.remove(self.filepath)

    def push(self):
        """
        Write the database pickle file and upload it to Google Drive
        """

        self.dataframe.to_pickle(self.filepath)
        self.gdrive.upload_file(self.filepath)

        os.remove(self.filepath)

    def append_data(self, data):
        """
        Append new data to the dataframe according to its columns structure


        Parameters
        ----------
        data : list of list
          Structured data
        """

        df = pd.DataFrame(data=data, columns=self.dataframe.columns)
        self.dataframe = self.dataframe.append(df, ignore_index=True)
