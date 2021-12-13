import logging
import os.path

from webapp.app.models import IosApp, Url
from webapp.app.tlsanalyzer.extractor import Extractor
from webapp.app.tlsanalyzer.helper.hash import calculate_hash
from webapp.app.tlsanalyzer.modules.info_plist_analyzer import InfoPlistAnalyzer
from webapp.app.tlsanalyzer.modules.url_extractor import UrlExtractor


class Analyzer:

    def __init__(self, work_dir, ipa_file, rescan_urls, num, total_count, db, all_urls):
        self.work_dir = work_dir
        self.ipa_file = ipa_file
        self.rescan_urls = rescan_urls
        self.num = num
        self.total_count = total_count
        self.db = db
        self.all_urls = all_urls

        self.info_plist_results = {}
        self.added_urls = []
        self.analyze()

    def analyze(self):
        extractor = Extractor(work_dir=self.work_dir, ipa_file=self.ipa_file)
        try:
            app_path = extractor.extract()
        except FileNotFoundError:
            return

        logging.info(f'[{self.num}/{self.total_count}] Starting to analyze {self.ipa_file}...')

        # Calculate hash and try to find in database
        # If found, use model. If not insert with dummy data and update later
        file_hash = calculate_hash(os.path.join(self.work_dir, self.ipa_file))
        logging.info(f'[Hash] {self.ipa_file} - {file_hash}')

        app = IosApp.query.filter_by(file_hash=file_hash).first()
        if app is None:
            app = IosApp(file_hash, '', '', '', '', 0)

        self.info_plist_results = self.analyze_info_plist(app_path)

        # Extract URLs
        urls = self.extract_urls(app_path, self.rescan_urls)

        url_keys = self.all_urls.keys()
        for url in urls:
            if url not in url_keys:
                logging.debug(f'Found new url: {url}')
                model = Url(url)
                self.added_urls.append(model)
            else:
                model = self.all_urls[url]

            self.db.session.add(model)
            app.urls.append(model)

        results = self.info_plist_results

        # Prepare database model
        app.name = results['name']
        app.version = results['version']
        app.build = results['build']
        app.sdk = results['sdk']
        app.min_ios = results['min_os']
        self.db.session.add(app)

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

