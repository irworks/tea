import json
import logging
import time

from app.models import Url, Domain, AtsException
from app.tlsanalyzer.analyzer import Analyzer
from app.tlsanalyzer.collector import Collector


class App:

    def __init__(self, work_dir, output_file, rescan_urls, db, cleanup):
        self.work_dir = work_dir
        self.output_file = output_file
        self.rescan_urls = rescan_urls
        self.db = db
        self.cleanup = cleanup

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
        # self.db.session.query(AppAtsExceptions).delete()
        # self.db.session.commit()

        ats_exceptions = 0
        for app in apps:
            analyzer = Analyzer(self.work_dir, app, self.rescan_urls, num, total_count, self.db, self.cleanup,
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
            {'key': 'NSExceptionDomains', 'state': 1, 'score': 0, 'parent': None, 'description': 'Custom App Transport Security configurations for named domains.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/nsexceptiondomains/'},
            {'key': 'NSPinnedDomains', 'state': 0, 'score': 0, 'parent': None, 'description': 'A collection of certificates that App Transport Security enforces when connecting to named domains.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/nspinneddomains/'},
            {'key': 'NSExceptionMinimumTLSVersion-TLSv1.3', 'state': 0, 'score': 0, 'parent': 'NSExceptionDomains', 'description': 'The minimum TLS version is set to 1.3. This is considered secure since enforcing TLS 1.3 is more strict than the default (1.2).', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsexceptionminimumtlsversion/'},
            {'key': 'NSRequiresCertificateTransparency', 'state': 0, 'score': 0, 'parent': 'NSExceptionDomains', 'description': 'Certificate Transparency (CT) is a protocol that ATS can use to identify mistakenly or maliciously issued X.509 certificates. Set the value for the NSRequiresCertificateTransparency key to YES to require that for a given domain, server certificates are supported by valid, signed CT timestamps from at least two CT logs trusted by Apple. This key is optional. The default value is NO.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsrequirescertificatetransparency/'},
            {'key': 'NSExceptionMinimumTLSVersion-TLSv1.2', 'state': 2, 'score': 10, 'parent': 'NSExceptionDomains', 'description': 'The minimum TLS version is set to 1.2. This version is vulnerable to attacks such as POODLE, FREAK or CurveSwap etc. As of right now (December 2021) this is the default.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsexceptionminimumtlsversion/'},
            {'key': 'NSAllowsArbitraryLoads', 'state': 3, 'score': 500, 'parent': None, 'description': 'App Transport Security restrictions are disabled for all network connections. Disabling ATS means that unsecured HTTP connections are allowed. HTTPS connections are also allowed, and are still subject to default server trust evaluation. However, extended security checks like requiring a minimum Transport Layer Security (TLS) protocol version are disabled. This setting is not applicable to domains listed in NSExceptionDomains.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/nsallowsarbitraryloads/'},
            {'key': 'NSAllowsArbitraryLoadsInWebContent', 'state': 3, 'score': 30, 'parent': None, 'description': 'App Transport Security restrictions are disabled for requests made from WebViews without affecting URLSession connections. This setting is not applicable to domains listed in NSExceptionDomains.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/nsallowsarbitraryloadsinwebcontent/'},
            {'key': 'NSAllowsArbitraryLoadsForMedia', 'state': 3, 'score': 60, 'parent': None, 'description': 'App Transport Security restrictions are disabled for media loaded using the AVFoundation framework, without affecting URLSession connections.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/NSAllowsArbitraryLoadsForMedia/'},
            {'key': 'NSAllowsLocalNetworking', 'state': 3, 'score': 50, 'parent': None, 'description': 'ATS restrictions are disabled for requests made from local networking without affecting your URLSession connections. This setting is not applicable to domains listed in NSExceptionDomains.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/nsallowslocalnetworking/'},
            {'key': 'NSExceptionAllowsInsecureHTTPLoads', 'state': 3, 'score': 150, 'parent': 'NSExceptionDomains', 'description': 'Insecure communication to the specified domain is allowed.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsexceptionallowsinsecurehttploads'},
            {'key': 'NSIncludesSubdomains', 'state': 3, 'score': 30, 'parent': 'NSExceptionDomains', 'description': 'NSIncludesSubdomains applies the ATS exceptions for the given domain to all subdomains as well.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsincludessubdomains/'},
            {'key': 'NSExceptionMinimumTLSVersion-TLSv1.0', 'state': 3, 'score': 100, 'parent': 'NSExceptionDomains', 'description': 'The minimum TLS version is set to 1.0. This version is vulnerable to attacks such as POODLE, FREAK or CurveSwap etc. As of right now (December 2021) this is the default.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsexceptionminimumtlsversion/'},
            {'key': 'NSExceptionMinimumTLSVersion-TLSv1.1', 'state': 3, 'score': 80, 'parent': 'NSExceptionDomains', 'description': 'The minimum TLS version is set to 1.1. This version is vulnerable to multiple attacks and considered insecure.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsexceptionminimumtlsversion/'},
            {'key': 'NSExceptionRequiresForwardSecrecy', 'state': 3, 'score': 70, 'parent': 'NSExceptionDomains', 'description': 'NSExceptionRequiresForwardSecrecy limits the accepted ciphers to those that support perfect forward secrecy (PFS) through the Elliptic Curve Diffie-Hellman Ephemeral (ECDHE) key exchange. Set the value for this key to NO to override the requirement that a server must support PFS for the given domain. This key is optional. The default value is YES, which limits the accepted ciphers to those that support PFS through Elliptic Curve Diffie-Hellman Ephemeral (ECDHE) key exchange.', 'documentation_url': 'https://developer.apple.com/documentation/bundleresources/information_property_list/nsexceptionrequiresforwardsecrecy/'},
        ]

        models = {}
        for ats_exception in ats_exceptions:
            key = ats_exception['key']
            model = AtsException.query.filter_by(key=key).first()
            if model is None:
                model = AtsException(key, ats_exception['state'], ats_exception['score'],
                                     ats_exception['description'], ats_exception['documentation_url'])

                # check if there is a parent defined, if so - connect them
                parent = ats_exception['parent']
                if parent:
                    # TODO: Maybe fix by using .parent = models[parent] - currently wrong id is saved
                    # TODO: needs fix in models.py
                    model.parent_id = models[parent].id

            self.db.session.add(model)
            models[model.key] = model

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
