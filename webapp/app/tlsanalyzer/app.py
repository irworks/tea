import json
import logging
import time

from webapp.app.models import Url, Domain
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
        self.add_urls_to_dict(Url.query.all())
        self.add_domains_to_dict(Domain.query.all())

        for app in apps:
            analyzer = Analyzer(self.work_dir, app, self.rescan_urls, num, total_count,
                                self.db, self.all_urls_dict, self.all_domains_dict)
            num += 1
            if analyzer.ats_exceptions():
                results = analyzer.info_plist_results
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
        logging.info(f'Results: {self.output_file}')

        results = open(self.output_file, 'w')
        # magic happens here to make it pretty-printed
        results.write(json.dumps(insecure_apps))
        results.close()

    def add_urls_to_dict(self, models):
        for urlModel in models:
            self.all_urls_dict[urlModel.path] = urlModel

    def add_domains_to_dict(self, models):
        for domainModel in models:
            self.all_domains_dict[domainModel.name] = domainModel
