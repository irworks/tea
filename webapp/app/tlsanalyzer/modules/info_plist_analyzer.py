from plistlib import (load)
from webapp.app.tlsanalyzer.modules.ats.ats_plist_analyzer import (
    check_transport_security
)


class InfoPlistAnalyzer:

    def __init__(self, info_plist_file):
        self.info_plist_file = info_plist_file

    def analyze(self):
        plist_info = {
            'name': '',
            'binary': '',
            'bundle_identifier': '',
            'version': '',
            'build': '',
            'sdk': '',
            'min_os': '',
            'ats': []
        }

        with open(self.info_plist_file, 'rb') as fp:
            plist_obj = load(fp)

        plist_info['name'] = (plist_obj.get('CFBundleDisplayName', '') or plist_obj.get('CFBundleName', ''))
        plist_info['binary'] = plist_obj.get('CFBundleExecutable', '')
        plist_info['bundle_identifier'] = plist_obj.get('CFBundleIdentifier', '')
        plist_info['version'] = plist_obj.get('CFBundleShortVersionString', '')
        plist_info['build'] = plist_obj.get('CFBundleVersion', '')
        plist_info['sdk'] = plist_obj.get('DTSDKName', '')
        plist_info['min_os'] = plist_obj.get('MinimumOSVersion', '')
        plist_info['ats'] += check_transport_security(plist_obj)

        return plist_info
