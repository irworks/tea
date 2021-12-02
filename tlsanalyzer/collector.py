import logging
import os


class Collector:

    def __init__(self, work_dir):
        self.apps = []
        self.work_dir = work_dir

    def collect(self):
        if not os.path.exists(self.work_dir) or not os.path.isdir(self.work_dir):
            logging.error(f'Unable to collect apps from {self.work_dir}. Invalid path!')
            raise FileNotFoundError

        logging.info(f'Start collecting files from {self.work_dir}')
        for filename in os.listdir(self.work_dir):
            if not filename.endswith('.ipa'):
                continue

            logging.info(f'Adding {filename} to app list.')
            self.apps.append(filename)
        return self.apps


