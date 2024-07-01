import pandas as pd
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
        except ValidationError as error:
            return error.json(), 403

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
    def get(self):

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

        if query_results is None:
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
        return df.loc[idx].reset_index()[["Sales Rep", "Total Sales", "Year"]].to_dict(orient="records")
