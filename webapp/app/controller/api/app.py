from flask import jsonify

from webapp.app.models import IosApp, Domain, Url, AppAtsExceptions


class AppController:

    def __init__(self, app, db):
        self.app = app
        self.db = db

    def index(self):
        # select all apps and their corresponding count of ats exceptions
        ats_label = self.db.func.count(AppAtsExceptions.app_id).label('ats')
        apps = self.db.session.query(IosApp, ats_label). \
            join(AppAtsExceptions). \
            group_by(IosApp.id).all()

        # build result models by appending the ats counts
        result = []
        for app, ats_count in apps:
            app_dict = IosApp.serialize(app)

            app_dict['ats'] = ats_count
            result.append(app_dict)

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
