from flask import Flask
from flask_restx import Api
from main.sellers import ns_sellers

app = Flask(__name__)
api = Api(app)
api.add_namespace(ns_sellers)
