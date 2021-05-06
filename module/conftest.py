import pytest
import requests


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://ya.ru",
        help="input URL for request"
    )

    parser.addoption(
        "--status_code",
        type=int,
        default=200,
        choices=[200, 400, 403, 404],
        help="expected server status code after request"
    )


@pytest.fixture
def verified_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def expected_status_code(request):
    return request.config.getoption("--status_code")