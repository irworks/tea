import logging
import os

from zipfile import ZipFile


class Analyzer:

    def __init__(self, work_dir, ipa_file):
        self.work_dir = work_dir
        self.ipa_file = ipa_file
        self.start()

    def start(self):
        logging.info(f'Starting to analyze {self.ipa_file}...')
        temp_dir = self.create_temp_dir()
        self.extract_app(temp_dir)

    '''
    Create the (temporary) working directory inside which all files
    are being extracted to. 
    '''
    def create_temp_dir(self):
        # trim file name to remove extension
        app_name = self.ipa_file[:-4]
        temp_dir = os.path.join(self.work_dir, 'tls-analyzer', app_name)

        # if directory is already created => do not re-create
        if os.path.isdir(temp_dir):
            return temp_dir

        os.makedirs(temp_dir)
        return temp_dir

    '''
    Extract the .ipa (which is a glorified .zip) file to a 
    working directory in order to start all file analysis.
    '''
    def extract_app(self, destination):
        if os.path.isdir(os.path.join(destination, 'Payload')):
            logging.info('Skipping extraction, Payload folder already there!')
            return

        with ZipFile(os.path.join(self.work_dir, self.ipa_file), 'r') as ipa:
            ipa.extractall(destination)