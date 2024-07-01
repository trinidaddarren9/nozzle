from flask import Blueprint
from flask_restx import Api

from main.sellers.sellers import ns_sellers

bp_seller = Blueprint('api_sellers', __name__, url_prefix="/api/v1")
bp_api = Api(bp_seller)
bp_api.add_namespace(ns_sellers)
