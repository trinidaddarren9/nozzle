import pytest


@pytest.mark.parametrize(
    "input_year", [("2001a"), ("qwert"), ("2021#$"), ("a2002"),]
)
def test_incorrect_type(client, input_year):
    response = client.get(f"/api/v1/sellers/{input_year}/top")
    assert response.status_code == 404


@pytest.mark.parametrize(
    "input_year", [(2001), (2002), (2023), (2024),]
)
def test_no_data(client, input_year):
    response = client.get(f"/api/v1/sellers/{input_year}/top")
    assert response.json == {'status': 'error', 'message': 'No data found.'}


@pytest.mark.parametrize(
    "input_year", [(100), (300), (3000), (4000),]
)
def test_out_of_range(client, input_year):
    response = client.get(f"/api/v1/sellers/{input_year}/top")
    assert response.json == {
        'field': 'year', 'message': 'Value error, year must be in range of 1900 - 2999', 'type': 'value_error'}


@pytest.mark.parametrize(
    "input_year, output_sales_rep, output_sales", [
        (2009, "Steve Johnson", 164.34), (2010, "Jane Peacock", 221.92), (2012, "Margaret Park", 197.2), (2013, "Margaret Park", 168.3)]
)
def test_with_data(client, input_year, output_sales_rep, output_sales):
    response = client.get(f"/api/v1/sellers/{input_year}/top")
    data = response.json
    assert data["Sales Rep"] == output_sales_rep
    assert data["Total Sales"] == output_sales
