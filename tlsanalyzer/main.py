import logging
import json

from tlsanalyzer.collector import Collector
from tlsanalyzer.analyzer import Analyzer


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s [%(module)s] %(message)s', datefmt='%H:%M:%S')
    logging.info('Starting up...')
    work_dir = "/Users/ilja/Desktop/tls-analyzer-work-dir/"

    collector = Collector(work_dir)
    try:
        apps = collector.collect()
    except FileNotFoundError:
        return

    insecure_apps = []
    for app in apps:
        analyzer = Analyzer(work_dir, app)
        if analyzer.ats_exceptions():
            insecure_apps.append(analyzer.info_plist_results)

    logging.info('')
    logging.info('--- Analysis complete ---')
    logging.info(f'{len(insecure_apps)} / {len(apps)} apps have ATS exceptions')

    results = open('results.json', 'w')
    # magic happens here to make it pretty-printed
    results.write(json.dumps(insecure_apps))
    results.close()

