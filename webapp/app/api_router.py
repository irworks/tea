from webapp.app.controller.api.app import AppController


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
