import os
import sys
from stat import S_IREAD, S_IWUSR

from gensim.parsing.preprocessing import strip_punctuation
from gensim.parsing.preprocessing import strip_non_alphanum

from rboost.source.document.base import Document
from rboost.source.document.figure import Figure
from rboost.utils.exceptions import Exceptions


class Notebook (Document):
    """
    Class for the Notebook object


    Parameters
    ----------
      date : str
        Notebook date (dd-mm-yyyy)

      user : str
        Notebook author (name-surname)

      path : str
        Notebook local path
    """

    def __init__(self, date, user, path):

        name = date + '_' + user + '.txt'
        doctype = 'notebook'

        super(Notebook, self).__init__(date=date, user=user,
                                       path=path, name=name,
                                       doctype=doctype)

        self.figures = self.get_figures()

    @property
    def docname(self):
        """
        Full Notebook name (str)
        """

        docname = os.path.basename(self.path[:-1]) + '/' + self.name

        return docname

    def open_editor(self):
        """
        Open the document using the system's basic text editor
        """

        filepath = self.path + self.name

        if not os.path.exists(filepath):
            with open(filepath, mode='w') as file:
                file.write('#TEXT\n\n#FIGURES\n\n')

        os.chmod(filepath, S_IWUSR | S_IREAD)

        if sys.platform.startswith('win'):
            os.system('notepad ' + filepath)
        if sys.platform.startswith('linux'):
            os.system('gedit ' + filepath)
        if sys.platform.startswith('darwin'):
            os.system('open -a TextEdit ' + filepath)

        os.chmod(filepath, S_IREAD)

    def read(self):
        """
        Get all the raw text extracted from the Notebook document


        Returns
        -------
        text : str
          Extracted raw text
        """

        with open(self.path + self.name, mode='r') as file:
            text = file.read()

        return text

    def get_text(self):
        """
        Get the pre-processed text extracted from the Notebook '#TEXT' section


        Returns
        -------
        text : str
          Extracted text
        """

        lines = self.read().splitlines()
        raw_text = ' '.join(
            [line for line in lines[1:lines.index('#FIGURES')]])
        text = strip_non_alphanum(strip_punctuation(raw_text.lower()))

        return text

    def get_figs_paragraph(self):
        """
        Get the raw text extracted from the Notebook '#FIGURES' section


        Returns
        -------
        text : str
          Extracted raw text
        """

        lines = self.read().splitlines()
        text = '\n'.join([line for line in lines[lines.index('#FIGURES')+1:]])

        return text

    def get_figures(self):
        """
        Get the Figure objects from the Notebook document


        Returns
        -------
        figures : list of Figure
          Figure objects
        """

        fig_names = [line[1:].strip()
                     for line in self.get_figs_paragraph().splitlines()
                     if line.startswith('-')]
        fig_captions = self.get_fig_captions()

        figures = [Figure(date=self.date, user=self.user, path=self.path, name=name, caption=caption)
                   for name, caption in zip(fig_names, fig_captions)]

        return figures

    def get_fig_captions(self):
        """
        Get the figures captions of the Notebook document


        Returns
        -------
        captions : list of str
          Figures captions
        """

        captions = []
        cap = ''

        for line in self.get_figs_paragraph().splitlines():

            if line.startswith('-'):
                if cap is not None:
                    captions.append(cap)
                cap = ''

            else:
                cap = cap + ' ' + line

        captions.append(cap)
        captions = [strip_non_alphanum(strip_punctuation(cap.lower()))
                    if not cap == '' else None
                    for cap in captions]

        return captions

    def check_figures(self):
        """
        Check if the Notebook directory contains all the figures files referenced
        in the Notebook document
        """

        missing = [fig.name for fig in self.get_figures()
                   if fig.name not in os.listdir(self.path)]

        if missing:
            e = Exceptions(state='failure',
                           message='The following files do not exist in the notebook directory:\n\t',
                           args=missing)
            e.throw()
