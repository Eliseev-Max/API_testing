# -*- coding: utf-8 -*-

import pytest
import requests
import cerberus
from jsonschema import validate


pages = ["breeds/list/all", "breeds/image/random",
         "breed/hound/list", "breed/hound/images"]


def test_status_code(base_url):
    """Проверка кода состояния HTTP"""
    response = requests.get(base_url)
    assert response.status_code == 200


@pytest.mark.parametrize("url_parts", pages)
def test_json_status(base_url, url_parts):
    ''' Проверка значения JSON-ответа по ключу "status" '''
    target = base_url + url_parts
    assert requests.get(target).json()['status'] == 'success', "The status is not \"success\""


def test_api_image_random_json_schema(base_url):
    """Проверка схемы JSON для
    https://dog.ceo/api/breeds/image/random"""
    res = requests.get(base_url + "breeds/image/random")
    schema = {
        "message": {"type": "string"},
        "status": {"type": "string"}
    }
    v = cerberus.Validator()
    assert v.validate(res.json(), schema), "Schema does not match the pattern"


def test_api_breed_hound_list_json_schema(base_url):
    ''' Проверка схемы JSON для
    https://dog.ceo/api/breed/hound/list '''
    resp = requests.get(base_url + "breed/hound/list")

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "array"},
            "status": {"type": "string"}
        },
        "required": ["message", "status"]
    }

    validate(instance=resp.json(), schema=schema)
