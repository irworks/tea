import logging
import os.path

from tlsanalyzer.extractor import Extractor
from tlsanalyzer.modules.info_plist_analyzer import InfoPlistAnalyzer


class Analyzer:

    def __init__(self, work_dir, ipa_file):
        self.work_dir = work_dir
        self.ipa_file = ipa_file
        self.info_plist_results = {}
        self.analyze()

    def analyze(self):
        extractor = Extractor(work_dir=self.work_dir, ipa_file=self.ipa_file)
        try:
            app_path = extractor.extract()
        except FileNotFoundError:
            return

        logging.info(f'Starting to analyze {self.ipa_file}...')
        self.info_plist_results = self.analyze_info_plist(app_path)

    def analyze_info_plist(self, app_path):
        info_plist_path = os.path.join(app_path, 'Info.plist')
        if not os.path.isfile(info_plist_path):
            logging.warning('App does not contain a Info.plist. Skipping .plist checks.')
            return False

        analyzer = InfoPlistAnalyzer(info_plist_path)
        return analyzer.analyze()

    def ats_exceptions(self):
        return self.info_plist_results['ats']

