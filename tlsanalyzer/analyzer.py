import logging

from tlsanalyzer.extractor import Extractor


class Analyzer:

    def __init__(self, work_dir, ipa_file):
        self.work_dir = work_dir
        self.ipa_file = ipa_file
        self.analyze()

    def analyze(self):
        extractor = Extractor(work_dir=self.work_dir, ipa_file=self.ipa_file)
        try:
            app_path = extractor.extract()
        except FileNotFoundError:
            return

        logging.info(f'Starting to analyze {self.ipa_file}...')