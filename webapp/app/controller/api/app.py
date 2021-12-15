from flask import jsonify

from webapp.app.models import IosApp, Domain, Url, AppAtsExceptions


class AppController:

    def __init__(self, app, db):
        self.app = app
        self.db = db

    def index(self):
        apps = IosApp.query.all()
        return jsonify(IosApp.serialize_list(apps))

    def show(self, id):
        app = IosApp.query.filter_by(id=id).first()
        domains = app.domains
        urls = app.urls
        ats_exceptions = app.ats_exceptions

        return jsonify({
            'app': IosApp.serialize(app),
            'domains': Domain.serialize_list(domains),
            'urls': Url.serialize_list(urls),
            'ats_exceptions': AppAtsExceptions.serialize_list(ats_exceptions),
        })
