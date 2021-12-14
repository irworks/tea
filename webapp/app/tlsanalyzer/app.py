import json
import logging
import time

from webapp.app.models import Url, Domain, AtsException, AppAtsExceptions
from webapp.app.tlsanalyzer.analyzer import Analyzer
from webapp.app.tlsanalyzer.collector import Collector


class App:

    def __init__(self, work_dir, output_file, rescan_urls, db):
        self.work_dir = work_dir
        self.output_file = output_file
        self.rescan_urls = rescan_urls
        self.db = db
        self.all_urls_dict = {}
        self.all_domains_dict = {}
        self.all_ats_exceptions = {}

    def run(self):
        start_time = time.time()
        collector = Collector(self.work_dir)
        try:
            apps = collector.collect()
        except FileNotFoundError:
            return

        num = 1
        total_count = len(apps)
        insecure_apps = []

        '''
        Yes, doing this in memory is significantly faster than querying
        for each url if it already is in the database 
        '''
        self.init_ats_exceptions()
        self.add_urls_to_dict(Url.query.all())
        self.add_domains_to_dict(Domain.query.all())
        self.add_ats_exceptions_to_dict(AtsException.query.all())

        # Bad Hack: Clear out current ats_app_exceptions data to prevent duplicates
        '''
        The reasoning behind this is that appending app_ats_exceptions models a second time does not trigger an update,
        SQLAlchemy always tries to insert which is a UNIQUE condition violation.
        Suspected reason for this behaviour is the specific AppAtsExceptions model which is explicitly
        instantiated and presumably considered as always a new entry.   
        '''
        self.db.session.query(AppAtsExceptions).delete()
        self.db.session.commit()

        ats_exceptions = 0
        for app in apps:
            analyzer = Analyzer(self.work_dir, app, self.rescan_urls, num, total_count, self.db,
                                self.all_urls_dict, self.all_domains_dict, self.all_ats_exceptions)
            num += 1
            if analyzer.ats_exceptions():
                results = analyzer.info_plist_results
                ats_exceptions += len(results['ats'])
                insecure_apps.append(results)

            # add the newly discovered url models to the local cache
            self.add_urls_to_dict(analyzer.added_urls)
            self.add_domains_to_dict(analyzer.added_domains)

        self.db.session.commit()

        logging.info('')
        logging.info('--- Analysis complete ---')
        logging.info(f'Rescanned URLs: {self.rescan_urls}')
        logging.info(f'Duration: {round(time.time() - start_time, 2)}s')
        logging.info(f'ATS exceptions: {len(insecure_apps)} / {len(apps)}')
        logging.info(f'Total count of ATS exceptions: {ats_exceptions}')
        logging.info(f'Results: {self.output_file}')

        results = open(self.output_file, 'w')
        # magic happens here to make it pretty-printed
        results.write(json.dumps(insecure_apps))
        results.close()

    def init_ats_exceptions(self):
        ats_exceptions = [
            {'key': 'NSPinnedDomains', 'state': 0},
            {'key': 'NSExceptionMinimumTLSVersion-TLSv1.3', 'state': 0},
            {'key': 'NSRequiresCertificateTransparency', 'state': 0},
            {'key': 'NSExceptionDomains', 'state': 1},
            {'key': 'NSExceptionMinimumTLSVersion-TLSv1.2', 'state': 2},
            {'key': 'NSAllowsArbitraryLoads', 'state': 3},
            {'key': 'NSAllowsArbitraryLoadsInWebContent', 'state': 3},
            {'key': 'NSAllowsArbitraryLoadsForMedia', 'state': 3},
            {'key': 'NSAllowsLocalNetworking', 'state': 3},
            {'key': 'NSExceptionAllowsInsecureHTTPLoads', 'state': 3},
            {'key': 'NSIncludesSubdomains', 'state': 3},
            {'key': 'NSExceptionMinimumTLSVersion-TLSv1.0', 'state': 3},
            {'key': 'NSExceptionMinimumTLSVersion-TLSv1.1', 'state': 3},
            {'key': 'NSExceptionRequiresForwardSecrecy', 'state': 3}
        ]

        for ats_exception in ats_exceptions:
            key = ats_exception['key']
            model = AtsException.query.filter_by(key=key).first()
            if model is None:
                model = AtsException(key, ats_exception['state'])
            self.db.session.add(model)

        self.db.session.commit()

    def add_urls_to_dict(self, models):
        for urlModel in models:
            self.all_urls_dict[urlModel.path] = urlModel

    def add_domains_to_dict(self, models):
        for domainModel in models:
            self.all_domains_dict[domainModel.name] = domainModel

    def add_ats_exceptions_to_dict(self, models):
        for atsModel in models:
            self.all_ats_exceptions[atsModel.key] = atsModel
