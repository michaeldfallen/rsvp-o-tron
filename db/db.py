from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand


db = SQLAlchemy()
migrate = Migrate(db)


def init(app, manager):
    db.init_app(app)
    migrate.init_app(app, db, 'db/migrations')
    manager.add_command('db', MigrateCommand)

#    with app.app_context():
#        db.create_all()
