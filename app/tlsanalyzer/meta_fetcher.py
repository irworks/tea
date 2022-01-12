import logging
import urllib.request, json

from app.models import IosApp


class MetaFetcher:

    def __init__(self, db):
        self.db = db

    def run(self):
        apps = IosApp.query.filter_by(genre_id=None).all()
        logging.info(f'Fetched all apps')
        for app in apps:
            self.fetch_meta(app)

    def fetch_meta(self, app):
        logging.info(f'Fetching meta from iTunes API for {app.name} ({app.bundle_id})')
        request_url = f'https://itunes.apple.com/lookup?bundleId={app.bundle_id}'
        with urllib.request.urlopen(request_url) as url:
            data = json.loads(url.read().decode())
            if not data['results']:
                logging.warning(f'Unable to find results in API response for {app.name} ({app.bundle_id})')
                return

            if len(data['results']) <= 0:
                logging.warning(f'Zero results for {app.name} ({app.bundle_id})')
                return

            app.genre_id = data['results'][0]['primaryGenreId']
            app.genre_name = data['results'][0]['primaryGenreName']
            self.db.session.add(app)

        self.db.session.commit()


