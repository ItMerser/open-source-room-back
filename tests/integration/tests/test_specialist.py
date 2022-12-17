import copy
import textwrap

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from tests.integration.api import api
from tests.integration.config import logger, fake
from tests.integration.utils import (
    generate_creation_specialist_data,
    generate_updating_specialist_data,
    create_specialists,
)


def test_specialists_list():
    response = api.get_specialists()
    specialists_before_creation = response.data
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    create_specialists()
    specialists_after_creation = api.get_specialists().data
    diff = len(specialists_after_creation) - len(specialists_before_creation)

    assert diff == 1, logger.error(textwrap.dedent(f"""
        Difference of specialists after creation single note should be 1, but equal {diff}
    """))


def test_retrieve_specialist():
    created_specialist = create_specialists()[0]
    specialist_id = created_specialist['id']
    response = api.get_specialist(id=specialist_id)
    retrieved_specialist = response.data
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    created_specialist.pop('token')

    assert created_specialist == retrieved_specialist, logger.error(textwrap.dedent(f"""
        Created specialist with id {specialist_id} don't equal retrieved specialist with this id
    """))


def test_retrieve_non_existent_specialist():
    response = api.get_specialist(id=0)
    response_code = response.status_code

    assert response_code == HTTP_404_NOT_FOUND, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_404_NOT_FOUND}, but equal {response_code}
    """))


def test_create_specialist():
    data = generate_creation_specialist_data()
    response = api.create_specialist(data=data)
    created_specialist = response.data
    response_code = response.status_code

    assert response_code == HTTP_201_CREATED, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_201_CREATED}, but equal {response_code}
    """))

    data.pop('password')
    data.pop('born_date')

    for field, value in data.items():
        assert created_specialist[field] == value, logger.error(textwrap.dedent(f"""
            Field {field} after creation specialist should be {value},
            but equal {created_specialist[field]}
        """))

    assert created_specialist.get('token') is not None, logger.error(textwrap.dedent("""
        After creation, specialist must have TOKEN key, but it is absent
    """))


def test_create_specialist_with_wrong_params():
    response = api.create_specialist(data={})
    created_specialist = response.data
    response_code = response.status_code

    assert response_code == HTTP_400_BAD_REQUEST, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_400_BAD_REQUEST}, but equal {response_code}
    """))

    required_fields_for_creation = ('nickname', 'github_nickname', 'password', 'direction',)
    absent_fields = tuple(created_specialist.keys())

    assert required_fields_for_creation == absent_fields, logger.error(textwrap.dedent(f"""
        Required fields {required_fields_for_creation} doesn't equal absent fields {absent_fields}
    """))


def test_authenticate_specialist():
    creation_data = generate_creation_specialist_data()
    created_specialist = api.create_specialist(data=creation_data).data
    nickname, password = creation_data['nickname'], creation_data['password']

    authenticate_data = {'nickname': nickname, 'password': password}
    response = api.authenticate_specialist(data=authenticate_data)
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    authenticated_specialist = response.data

    assert created_specialist == authenticated_specialist, logger.error(textwrap.dedent(f"""
        Specialist data {authenticated_specialist} after authentication doesn't equal data after
        registration {created_specialist}
    """))


def test_authenticate_specialist_with_wrong_params():
    response = api.authenticate_specialist(data={
        'nickname': 'nickname',
        'password': 'secret_password'
    })
    response_code = response.status_code

    assert response_code == HTTP_400_BAD_REQUEST, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_400_BAD_REQUEST}, but equal {response_code}
    """))


def test_update_specialist():
    created_specialist = create_specialists()[0]
    data = generate_updating_specialist_data()
    response = api.update_specialist(data=data, token=created_specialist['token'])
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    specialist = api.get_specialist(id=created_specialist['id']).data
    data.pop('born_date')

    for field, value in data.items():
        assert specialist[field] == value, logger.error(textwrap.dedent(f"""
            Field {field} after updating data should be {value}, but equal {specialist[field]}
        """))


