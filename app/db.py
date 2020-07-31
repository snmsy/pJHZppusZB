from extensions import db
from create_app import create_app


def create():
    app = create_app()
    db.create_all(app=app)


def drop():
    app = create_app()
    db.drop_all(app=app)
