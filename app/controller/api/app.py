import logging
import time

from flask import jsonify

from app.models import IosApp, Domain, Url, AppAtsExceptions, AtsException


class AppController:

    def __init__(self, app, db):
        self.app = app
        self.db = db

    def index(self):
        start_time = time.time()
        logging.warning(f'Starting index call: {start_time}')
        # select all apps and their corresponding count of ats exceptions
        ats_label = self.db.func.count(AppAtsExceptions.app_id).label('ats')
        score_label = self.db.func.sum(AtsException.score).label('ats_score')
        apps = self.db.session.query(IosApp, ats_label, score_label). \
            outerjoin(AppAtsExceptions, AppAtsExceptions.app_id == IosApp.id). \
            outerjoin(AtsException, AtsException.id == AppAtsExceptions.exception_id). \
            group_by(IosApp.id).all()

        duration = time.time() - start_time
        logging.warning(f'Fetched all data, took: {duration}')

        # build result models by appending the ats counts
        result = {
            'ats_apps_count': 0,
            'apps': []
        }
        logging.warning(f'Building results...')

        for app, ats_count, score in apps:
            app_dict = IosApp.serialize(app)
            if ats_count > 0:
                result['ats_apps_count'] += 1

            app_dict['ats'] = ats_count
            app_dict['score'] = score or 0
            result['apps'].append(app_dict)

        duration = time.time() - start_time
        logging.warning(f'Devlivering, took: {duration}')
        return jsonify(result)

    '''
    Return an app model and all related domains, urls and detected ats exceptions. 
    '''
    def show(self, app_id):
        app = IosApp.query.filter_by(id=app_id).first()
        domains = app.domains
        urls = app.urls
        ats_exceptions = app.ats_exceptions

        return jsonify({
            'app': IosApp.serialize(app),
            'domains': Domain.serialize_list(domains),
            'urls': Url.serialize_list(urls),
            'ats_exceptions': AppAtsExceptions.serialize_list(ats_exceptions),
        })
