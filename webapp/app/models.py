from webapp.app.start import db


class IosApp(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_hash = db.Column(db.String(40), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    version = db.Column(db.String(32), nullable=False)
    build = db.Column(db.String(32), nullable=False)
    sdk = db.Column(db.String(16), nullable=False)
    min_ios = db.Column(db.Float, nullable=False)

    def __init__(self, file_hash, name, version, build, sdk, min_ios):
        self.file_hash = file_hash
        self.name = name
        self.version = version
        self.build = build
        self.sdk = sdk
        self.min_ios = min_ios

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Domain(db.Model):
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<id {}>'.format(self.id)


app_domains = db.Table('app_domain',
                db.Column('app_id', db.Integer, db.ForeignKey('apps.id'), primary_key=True),
                db.Column('domain_id', db.Integer, db.ForeignKey('domains.id'), primary_key=True)
                )


class Url(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(256), nullable=False)

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '<id {}>'.format(self.id)


app_urls = db.Table('app_url',
                db.Column('app_id', db.Integer, db.ForeignKey('apps.id'), primary_key=True),
                db.Column('url_id', db.Integer, db.ForeignKey('urls.id'), primary_key=True)
                )


class AtsException(db.Model):
    __tablename__ = 'ats_exceptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(128), nullable=False)

    # map int to values = ['secure', 'warning', 'info', 'insecure']
    state = db.Column(db.Integer, nullable=False)

    def __init__(self, key, state):
        self.path = key
        self.state = state

    def __repr__(self):
        return '<id {}>'.format(self.id)


app_exceptions = db.Table('app_ats_exceptions',
                db.Column('app_id', db.Integer, db.ForeignKey('apps.id'), primary_key=True),
                db.Column('exception_id', db.Integer, db.ForeignKey('ats_exceptions.id'), primary_key=True),
                db.Column('meta', db.VARCHAR(128), nullable=True),
                db.Column('domain_id', db.Integer, db.ForeignKey('domains.id'), nullable=True),
                )