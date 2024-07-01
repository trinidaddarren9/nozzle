import os

from flask import Flask
from main.models import db
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
        os.path.join(basedir, 'data.db')
    db.init_app(app)

    with app.app_context():
        db.create_all()

        from main.sellers import bp_seller
        app.register_blueprint(bp_seller)

    return app


app = create_app()
