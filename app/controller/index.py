from flask import render_template


class IndexController:

    def __init__(self, app):
        self.app = app

    def index(self):
        return render_template('apps-list.html')
