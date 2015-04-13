from app import create_app
from app.db import db
from functools import wraps


class TestForm(object):
    errors = {}


def with_context(test):
    @wraps(test)
    def _wrapped_test(self):
        with self.app.app_context():
            with self.app.test_request_context():
                test(self)
    return _wrapped_test


def with_client(test):
    @wraps(test)
    def _wrapped_test(self):
        with self.app.test_client() as client:
            test(self, client)
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
