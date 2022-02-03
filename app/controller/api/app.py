from flask import jsonify

from app.models import IosApp, Domain, Url, AppAtsExceptions


class AppController:

    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.ignored_domains = ['localhost', '127.0.0.1']
        self.ignored_domains_string = str(self.ignored_domains)[1:-1]

    def index(self):
        # select all apps and their corresponding count of ats exceptions
        """
        Funny enough the naive approach of building the query using the ORM system
        it takes forever (300 rows in ~3 seconds). Running the raw query takes around 0.09 seconds.

        ats_label = self.db.func.count(AppAtsExceptions.app_id).label('ats')
        score_label = self.db.func.sum(AtsException.score).label('ats_score')

        apps = self.db.session.query(IosApp, ats_label, score_label). \
            outerjoin(AppAtsExceptions, AppAtsExceptions.app_id == IosApp.id). \
            outerjoin(AtsException, AtsException.id == AppAtsExceptions.exception_id). \
            group_by(IosApp.id)
        """

        query = "SELECT apps.id AS id, apps.name AS name, apps.genre_name AS genre_name," \
                " apps.bundle_id AS bundle_id, apps.version AS version, apps.build AS build," \
                " apps.sdk AS sdk, apps.min_ios AS min_ios," \
                " count(app_ats_exceptions.app_id) AS ats," \
                " sum(ats_exceptions.score) AS score" \
                " FROM apps" \
                " LEFT OUTER JOIN app_ats_exceptions ON app_ats_exceptions.app_id = apps.id" \
                " LEFT OUTER JOIN ats_exceptions ON ats_exceptions.id = app_ats_exceptions.exception_id" \
                " LEFT OUTER JOIN domains ON domains.id = app_ats_exceptions.domain_id" \
                f" WHERE app_ats_exceptions.domain_id IS NULL OR domains.name NOT IN ({self.ignored_domains_string})" \
                " GROUP BY apps.id"

        rows = self.db.engine.execute(query)
        # convert to a RowMapping
        results_as_dict = rows.mappings().all()

        # build result models by appending the ats counts
        result = {
            'ats_apps_count': 0,
            'apps': []
        }

        for app in results_as_dict:
            if app['ats'] > 0:
                result['ats_apps_count'] += 1

            # convert RowMapping to an actual python dict
            app = dict(app)
            app['score'] = app['score'] or 0
            result['apps'].append(app)

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
