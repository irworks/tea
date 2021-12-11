#!/usr/bin/env python

import os

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class.
    Contains default configuration settings + configuration settings applicable to all environments.
    """
    # Default settings
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    # Settings applicable to all environments
    SECRET_KEY = os.getenv('SECRET_KEY', default='default secret key!')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'dev.sqlite3')


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'test.sqlite3')


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_DATABASE_URl', default="sqlite:///" + os.path.join(basedir, 'prod.sqlite3'))
