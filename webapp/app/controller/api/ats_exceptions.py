from flask import jsonify

from webapp.app.models import AtsException


class AtsExceptionsController:

    def __init__(self, app, db):
        self.app = app
        self.db = db

    '''
    Return domains which are used in multiple apps.  
    '''
    def index(self):
        exceptions = self.db.session.query(AtsException).all()
        return jsonify(AtsException.serialize_list(exceptions))
