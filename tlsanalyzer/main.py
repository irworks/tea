import logging

from tlsanalyzer.collector import Collector


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s [%(module)s] %(message)s', datefmt='%H:%M:%S')
    logging.info('Starting up...')
    collector = Collector("/Users/ilja/Desktop/tls-analyzer-work-dir/")

