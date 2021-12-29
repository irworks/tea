from flask import jsonify
from sqlalchemy import distinct

from webapp.app.controller.api.order import add_order_to_query
from webapp.app.controller.api.pagination import pagination_meta, paginate
from webapp.app.models import Domain, app_domains, IosApp, AppAtsExceptions


class DomainController:

    def __init__(self, app, db):
        self.app = app
        self.db = db

        self.apps_count = self.db.func.count(distinct(app_domains.c.app_id)).label('apps_count')
        self.ats_apps_count = self.db.func.count(distinct(AppAtsExceptions.app_id)).label('ats_apps_count')

    def build_result(self, domains):
        result = []
        for domain, apps_count, ats_exceptions_count in domains:
            app_dict = Domain.serialize(domain)

            app_dict['used_in_apps'] = apps_count
            app_dict['ats_apps_count'] = ats_exceptions_count
            result.append(app_dict)
        return result

    def index(self):
        domains = self.db.session.query(Domain, self.apps_count, self.ats_apps_count) \
            .outerjoin(app_domains) \
            .outerjoin(AppAtsExceptions) \
            .group_by(Domain.id).all()

        return jsonify({
            'domains': self.build_result(domains)
        })

    def index_paginated(self, page, options):
        query = self.db.session.query(Domain, self.apps_count, self.ats_apps_count) \
            .outerjoin(app_domains) \
            .outerjoin(AppAtsExceptions) \
            .group_by(Domain.id)

        query = add_order_to_query(query, options['order'], {
            'apps_count': self.apps_count,
            'ats_apps_count': self.ats_apps_count
        })

        domains = paginate(query, page)

        return jsonify({
            'pagination': pagination_meta(domains),
            'domains': self.build_result(domains.items)
        })

    def show(self, domain_id):
        domain = self.db.session.query(Domain).filter_by(id=domain_id).first()

        return jsonify({
            'domain': Domain.serialize(domain),
            'apps': IosApp.serialize_list(domain.apps),
            'ats_exceptions': AppAtsExceptions.serialize_list(domain.ats_exceptions),
        })

    '''
    Return domains which are used in multiple apps.  
    '''
    def cross_domains(self):
        query = 'SELECT a1.app_id, a1.domain_id, domains.name, apps.name\
          FROM app_domain a1\
          JOIN (SELECT a2.domain_id\
                  FROM app_domain a2\
              GROUP BY a2.domain_id\
                HAVING COUNT(a2.domain_id) > 1) a2 ON a2.domain_id = a1.domain_id\
          JOIN domains ON a1.domain_id = domains.id\
          JOIN apps ON a1.app_id = apps.id;'

        rows = self.db.engine.execute(query)
        result = {}

        # build an results set with domain_id => {domain_name: '', apps: []}
        for app_id, domain_id, domain_name, app_name in rows:
            if domain_id not in result:
                result[domain_id] = {
                    'domain_name': domain_name,
                    'apps': []
                }

            result[domain_id]['apps'].append({
                'app_id': app_id,
                'app_name': app_name
            })

        return jsonify(result)
