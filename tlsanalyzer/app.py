import json
import logging

from tlsanalyzer.analyzer import Analyzer
from tlsanalyzer.collector import Collector


class App:

    def __init__(self, work_dir, output_file, rescan_urls):
        self.work_dir = work_dir
        self.output_file = output_file
        self.rescan_urls = rescan_urls

    def run(self):
        collector = Collector(self.work_dir)
        try:
            apps = collector.collect()
        except FileNotFoundError:
            return

        insecure_apps = []
        for app in apps:
            analyzer = Analyzer(self.work_dir, app, self.rescan_urls)
            if analyzer.ats_exceptions():
                insecure_apps.append(analyzer.info_plist_results)

        logging.info('')
        logging.info('--- Analysis complete ---')
        logging.info(f'{len(insecure_apps)} / {len(apps)} apps have ATS exceptions')

        results = open(self.output_file, 'w')
        # magic happens here to make it pretty-printed
        results.write(json.dumps(insecure_apps))
        results.close()
