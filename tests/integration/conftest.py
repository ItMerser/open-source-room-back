import pytest

from tests.integration.api import api


@pytest.fixture(autouse=True)
def setup(db):
    yield
    api.client.credentials()
