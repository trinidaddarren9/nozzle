import pytest
from urllib.parse import urlencode


@pytest.mark.parametrize(
    "input_cat,input_ord,expected_key",
    [
        # cat
        ("sales_representative","asc","category"),
        (123,"asc","category"),
        ("years","dsc","category"),
        ("sales_representative","dsc","category"),
        (123,"dsc","category"),
        ("years","dsc","category"),
        # order
        ("sales_rep","dasc","order"),
        ("year","ascd","order"),
        ("total_sales","desc","order"),
    ]
)
def test_incorrect_params(client,input_cat,input_ord,expected_key):
    url_params = urlencode({"category": input_cat, "order": input_ord})
    response = client.get(f"/api/v1/sellers/top?{url_params}")
    errors = response.json["errors"]
    assert expected_key in errors
    
    

@pytest.mark.parametrize(
    "input_cat,input_ord,expected_first,expected_last",
    [
        ("sales_rep","desc","Steve Johnson","Jane Peacock"),
        ("sales_rep","asc","Jane Peacock","Steve Johnson"),
        ("total_sales","desc",221.92,164.34),
        ("total_sales","asc",164.34,221.92),
        ("year","desc",2013,2009),
        ("year","asc",2009,2013),
    ]
)
def test_correct_data(client,input_cat,input_ord,expected_first,expected_last):
    index = {
        "sales_rep": "Sales Rep",
        "total_sales": "Total Sales",
        "year": "Year"
    }
    url_params = urlencode({"category": input_cat, "order": input_ord})
    response = client.get(f"/api/v1/sellers/top?{url_params}")
    data = response.json
    assert data[0][index[input_cat]] == expected_first
    assert data[-1][index[input_cat]] == expected_last