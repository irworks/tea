import json
import logging
import time

from webapp.app.tlsanalyzer.analyzer import Analyzer
from webapp.app.tlsanalyzer.collector import Collector


class App:

    def __init__(self, work_dir, output_file, rescan_urls, db):
        self.work_dir = work_dir
        self.output_file = output_file
        self.rescan_urls = rescan_urls
        self.db = db

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
        for app in apps:
            analyzer = Analyzer(self.work_dir, app, self.rescan_urls, num, total_count, self.db)
            num += 1
            if analyzer.ats_exceptions():
                results = analyzer.info_plist_results
                insecure_apps.append(results)

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
