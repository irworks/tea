from app.controller.index import IndexController


def web_routes(app):
    @app.route('/')
    @app.route('/domains')
    @app.route('/apps')
    @app.route('/ats')
    def index():
        controller = IndexController(app)
        return controller.index()