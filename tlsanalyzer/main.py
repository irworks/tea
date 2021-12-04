import logging
import os

from argparse import ArgumentParser

from tlsanalyzer.app import App


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-v',
        '--verbosity',
        help='Set verbosity level (default: %(default)s)',
        choices=['INFO', 'WARNING', 'DEBUG'],
        default='INFO',
    )

    parser.add_argument(
        '-w',
        '--work-dir',
        help='Set the working directory containing your .ipa files.',
        type=dir_path,
        required=True
    )

    parser.add_argument(
        '-i',
        '--ignore-url-cache',
        help='Re-analyze all apps for containing urls.',
        nargs='?',
        const=True,
        type=bool,
        default=False
    )

    parser.add_argument(
        '-o',
        '--output',
        help='Set the output file.',
        default='results.json'
    )

    args = parser.parse_args()
    level = logging.getLevelName(args.verbosity)

    logging.basicConfig(level=level, format='%(asctime)s %(levelname)s [%(module)s] %(message)s', datefmt='%H:%M:%S')
    logging.info('Starting up...')

    app = App(work_dir=args.work_dir, output_file=args.output, rescan_urls=args.ignore_url_cache)
    app.run()


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
