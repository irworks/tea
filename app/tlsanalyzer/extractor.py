import logging
import os

from zipfile import ZipFile


class Extractor:

    def __init__(self, work_dir, ipa_file):
        self.work_dir = work_dir
        self.ipa_file = ipa_file

    def extract(self):
        logging.info(f'Starting to extract {self.ipa_file}...')
        temp_dir = self.create_temp_dir()
        payload_folder = self.extract_ipa(temp_dir)
        if not payload_folder:
            logging.warning(f'Payload folder not found after extracting .ipa. Skipping app.')
            raise FileNotFoundError

        app_folder = self.find_app_dir(payload_folder)
        if not app_folder:
            logging.warning(f'App folder not found inside Payload folder. Skipping app.')
            raise FileNotFoundError

        return app_folder

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
    def extract_ipa(self, destination):
        # If already extracted, return target path
        target_path = os.path.join(destination, 'Payload')
        if os.path.isdir(target_path):
            logging.info('Skipping extraction, Payload folder already there!')
            return target_path

        with ZipFile(os.path.join(self.work_dir, self.ipa_file), 'r') as ipa:
            ipa.extractall(destination)

        # check if this was a valid .ipa (if it contained a Payload/)
        if not os.path.isdir(target_path):
            return False

        return target_path

    '''
    Find the final app dir, it should be a folder inside
    Payload/ with an .app suffix.
    '''
    def find_app_dir(self, payload_folder):
        for filename in os.listdir(payload_folder):
            if filename.endswith('.app'):
                logging.info(f'Found the folder: {filename}')
                return os.path.join(payload_folder, filename)
        return False
