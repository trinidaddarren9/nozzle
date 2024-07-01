import os

from flask import Flask
from main.models import db
from main.sellers import bp_seller

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(database_uri: str = 'sqlite:///' +
               os.path.join(basedir, 'data.db')):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.init_app(app)

    with app.app_context():
 
        app.register_blueprint(bp_seller)

    return app
