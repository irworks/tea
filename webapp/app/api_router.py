from webapp.app.controller.api.app import AppController
from webapp.app.controller.api.ats_exceptions import AtsExceptionsController
from webapp.app.controller.api.domain import DomainController


def api_routes(app, db):
    @app.route('/api')
    def main():
        return "Hello from the api!"

    @app.route('/api/apps')
    def apps_index():
        controller = AppController(app, db)
        return controller.index()

    @app.route('/api/apps/<app_id>')
    def apps_details(app_id=0):
        controller = AppController(app, db)
        return controller.show(app_id)

    @app.route('/api/domains/cross')
    def domains_cross():
        controller = DomainController(app, db)
        return controller.cross_domains()

    @app.route('/api/exceptions/ats')
    def ats_exceptions_index():
        controller = AtsExceptionsController(app, db)
        return controller.index()
