"""
This contains the application factory for creating flask application instances.
Using the application factory allows for the creation of flask applications configured
for different environments based on the value of the CONFIG_TYPE environment variable
"""

import os
from flask import Flask, render_template

# Flask extension objects instantiation
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from webapp.app.web_router import web_routes

db = SQLAlchemy()
migrate = Migrate()


# Application Factory
def create_app():
    app = Flask(__name__)

    # Configure the flask app instance
    # CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    # app.config.from_object(CONFIG_TYPE)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Register error handlers
    # register_error_handlers(app)

    register_routes(app)

    return app


def register_routes(app):
    web_routes(app)


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_error_handlers(app):
    # 400 - Bad Request
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'), 400

    # 403 - Forbidden
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    # 404 - Page Not Found
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # 405 - Method Not Allowed
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

    # 500 - Internal Server Error
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500
