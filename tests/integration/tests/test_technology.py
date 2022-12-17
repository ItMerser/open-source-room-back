import textwrap

from rest_framework.status import HTTP_200_OK

from tests.integration.api import api
from tests.integration.config import logger


def test_languages():
    response = api.get_languages()
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))


def test_technologies():
    response = api.get_technologies()
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))
