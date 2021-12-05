import io
import json
import logging
import os
import re


class UrlExtractor:

    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.excluded_urls = {
            'https://buy.itunes.apple.com/verifyReceipt',
            'https://%s:%d%s%s%s',
            'http://*',
            'https://%@/%@',
            'http://%@/',
            'http://%@',
            'www.%@',
            'https://www.apple.com/appleca/0',
            'http://ocsp.apple.com/ocsp03-applerootca0.',
            'http://crl.apple.com/root.crl0',
            'http://ocsp.apple.com/ocsp03-aipca040',
            'https://github.com/facebook/facebook-ios-sdk/releases',
            'https://github.com/ashleymills/Reachability.swift',

            # Google analytics and firebase stuff
            'www.google.com',
            'www.googleapis.com',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://goo.gl/txkZbE',
            'http://goo.gl/426NGa',
            'https://goo.gl/YNbdK2',
            'http://goo.gl/9vSsPb',
            'https://goo.gl/ctyzm8.',
            'https://goo.gl/ctyzm8',
            'http://goo.gl/RfcP7r)',
            'https://google.com/dfp.',
            'http://cordova.apache.org/ns/1.0',
            'https://badad.googleplex.com/s/reportAd',

            # Facebook
            'www.facebook.com'
        }

    def find_urls(self, force=False):
        results_file_name = 'tls-analyzer-url-extraction-results.json'
        results_file = os.path.join(self.target_dir, results_file_name)
        if not force and os.path.isfile(results_file):
            file = open(results_file, 'r')
            urls = json.load(file)
            file.close()
            return urls

        try:
            url_list = []
            for file in os.listdir(self.target_dir):
                # Skip CodeResources and contents under Frameworks
                if 'CodeResources' in file or 'Frameworks' in file or '_CodeSignature' in file:
                    continue
                elif file.endswith(('.nib', '.ttf', '.svg', '.woff2', '.otf', '.jpg',
                                    '.png', '.dylib', '.mobileprovision', '.pdf', '.webp',
                                    '.pbf', '.mp3', '.mp4', '.wav', 'Assets.car', 'PkgInfo')):
                    continue
                else:
                    logging.debug(f'Checking file: {file}')
                    full_path = os.path.join(self.target_dir, file)
                    if os.path.isdir(full_path):
                        continue

                    with io.open(full_path,
                                 mode='r',
                                 encoding='utf8',
                                 errors='ignore') as flip:
                        dat = flip.read()
                # Extract URLs
                urls = self.url_n_email_extract(dat)
                url_list.extend(urls)

            # Unique URLs
            urls_list = list(set(url_list))
        except Exception as err:
            urls_list = []
            logging.warning(f'Failed: {err}')

        # Cache results
        results = open(results_file, 'w')
        results.write(json.dumps(urls_list))
        results.close()

        return urls_list

    def url_n_email_extract(self, dat):
        urls = []
        # URLs Extraction My Custom regex
        pattern = re.compile(
            (
                r'((?:https?://|s?ftps?://|'
                r'www\d{0,3}[.])'
                r'[\w().=/;,#:@?&~*+!$%\'{}-]+)'
            ),
            re.UNICODE)
        url_list = re.findall(pattern, dat)
        for url in url_list:
            if url not in urls \
                    and 'DTDs/PropertyList-1.0.dtd' not in url\
                    and 'w3.org' not in url\
                    and not url.endswith('/LICENSE')\
                    and url not in self.excluded_urls:
                urls.append(url)

        return urls
