from webapp.app.controller.index import IndexController


def web_routes(app):
    @app.route('/')
    def index():
        controller = IndexController(app)
        return controller.index()

    @app.route('/test')
    def test():
        return "Hello Test!"