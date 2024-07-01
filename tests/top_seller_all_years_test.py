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
