"""
This contains the application factory for creating flask application instances.
Using the application factory allows for the creation of flask applications configured
for different environments based on the value of the CONFIG_TYPE environment variable
"""
import logging
import os

import click
from flask import Flask, render_template

# Flask extension objects instantiation
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

from app.models import *
from app.tlsanalyzer.app import App
from app.tlsanalyzer.meta_fetcher import MetaFetcher

from app.web_router import web_routes
from app.api_router import api_routes


# Application Factory
def create_app():
    app = Flask(__name__)

    # Configure the flask app instance
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Register error handlers
    # register_error_handlers(app)

    register_routes(app)

    register_cli_commands(app)

    return app


def register_cli_commands(app):
    @app.cli.command("analyze")
    @click.option("-w", "--work-dir", required=True, type=dir_path)
    @click.option("-v", "--verbosity", default='INFO')
    def analyze(work_dir, verbosity):
        log_options = ['INFO', 'WARNING', 'DEBUG']
        if verbosity not in log_options:
            return False
        print(f'Starting analyzer in {work_dir} with log level = {verbosity}!')
        level = logging.getLevelName(verbosity)
        logging.basicConfig(level=level, format='%(asctime)s %(levelname)s [%(module)s] %(message)s',
                            datefmt='%H:%M:%S')
        logging.info('Starting up...')

        tls_app = App(work_dir=work_dir, output_file="results.json", rescan_urls=False, db=db)
        tls_app.run()

        meta_fetcher = MetaFetcher(db=db)
        meta_fetcher.run()

    @app.cli.command("fetch-meta")
    def fetch_apps_meta():
        logging.basicConfig(level='INFO', format='%(asctime)s %(levelname)s [%(module)s] %(message)s',
                            datefmt='%H:%M:%S')
        meta_fetcher = MetaFetcher(db=db)
        meta_fetcher.run()


def register_routes(app):
    web_routes(app)
    api_routes(app, db)


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all(app=app)


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


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

