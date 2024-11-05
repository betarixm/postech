import pytest

from pydining.client.models import Connection


@pytest.fixture
def connection():
    return Connection(protocol="https", host="food.podac.poapper.com", port=443)
