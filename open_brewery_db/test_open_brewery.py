# -*- coding: utf-8 -*-

import pytest
import requests
from jsonschema import validate


url_parts = ["", "/8094", "/search?query=Brewing",
             "/autocomplete?query=dog"]


@pytest.mark.parametrize("params", url_parts)
def test_status_code(base_url, params):
    """Проверка кода состояния HTTP"""
    target = base_url + params
    response = requests.get(target)
    assert response.status_code == 200


def test_api_json_schema(base_url):
    """Проверка схемы JSON для id = 9180"""
    resp = requests.get(base_url + "/9180")

    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "obdb_id": {"type": "string"},
            "name": {"type": "string"},
            "brewery_type": {"type": "string"},
            "street": {"type": "string"},
            "address_2": {"type": "null"},
            "address_3": {"type": "null"},
            "city": {"type": "string"},
            "state": {"type": "string"},
            "country_province": {"type": "null"},
            "postal_code": {"type": "string"},
            "country": {"type": "string"},
            "longitude": {"type": "string"},
            "latitude": {"type": "string"},
            "phone": {"type": "null"},
            "website_url": {"type": "null"},
            "updated_at": {"type": "string"},
            "created_at": {"type": "string"}
        },
        "required": ["id", "obdb_id", "name", "brewery_type",
                     "city", "state", "country", "updated_at", "created_at"]
    }

    validate(instance=resp.json(), schema=schema)


# Типы пивоварен, передаваемые в качестве параметра в GET-запросе
types = ['micro', 'nano', 'regional', 'brewpub', 'large',
         'planting', 'bar', 'contract', 'proprietor', 'closed']


@pytest.mark.parametrize("brewery_type", types)
def test_sorting_by_type(base_url, brewery_type):
    """Проверка фильтра по значению параметра brewery_type"""
    target = base_url + f"?by_type={types}"
    resp = requests.get(target)
    for brewery in resp.json():
        assert brewery["brewery_type"] == types


def test_country_is_USA(base_url):
    """Проверяем, что страной является United States"""

    resp = requests.get(base_url)
    for brewery in resp.json():
        assert brewery["country"] == "United States"


@pytest.mark.skip
@pytest.mark.parametrize("amount",range(1, 50))
def test_parameter_per_page(base_url, amount):
    """Позитивный тест параметра per_page"""

    target = base_url + f"?per_page={amount}"
    resp = requests.get(target)
    assert len(resp.json()) == amount, "Количество пивоварен на странице "\
        "не соответствует переданному в GET-запросе параметру"


def test_border_conditions_per_page(base_url):
    """Проверка граничных условий параметра per_page"""

    res_1 = requests.get(base_url + "?per_page=0")
    res_2 = requests.get(base_url + "?per_page=51")

    assert res_1.json() == []
    assert len(res_2.json()) == 50, "Max per_page is not 50!"