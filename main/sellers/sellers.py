from flask_restx import Namespace, Resource
from main.models import Employee, Customer, Invoice

from main import db

ns_sellers = Namespace(
    "sellers", description="Contains routes for all seller related data.")


@ns_sellers.route("/<int:year>/top")
class TopSeller(Resource):
    def get(self, year: int):

        query_result = db.session.query(
            Employee,
            db.func.sum(Invoice.Total).label("total_sales")
        ) \
            .join(Customer, Employee.EmployeeId == Customer.SupportRepId) \
            .join(Invoice, Customer.SupportRepId == Invoice.CustomerId) \
            .filter(db.extract('year', Invoice.InvoiceDate) == year) \
            .group_by(Employee.EmployeeId) \
            .order_by(db.func.sum(Invoice.Total).desc()) \
            .first()
        return {
            "Sales Rep": f'{query_result[0].__getattribute__("FirstName")} {query_result[0].__getattribute__("LastName") }',
            "Total Sales": float(query_result[1])
        }
