def web_routes(app):
    @app.route('/')
    def hello():
        return "Hello World!"

    @app.route('/test')
    def test():
        return "Hello Test!"