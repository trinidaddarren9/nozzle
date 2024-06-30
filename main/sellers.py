from flask_restx import Namespace, Resource

ns_sellers = Namespace(
    "api/v1/sellers", description="Contains routes for all seller related data.")
