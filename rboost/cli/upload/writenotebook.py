import os
import sys
from tqdm import tqdm

from rboost.cli.rboost import RBoost
from rboost.source.document.notebook import Notebook
from rboost.utils.autocomplete import AutoComplete
from rboost.utils.exceptions import Exceptions


@RBoost.subcommand ('write-notebook')
class WriteNotebook (RBoost):
  """
  Write a notebook on RBoost database
  """

  def main (self):

    dirname = self.create_directory()
    notebook = self.create_document(dirname)
    notebook.open_editor()

    notebook.check_figures()
    figures = notebook.get_figures()

    self.upload_files(notebook, figures)
    self.update_database(notebook, figures)
    self.update_network(notebook, figures)

    self.database.push()
    self.network.push()

  def create_directory (self):

    gdrive_notebooks = self.gdrive.list_folder(foldername='notebooks', field='title')

    with AutoComplete(options=gdrive_notebooks):
      dirname = input('>>> Notebook name : ')

    if dirname not in gdrive_notebooks:
      print(f'>>> The notebook "{dirname}" does not exist yet on RBoost database, do you want to create it?')
      answer = input('>>> (y/n) ')
      if answer == 'y':
        self.gdrive.create_folder(foldername=dirname, parent_folder='notebooks')
      else:
        sys.exit()

    else:
      print(f'>>> The notebook "{dirname}" already exists on RBoost database')

    os.makedirs(dirname, exist_ok=True)

    return dirname

  def create_document (self, dirname):

    print(f'>>> Do you want to create/edit a notebook page?')
    answer = input('>>> (y/n) ')
    if not answer == 'y':
      sys.exit()

    date = self.get_date()
    author = self.get_user()
    path = self.notebooks_path + dirname + '/'
    notebook = Notebook(date=date, user=author, path=path)

    if notebook.docname in self.docnames_list:
      e = Exceptions(state='failure',
                     message=f'The file "{notebook.docname}" already exists on RBoost database')
      e.throw()

    if not os.path.exists(notebook.path + notebook.name):
      with open(notebook.path + notebook.name, mode='w') as file:
        file.write('#TEXT\n\n#FIGURES\n\n')

    return notebook

  def upload_files (self, notebook, figures):

    print(f'>>> Do you want to upload the file "{notebook.docname}" on RBoost database?')
    answer = input('>>> (y/n) ')
    if not answer == 'y':
      sys.exit()

    print(f'>>> Uploading "{notebook.docname}"')

    folder = notebook.docname.split('/')[0]
    self.gdrive.create_folder(foldername=folder, parent_folder='notebooks')

    filepaths = [notebook.path + notebook.name] + [fig.path + fig.name for fig in figures]

    for filepath in tqdm(filepaths, desc='Uploading files', ncols=80):
      self.gdrive.upload_file(filepath=filepath, parent_folder=folder)

  def update_database (self, notebook, figures):

    data = [[fig.date, fig.user, fig.docname, fig.doctype] for fig in figures]
    data.append([notebook.date, notebook.user, notebook.docname, notebook.doctype])
    self.database.append_data(data)

  def update_network (self, notebook, figures):

    text = notebook.get_text()
    text_labs, text_links = notebook.get_data_from_text(text)
    figs_labs, figs_links = notebook.get_data_from_figures(figures)
    self.network.update_nodes(text_labs + figs_labs)
    self.network.update_edges(text_links + figs_links)
