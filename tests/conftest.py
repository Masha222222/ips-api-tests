import pytest

from api_tests.client import PumpsClient


@pytest.fixture
def pumps_client():
    return PumpsClient("https://ips.alexgallax-edu.ru")