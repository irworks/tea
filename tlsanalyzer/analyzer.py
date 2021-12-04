import logging
import os.path

from tlsanalyzer.extractor import Extractor
from tlsanalyzer.modules.info_plist_analyzer import InfoPlistAnalyzer
from tlsanalyzer.modules.url_extractor import UrlExtractor


class Analyzer:

    def __init__(self, work_dir, ipa_file, rescan_urls):
        self.work_dir = work_dir
        self.ipa_file = ipa_file
        self.rescan_urls = rescan_urls
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

        urls = self.extract_urls(app_path, self.rescan_urls)
        self.info_plist_results['urls'] = urls

    '''
    Extract app base information and ATS rules from Info.plist
    '''
    def analyze_info_plist(self, app_path):
        info_plist_path = os.path.join(app_path, 'Info.plist')
        if not os.path.isfile(info_plist_path):
            logging.warning('App does not contain a Info.plist. Skipping .plist checks.')
            return False

        analyzer = InfoPlistAnalyzer(info_plist_path)
        return analyzer.analyze()

    '''
    Extract all URLs which can be found in the binary and 
    companion files, filter out not interesting ones.
    '''
    def extract_urls(self, app_path, force=False):
        url_extractor = UrlExtractor(app_path)
        urls = url_extractor.find_urls(force)
        logging.info(f'Found {len(urls)} urls')
        return urls

    def ats_exceptions(self):
        return self.info_plist_results['ats']

