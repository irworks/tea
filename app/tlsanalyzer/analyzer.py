import logging
import os.path

from urllib.parse import urlparse
from app.models import IosApp, Url, Domain, AppAtsExceptions
from app.tlsanalyzer.extractor import Extractor
from app.tlsanalyzer.helper.hash import calculate_hash
from app.tlsanalyzer.modules.info_plist_analyzer import InfoPlistAnalyzer
from app.tlsanalyzer.modules.url_extractor import UrlExtractor


class Analyzer:

    def __init__(self, work_dir, ipa_file, rescan_urls, num, total_count, db, all_urls, all_domains, all_ats_exceptions):
        self.work_dir = work_dir
        self.ipa_file = ipa_file
        self.rescan_urls = rescan_urls
        self.num = num
        self.total_count = total_count
        self.db = db
        self.all_urls = all_urls
        self.all_domains = all_domains
        self.all_ats_exceptions = all_ats_exceptions

        self.info_plist_results = {}
        self.added_urls = []
        self.added_domains = []
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
            app = IosApp(file_hash, '', '', '', '', '', 0)
        else:
            # Bad Hack: Clear out current ats_app_exceptions data to prevent duplicates
            '''
            The reasoning behind this is that appending app_ats_exceptions models a second time does not trigger an update,
            SQLAlchemy always tries to insert which is a UNIQUE condition violation.
            Suspected reason for this behaviour is the specific AppAtsExceptions model which is explicitly
            instantiated and presumably considered as always a new entry.   
            '''
            self.db.session.query(AppAtsExceptions).filter(AppAtsExceptions.app_id == app.id).delete()
            self.db.session.commit()

        self.info_plist_results = self.analyze_info_plist(app_path)

        # Extract URLs
        urls = self.extract_urls(app_path, self.rescan_urls)

        url_keys = self.all_urls.keys()
        domain_keys = self.all_domains.keys()
        domains_in_app = []
        for url in urls:
            # Extract domain from URL
            domain = urlparse(url).netloc

            # Check if this URL is new, if not use the existing one
            if url not in url_keys:
                logging.debug(f'Found new url: {url}')
                model = Url(url)
                self.added_urls.append(model)
            else:
                model = self.all_urls[url]

            self.db.session.add(model)
            app.urls.append(model)

            # Add somewhat useful domains to the list
            if domain and len(domain) > 3:
                domains_in_app.append(domain)

        # Filter out domain duplicates
        for domain in set(domains_in_app):
            if domain not in domain_keys:
                logging.debug(f'Found new domain: {domain}')
                model = Domain(domain)
                self.added_domains.append(model)
                self.all_domains[domain] = model
            else:
                model = self.all_domains[domain]

            self.db.session.add(model)
            app.domains.append(model)

        results = self.info_plist_results

        # Set ATS Exceptions
        for exception in results['ats']:
            key = exception['key']
            domain = exception['domain']
            domain_model = None
            if domain:
                if domain not in domain_keys:
                    domain_model = Domain(domain)
                    self.added_domains.append(domain_model)
                    self.all_domains[domain] = domain_model
                    self.db.session.add(domain_model)

                domain_model = self.all_domains[domain]

            aae = AppAtsExceptions()
            aae.exception = self.all_ats_exceptions[key]
            aae.app = app
            if domain_model:
                aae.domain = domain_model

            self.db.session.add(aae)

        # Prepare database model
        app.name = results['name']
        app.bundle_id = results['bundle_identifier']
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