def test_change_specialist_password():
    created_specialist = create_specialists()[0]
    new_password = fake.password()
    response = api.change_specialist_password(
        data={'password': new_password},
        token=created_specialist['token']
    )
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    auth_data = {'nickname': created_specialist['nickname'], 'password': new_password}
    response_after_auth = api.authenticate_specialist(data=auth_data)
    response_code = response_after_auth.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))


def test_delete_specialist():
    created_specialist = create_specialists()[0]
    response = api.delete_specialist(token=created_specialist['token'])
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    # Remove authentication credentials, because we won't enter by deleted specialist token
    api.client._credentials = {}
    response_after_deleting = api.get_specialist(id=created_specialist['id'])
    response_code = response_after_deleting.status_code

    assert response_code == HTTP_404_NOT_FOUND, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_404_NOT_FOUND}, but equal {response_code}
    """))


def test_add_languages_to_specialist():
    created_specialist = create_specialists()[0]
    languages_for_adding = api.get_languages().data
    expected_new_languages = copy.copy(languages_for_adding)

    languages_for_adding.extend(['lang_without_bugs', 'python4', 'c--', languages_for_adding[0]])
    response_after_adding = api.add_languages_to_specialist(
        data={'languages': languages_for_adding},
        token=created_specialist['token']
    )
    response_code = response_after_adding.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    languages_after_adding = api.get_specialist(id=created_specialist['id']).data['languages']

    assert languages_after_adding == expected_new_languages, logger.error(textwrap.dedent(f"""
        Specialist languages after adding should be {expected_new_languages}, but equal 
        {languages_after_adding}
    """))


def test_remove_specialist_languages():
    created_specialist = create_specialists()[0]
    auth_token = created_specialist['token']
    languages_for_adding = api.get_languages().data
    api.add_languages_to_specialist(
        data={'languages': languages_for_adding},
        token=auth_token
    )

    expected_languages_after_removing = languages_for_adding[:3]
    languages_for_removing = copy.copy(languages_for_adding[3:])
    languages_for_removing.extend(['lang_without_bugs', 'python4', 'c--'])

    response = api.remove_specialist_languages(
        data={'languages': languages_for_removing},
        token=auth_token
    )
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    languages_after_removing = api.get_specialist(id=created_specialist['id']).data['languages']

    assert languages_after_removing == expected_languages_after_removing, \
        logger.error(textwrap.dedent(f"""
            Remaining languages after removing should be {expected_languages_after_removing}, but 
            remain {languages_after_removing}     
        """))


def test_add_technologies_to_specialist():
    created_specialist = create_specialists()[0]
    technologies = api.get_technologies().data
    technologies_for_adding = [tech['name'] for tech in technologies]
    expected_technologies = copy.copy(technologies_for_adding)

    technologies_for_adding.extend(['lib', 'technology', technologies_for_adding[0]])
    response_after_adding = api.add_technologies_to_specialist(
        data={'technologies': technologies_for_adding},
        token=created_specialist['token']
    )
    response_code = response_after_adding.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    technologies_after_adding = api.get_specialist(id=created_specialist['id']).data['technologies']

    assert technologies_after_adding == expected_technologies, logger.error(textwrap.dedent(f"""
        Specialist technologies after adding should be {technologies}, but equal 
        {technologies_after_adding}
    """))


def test_remove_specialist_technologies():
    created_specialist = create_specialists()[0]
    auth_token = created_specialist['token']
    technologies = api.get_technologies().data
    technologies_for_adding = [tech['name'] for tech in technologies]
    api.add_technologies_to_specialist(
        data={'technologies': technologies_for_adding},
        token=auth_token
    )

    expected_technologies_after_removing = technologies_for_adding[:3]
    technologies_for_removing = copy.copy(technologies_for_adding[3:])
    technologies_for_removing.extend(['lib', 'technology', 'type'])

    response = api.remove_specialist_technologies(
        data={'technologies': technologies_for_removing},
        token=auth_token
    )
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    specialist = api.get_specialist(id=created_specialist['id']).data
    technologies_after_removing = specialist['technologies']

    assert technologies_after_removing == expected_technologies_after_removing, \
        logger.error(textwrap.dedent(f"""
            Remaining technologies after removing should be {expected_technologies_after_removing}, 
            but remain {technologies_after_removing}     
        """))
