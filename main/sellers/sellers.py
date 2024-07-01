from pydantic import BaseModel, field_validator, ValidationError
from flask_restx import Namespace, Resource
from main.models import Employee, Customer, Invoice

from main import db

ns_sellers = Namespace(
    "sellers", description="Contains routes for all seller related data.")


class YearValidator(BaseModel):
    year: int

    @field_validator('year')
    def check_range(cls, x):
        if not 1900 <= x <= 2999:
            raise ValueError("year must be in range of 1900 - 2999")


@ns_sellers.route("/<int:year>/top")
class TopSeller(Resource):
    def get(self, year: int):

        # validate year input
        try:
            YearValidator(year=year)
        except Exception as error:
            return error.json(), 403

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

        if query_result is None:
            return {
                "status": "error",
                "message": "No data found."
            }, 400

        return {
            "Sales Rep": f'{query_result[0].__getattribute__("FirstName")} {query_result[0].__getattribute__("LastName") }',
            "Total Sales": float(query_result[1])
        }
