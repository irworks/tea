#
# Taken from the Mobile-Security-Framework-MobSF:
# https://github.com/MobSF/Mobile-Security-Framework-MobSF/blob/master/mobsf/StaticAnalyzer/views/ios/app_transport_security.py
#
def check_transport_security(p_list):
    """Check info.plist for insecure connection configurations."""
    ats = []
    if 'NSAppTransportSecurity' in p_list:
        ats_dict = p_list['NSAppTransportSecurity']
        if ats_dict and ats_dict.get('NSAllowsArbitraryLoads'):
            ats.append({
                'key': 'NSAllowsArbitraryLoads',
                'domain': None,
                'issue': ('App Transport Security '
                          'AllowsArbitraryLoads is allowed'),
                'status': 'insecure',
                'description': (
                    'App Transport Security restrictions are disabled '
                    'for all network connections. Disabling ATS means that '
                    'unsecured HTTP connections are allowed. HTTPS '
                    'connections are also allowed, and are still subject '
                    'to default server trust evaluation. However, '
                    'extended security checks like requiring a minimum '
                    'Transport Layer Security (TLS) protocol version are '
                    'disabled. This setting is not applicable to domains '
                    'listed in NSExceptionDomains.'),
            })
        if ats_dict and ats_dict.get('NSAllowsArbitraryLoadsForMedia'):
            ats.append({
                'key': 'NSAllowsArbitraryLoadsForMedia',
                'domain': None,
                'issue': 'Insecure media load is allowed',
                'status': 'insecure',
                'description': (
                    'App Transport Security restrictions are disabled for '
                    'media loaded using the AVFoundation framework, '
                    'without affecting your URLSession connections. '
                    'This setting is not applicable to domains '
                    'listed in NSExceptionDomains.'),
            })
        if ats_dict and ats_dict.get('NSAllowsArbitraryLoadsInWebContent'):
            ats.append({
                'key': 'NSAllowsArbitraryLoadsInWebContent',
                'domain': None,
                'issue': 'Insecure WebView load is allowed',
                'status': 'insecure',
                'description': (
                    'App Transport Security restrictions are disabled for '
                    'requests made from WebViews without affecting your '
                    'URLSession connections. This setting is not applicable '
                    'to domains listed in NSExceptionDomains.'),
            })
        if ats_dict and ats_dict.get('NSAllowsLocalNetworking'):
            ats.append({
                'key': 'NSAllowsLocalNetworking',
                'domain': None,
                'issue': 'Insecure local networking is allowed',
                'status': 'insecure',
                'description': (
                    'App Transport Security restrictions are disabled for '
                    'requests made from local networking '
                    'without affecting your '
                    'URLSession connections. This setting is not applicable '
                    'to domains listed in NSExceptionDomains.'),
            })

        # this is actually a good thing!
        # https://developer.apple.com/documentation/bundleresources/information_property_list/nsapptransportsecurity/nsexceptiondomains
        if ats_dict and ats_dict.get('NSPinnedDomains'):
            domains = ats_dict.get('NSPinnedDomains')
            findings = {
                'key': 'NSPinnedDomains',
                'domain': None,
                'issue': 'NSPinnedDomains is enabled',
                'status': 'secure',
                'description': (
                    'NSPinnedDomains enables certificate '
                    'pinning for configured domains. '
                    'This increases security by detecting '
                    'MITM proxys with trusted root CA certificates. '
                    'This key is available since '
                    'iOS 14.0+, iPadOS 14.0+, macOS 11.0+. '
                    'This key is optional. The default is not defined.'
                ),
                'domains': list(domains.keys()),
            }
            ats.append(findings)

        # NS Domain Exceptions
        if ats_dict and ats_dict.get('NSExceptionDomains'):
            exception_domains = ats_dict.get('NSExceptionDomains')
            ats.append({
                'key': 'NSExceptionDomains',
                'domain': None,
                'issue': 'NSExceptionDomains',
                'status': 'info',
                'description': 'Custom App Transport Security configurations for named domains.',
                'domains': list(exception_domains.keys()),
            })
            for domain, config in exception_domains.items():
                if not isinstance(config, dict):
                    continue
                old_exp = 'NSTemporaryExceptionAllowsInsecureHTTPLoads'
                old_exp2 = 'NSThirdPartyExceptionAllowsInsecureHTTPLoads'
                if (config.get('NSExceptionAllowsInsecureHTTPLoads', False)
                        or config.get(old_exp, False)
                        or config.get(old_exp2, False)):
                    findings = {
                        'key': 'NSExceptionAllowsInsecureHTTPLoads',
                        'domain': format(domain),
                        'issue': ('Insecure communication'
                                  ' to {} is allowed'.format(domain)),
                        'status': 'insecure',
                        'description': (
                            'NSExceptionAllowsInsecureHTTPLoads allows '
                            'insecure HTTP loads to {}, '
                            'or to be able to loosen the '
                            'server trust evaluation '
                            'requirements for HTTPS '
                            'connections to the domain.'.format(domain)
                        ),
                    }
                    ats.append(findings)

                if config.get('NSIncludesSubdomains', False):
                    findings = {
                        'key': 'NSIncludesSubdomains',
                        'domain': format(domain),
                        'issue': ('NSIncludesSubdomains set to TRUE'
                                  ' for {}'.format(domain)),
                        'status': 'insecure',
                        'description': (
                            'NSIncludesSubdomains applies the ATS exceptions '
                            'for the given domain to all '
                            'subdomains as well. '
                            'For example, the ATS exceptions in the '
                            'domain exception dictionary apply to {}, '
                            'as well as math.{}, history.{}, and so on. '
                            'Otherwise, if the value is NO, the exceptions '
                            'apply only to '
                            '{}.'.format(domain, domain, domain, domain)
                        ),
                    }
                    ats.append(findings)
                old_tls = 'NSTemporaryExceptionMinimumTLSVersion'
                inc_min_tls = (config.get('NSExceptionMinimumTLSVersion', None)
                               or config.get(old_tls, None))
                if inc_min_tls in ['TLSv1.0', 'TLSv1.1']:
                    findings = {
                        'key': ('NSExceptionMinimumTLSVersion-{}'.format(inc_min_tls)),
                        'domain': format(domain),
                        'issue': ('NSExceptionMinimumTLSVersion set to {}'
                                  ' on {}'.format(inc_min_tls, domain)),
                        'status': 'insecure',
                        'description': (
                            'The minimum Transport Layer '
                            'Security (TLS) version '
                            'for network connections sent to {} '
                            'is set to {}. This version is deemed '
                            'to be insecure'.format(domain, inc_min_tls)
                        ),
                    }
                    ats.append(findings)

                elif inc_min_tls == 'TLSv1.2':
                    findings = {
                        'key': ('NSExceptionMinimumTLSVersion-{}'.format(inc_min_tls)),
                        'domain': format(domain),
                        'issue': ('NSExceptionMinimumTLSVersion set to {}'
                                  ' on {}'.format(inc_min_tls, domain)),
                        'status': 'warning',
                        'description': (
                            'The minimum Transport Layer '
                            'Security (TLS) version '
                            'for network connections sent to {} '
                            'is set to {}. '
                            'This version is vulnerable to '
                            'attacks such as POODLE, FREAK, '
                            'or CurveSwap etc.'.format(domain, inc_min_tls)
                        ),
                    }
                    ats.append(findings)

                elif inc_min_tls == 'TLSv1.3':
                    findings = {
                        'key': ('NSExceptionMinimumTLSVersion-{}'.format(inc_min_tls)),
                        'domain': format(domain),
                        'issue': ('NSExceptionMinimumTLSVersion set to {}'
                                  ' on {}'.format(inc_min_tls, domain)),
                        'status': 'secure',
                        'description': (
                            'The minimum Transport Layer '
                            'Security (TLS) version '
                            'for network connections sent to {} '
                            'is set to {}.'.format(domain, inc_min_tls)
                        ),
                    }
                    ats.append(findings)

                elif inc_min_tls is None:
                    pass

                else:
                    findings = {
                        'issue': ('NSExceptionMinimumTLSVersion set to {}'
                                  ' on {}'.format(inc_min_tls, domain)),
                        'status': 'info',
                        'key': ('NSExceptionMinimumTLSVersion-{}'.format(inc_min_tls)),
                        'domain': format(domain),
                        'description': (
                            'The minimum Transport Layer '
                            'Security (TLS) version '
                            'for network connections sent to {} '
                            'is set to {}.'.format(domain, inc_min_tls)
                        ),
                    }
                    ats.append(findings)
                old_fwd = 'NSTemporaryExceptionRequiresForwardSecrecy'
                old_fwd2 = 'NSThirdPartyExceptionRequiresForwardSecrecy'
                if not (config.get('NSExceptionRequiresForwardSecrecy', False)
                        or config.get(old_fwd, False)
                        or config.get(old_fwd2, False)):
                    findings = {
                        'key': 'NSExceptionRequiresForwardSecrecy',
                        'domain': format(domain),
                        'issue': ('NSExceptionRequiresForwardSecrecy '
                                  'set to NO'
                                  ' for {}'.format(domain)),
                        'status': 'insecure',
                        'description': (
                            'NSExceptionRequiresForwardSecrecy '
                            'limits the accepted ciphers to '
                            'those that support perfect '
                            'forward secrecy (PFS) through the '
                            'Elliptic Curve Diffie-Hellman '
                            'Ephemeral (ECDHE) key exchange. '
                            'Set the value for this key to NO to override '
                            'the requirement that a server must support '
                            'PFS for the given domain. This key is optional. '
                            'The default value is YES, which limits the '
                            'accepted ciphers to those that support '
                            'PFS through Elliptic Curve Diffie-Hellman '
                            'Ephemeral (ECDHE) key exchange.'),
                    }
                    ats.append(findings)

                if config.get('NSRequiresCertificateTransparency', False):
                    findings = {
                        'key': 'NSRequiresCertificateTransparency',
                        'domain': format(domain),
                        'issue': ('NSRequiresCertificateTransparency'
                                  ' set to YES for {}'.format(domain)),
                        'status': 'secure',
                        'description': (
                            'Certificate Transparency (CT) is a protocol '
                            'that ATS can use to identify '
                            'mistakenly or maliciously '
                            'issued X.509 certificates. '
                            'Set the value for the '
                            'NSRequiresCertificateTransparency '
                            'key to YES to require that for a given domain, '
                            'server certificates are supported by valid, '
                            'signed CT timestamps from at least '
                            'two CT logs trusted by Apple. '
                            'This key is optional. The default value is NO.'),
                    }
                    ats.append(findings)

    return ats
