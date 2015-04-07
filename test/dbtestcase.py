from app import create_app
from app.db import db
from functools import wraps


def with_context(test):
    @wraps(test)
    def _wrapped_test(self):
        with self.app.app_context():
            test(self)
    return _wrapped_test


def setUpApp(self):
    app, manager = create_app()
    app.config['TESTING'] = True
    self.app = app
    self.manager = manager


def setUpDB(self):
    with self.app.app_context():
        db.create_all()


def tearDownDB(self):
    with self.app.app_context():
        db.session.remove()
        db.drop_all()
