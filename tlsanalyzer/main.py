import logging

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

    for app in apps:
        analyzer = Analyzer(work_dir, app)

