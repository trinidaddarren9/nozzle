from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from main.sellers import ns_sellers

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///data.db'

    # API
    api = Api(app)
    api.add_namespace(ns_sellers)

    # db
    db.init_app(app)

    return app


app = create_app()
