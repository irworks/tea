from app.controller.index import IndexController


def web_routes(app):
    @app.route('/')
    @app.route('/domains')
    @app.route('/apps')
    def index():
        controller = IndexController(app)
        return controller.index()

    @app.route('/test')
    def test():
        return "Hello Test!"