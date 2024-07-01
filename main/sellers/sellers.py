import pandas as pd
from pydantic import BaseModel, field_validator, ValidationError, Field
from typing import Literal

from flask_restx import Namespace, Resource, reqparse
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


class TopSellerAllYearsValidator(BaseModel):
    category: Literal['sales_rep', 'total_sales', 'year']
    order: Literal['asc', 'dsc']


parser = reqparse.RequestParser()
parser.add_argument('category', type=str, required=False, choices=('sales_rep', 'total_sales',
                    'year'), help='Category must be one of: sales_rep, total_sales, year', default='sales_rep')

parser.add_argument('order', type=str, required=False, choices=(
    'asc', 'dsc'), help='Order must be one of: asc, dsc', default='asc')


def validation_errors_as_dict(errors):
    error_dict = {}
    for error in errors:
        error_dict["field"] = error['loc'][0]
        error_dict["message"] = error['msg']
        error_dict["type"] = error['type']
    return error_dict


@ns_sellers.route("/<int:year>/top")
class TopSeller(Resource):
    def get(self, year: int):

        # validate year input
        try:
            YearValidator(year=year)
        except ValidationError as error:
            return validation_errors_as_dict(error.errors()), 403

        # query data
        query_result = db.session.query(
            Employee,
            db.func.sum(Invoice.Total).label("total_sales")
        ) \
            .join(Customer, Employee.EmployeeId == Customer.SupportRepId,) \
            .join(Invoice, Customer.CustomerId == Invoice.CustomerId,) \
            .group_by(Employee.EmployeeId) \
            .filter(db.extract('year', Invoice.InvoiceDate) == year) \
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


@ns_sellers.route("/top")
class TopSellerAllYears(Resource):
    @ns_sellers.expect(parser)
    def get(self):

        # parse args
        args = parser.parse_args()
        category = args['category']
        order = args['order']

        # validate input
        try:
            TopSellerAllYearsValidator(
                category=category,
                order=order
            )
        except ValidationError as error:
            return validation_errors_as_dict(error.errors()), 403

        # query data
        query_results = db.session.query(
            Employee,
            db.func.sum(Invoice.Total).label("total_sales"),
            db.extract('year', Invoice.InvoiceDate).label("year")
        ) \
            .join(Customer, Employee.EmployeeId == Customer.SupportRepId) \
            .join(Invoice, Customer.CustomerId == Invoice.CustomerId) \
            .group_by(Employee.EmployeeId, db.extract('year', Invoice.InvoiceDate)) \
            .order_by(db.func.sum(Invoice.Total).desc()) \
            .all()

        # check if there is no data
        if len(query_results) == 0:
            return {
                "status": "error",
                "message": "No data found."
            }, 400

        data = [{
            "Sales Rep": f'{query_result[0].__getattribute__("FirstName")} {query_result[0].__getattribute__("LastName") }',
            "Total Sales": float(query_result[1]),
            "Year": int(query_result[2]),
        } for query_result in query_results]

        df = pd.DataFrame(data).groupby(["Year", "Sales Rep"]).max()

        # get the index of max sales per year
        idx = df.groupby('Year')['Total Sales'].idxmax()

        index = {
            "sales_rep": "Sales Rep",
            "total_sales": "Total Sales",
            "year": "Year"
        }

        # arrange columns and sort values base on query params
        result = df.loc[idx].reset_index()[["Sales Rep", "Total Sales", "Year"]].sort_values(
            by=index[category], ascending=True if order == "asc" else False)
        return result.to_dict(orient="records")
