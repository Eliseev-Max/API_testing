# -*- coding: utf-8 -*-

import pytest
import requests


def test_check_status_code(verified_url, expected_status_code):
    """
    Тест сопоставляет введённый и действительный коды состояния
    HTTP/HTTPS-запроса

    """
    response = requests.get(verified_url)
    assert response.status_code == expected_status_code, "You set invalid status code"
