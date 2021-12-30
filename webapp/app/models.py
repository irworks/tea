import logging

from webapp.app.start import db

from sqlalchemy.inspection import inspect


class Serializer(object):

    def serialize(self, include_relations=False):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l, include_relations=False):
        return [m.serialize(include_relations) for m in l]


app_urls = db.Table('app_url',
                db.Column('app_id', db.Integer, db.ForeignKey('apps.id'), primary_key=True),
                db.Column('url_id', db.Integer, db.ForeignKey('urls.id'), primary_key=True)
                )

app_domains = db.Table('app_domain',
                db.Column('app_id', db.Integer, db.ForeignKey('apps.id'), primary_key=True),
                db.Column('domain_id', db.Integer, db.ForeignKey('domains.id'), primary_key=True)
                )


class AppAtsExceptions(db.Model, Serializer):
    __tablename__ = 'app_ats_exceptions'
    app_id = db.Column(db.ForeignKey('apps.id'), primary_key=True)
    exception_id = db.Column(db.ForeignKey('ats_exceptions.id'), primary_key=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=True, primary_key=True)

    app = db.relationship("IosApp", back_populates="ats_exceptions", uselist=False)
    exception = db.relationship("AtsException", back_populates="ats_exceptions", uselist=False)
    domain = db.relationship("Domain", backref=db.backref('ats_exceptions', lazy=True), uselist=False)

    def __repr__(self):
        return '<appId-exceptionId {}-{}>'.format(self.app_id, self.exception_id)

    def serialize(self, include_relations=False):
        domain_out = None
        if self.domain_id:
            domain_out = self.domain.name

        data = {
            'exception_id': self.exception_id,
            'domain_id': self.domain_id,
            'domain': domain_out,
            'app_id': self.app_id
        }

        if include_relations:
            data['app'] = IosApp.serialize(self.app)
            data['exception'] = AtsException.serialize(self.exception)

        return data


class IosApp(db.Model, Serializer):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_hash = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    bundle_id = db.Column(db.String(128), nullable=False)
    version = db.Column(db.String(32), nullable=False)
    build = db.Column(db.String(32), nullable=False)
    sdk = db.Column(db.String(16), nullable=False)
    min_ios = db.Column(db.Float, nullable=False)
    urls = db.relationship('Url', secondary=app_urls, lazy='subquery',
        backref=db.backref('apps', lazy=True))
    domains = db.relationship('Domain', secondary=app_domains, lazy='subquery',
        backref=db.backref('apps', lazy=True))
    ats_exceptions = db.relationship('AppAtsExceptions', back_populates='app')

    def __init__(self, file_hash, name, bundle_id, version, build, sdk, min_ios):
        self.file_hash = file_hash
        self.name = name
        self.bundle_id = bundle_id
        self.version = version
        self.build = build
        self.sdk = sdk
        self.min_ios = min_ios

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self, include_relations=False):
        return {
            'id': self.id,
            'name': self.name,
            'bundle_id': self.bundle_id,
            'version': self.version,
            'build': self.build,
            'sdk': self.sdk,
            'min_ios': self.min_ios
        }


class Domain(db.Model, Serializer):
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self, include_relations=False):
        return {
            'id': self.id,
            'name': self.name
        }


class Url(db.Model, Serializer):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(128), nullable=False)

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self, include_relations=False):
        return {
            'id': self.id,
            'path': self.path
        }


class AtsException(db.Model, Serializer):
    __tablename__ = 'ats_exceptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    documentation_url = db.Column(db.String(128), nullable=True)
    # score for defining severity
    score = db.Column(db.Integer, nullable=False)

    # map int to values = ['secure', 'info', 'warning', 'insecure']
    state = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('ats_exceptions.id'), nullable=True)

    parent = db.relationship("AtsException", uselist=False)
    ats_exceptions = db.relationship('AppAtsExceptions', back_populates='exception')

    def __init__(self, key, state, score, description, documentation_url):
        self.key = key
        self.state = state
        self.score = score
        self.description = description
        self.documentation_url = documentation_url

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self, include_relations=False):
        state_values = ['secure', 'info', 'warning', 'insecure']
        state_value = 'unknown'
        try:
            state_value = state_values[self.state]
        except IndexError:
            logging.warning(f'Unknown state index: {self.state} in ats_exceptions.id = {self.id}')

        return {
            'id': self.id,
            'key': self.key,
            'state': state_value,
            'score': self.state,
            'parent_id': self.parent_id,
            'description': self.description,
            'documentation_url': self.documentation_url
        }
