import copy
import textwrap

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from api.permissions import ERROR_MESSAGE
from tests.integration.api import api
from tests.integration.config import logger
from tests.integration.utils import generate_project_data, create_specialists


def test_projects_list():
    response = api.get_projects()
    projects_before_creation = response.data
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    create_specialists(projects=1, private_projects=1)

    response = api.get_projects()
    projects_after_creation = response.data
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    diff = len(projects_after_creation) - len(projects_before_creation)

    assert diff == 1, logger.error(textwrap.dedent(f"""
        Difference of projects after creation should be 1, but equal {diff}
    """))


def test_retrieve_project():
    created_specialist = create_specialists(projects=1)[0]
    created_project_id = created_specialist['own_projects'][0]['id']
    created_project = api.get_project(id=created_project_id).data

    response = api.get_project(id=created_project_id)
    retrieved_project = response.data
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    assert created_project == retrieved_project, logger.error(textwrap.dedent(f"""
        Project data with id {created_project_id} after retrieve should be {created_project}, but
        equal {retrieved_project}
    """))


def test_retrieve_non_existent_project():
    response = api.get_project(id=0)
    response_code = response.status_code

    assert response_code == HTTP_404_NOT_FOUND, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_404_NOT_FOUND}, but equal {response_code}
    """))


def test_create_project():
    created_specialist = create_specialists()[0]
    data = generate_project_data()
    response = api.create_project(data=data, token=created_specialist['token'])
    created_project = response.data
    response_code = response.status_code

    assert response_code == HTTP_201_CREATED, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_201_CREATED}, but equal {response_code}
    """))

    data.pop('is_private')

    for field, value in data.items():
        assert created_project[field] == value, logger.error(textwrap.dedent(f"""
            Field {field} after creation specialist should be {value},
            but equal {created_project[field]}
        """))


def test_create_project_with_wrong_params():
    created_specialist = create_specialists()[0]
    response = api.create_project(data={}, token=created_specialist['token'])
    created_project = response.data
    response_code = response.status_code

    assert response_code == HTTP_400_BAD_REQUEST, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_400_BAD_REQUEST}, but equal {response_code}
    """))

    required_fields_for_creation = ('name', 'github_name', 'type',)
    absent_fields = tuple(created_project.keys())

    assert required_fields_for_creation == absent_fields, logger.error(textwrap.dedent(f"""
        Required fields {required_fields_for_creation} doesn't equal absent fields {absent_fields}
    """))


def test_create_project_with_same_name():
    specialist = create_specialists()[0]
    auth_token = specialist['token']
    projects_data = [generate_project_data(name='pytest') for _ in range(2)]
    api.create_project(data=projects_data[0], token=auth_token)
    response = api.create_project(data=projects_data[1], token=auth_token)
    response_code = response.status_code

    assert response_code == HTTP_400_BAD_REQUEST, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_400_BAD_REQUEST}, but equal {response_code}
    """))

    assert response.data.get('name'), logger.error(textwrap.dedent("""
        After creation second specialist with same name, we should get validation error with key 
        name, but it's absent
    """))


def test_update_project():
    created_specialist = create_specialists(projects=1)[0]
    project_id = created_specialist['own_projects'][0]['id']
    data = generate_project_data()
    response = api.update_project(
        id=project_id,
        data=data,
        token=created_specialist['token']
    )
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    updated_project = api.get_project(id=project_id).data
    data.pop('is_private')

    for field, value in data.items():
        assert updated_project[field] == value, logger.error(textwrap.dedent(f"""
            Field {field} after updating data should be {value}, but equal {updated_project[field]}
        """))


def test_delete_project():
    created_specialist = create_specialists(projects=1)[0]
    project_id = created_specialist['own_projects'][0]['id']
    response_after_deletion = api.delete_project(
        id=project_id,
        token=created_specialist['token']
    )
    response_code = response_after_deletion.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    response = api.get_specialist(id=created_specialist['id'])
    specialist_projects_after_deleting = response.data['own_projects']

    assert not specialist_projects_after_deleting, logger.error(textwrap.dedent(f"""
        Specialist project with id {project_id} after deleting still exists
    """))


def test_add_languages_to_project():
    created_specialist = create_specialists(projects=1)[0]
    project_id = created_specialist['own_projects'][0]['id']
    languages_for_adding = api.get_languages().data
    expected_new_languages = copy.copy(languages_for_adding)

    languages_for_adding.extend(['lang_without_bugs', 'python4', 'c--', languages_for_adding[0]])
    response_after_adding = api.add_languages_to_project(
        id=project_id,
        data={'languages': languages_for_adding},
        token=created_specialist['token']
    )
    response_code = response_after_adding.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    languages_after_adding = api.get_project(id=project_id).data['languages']

    assert languages_after_adding == expected_new_languages, logger.error(textwrap.dedent(f"""
        Specialist languages after adding should be {expected_new_languages}, but equal 
        {languages_after_adding}
    """))


def test_remove_project_languages():
    created_specialist = create_specialists(projects=1)[0]
    project_id = created_specialist['own_projects'][0]['id']
    auth_token = created_specialist['token']
    languages_for_adding = api.get_languages().data
    api.add_languages_to_project(
        id=project_id,
        data={'languages': languages_for_adding},
        token=auth_token
    )

    expected_languages_after_removing = languages_for_adding[:3]
    languages_for_removing = copy.copy(languages_for_adding[3:])
    languages_for_removing.extend(['lang_without_bugs', 'python4', 'c--'])

    response = api.remove_project_languages(
        id=project_id,
        data={'languages': languages_for_removing},
        token=auth_token
    )
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    languages_after_removing = api.get_project(id=project_id).data['languages']

    assert languages_after_removing == expected_languages_after_removing, \
        logger.error(textwrap.dedent(f"""
            Remaining languages after removing should be {expected_languages_after_removing}, but 
            remain {languages_after_removing}     
        """))


def test_add_technologies_to_project():
    created_specialist = create_specialists(projects=1)[0]
    project_id = created_specialist['own_projects'][0]['id']
    technologies = api.get_technologies().data
    technologies_for_adding = [tech['name'] for tech in technologies]
    expected_technologies = copy.copy(technologies_for_adding)

    technologies_for_adding.extend(['lib', 'technology', technologies_for_adding[0]])
    response_after_adding = api.add_technologies_to_project(
        id=project_id,
        data={'technologies': technologies_for_adding},
        token=created_specialist['token']
    )
    response_code = response_after_adding.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    technologies_after_adding = api.get_project(id=project_id).data['technologies']

    assert technologies_after_adding == expected_technologies, logger.error(textwrap.dedent(f"""
        Specialist technologies after adding should be {technologies}, but equal 
        {technologies_after_adding}
    """))


def test_remove_project_technologies():
    created_specialist = create_specialists(projects=1)[0]
    project_id = created_specialist['own_projects'][0]['id']
    auth_token = created_specialist['token']
    technologies = api.get_technologies().data
    technologies_for_adding = [tech['name'] for tech in technologies]
    api.add_technologies_to_project(
        id=project_id,
        data={'technologies': technologies_for_adding},
        token=auth_token
    )

    expected_technologies_after_removing = technologies_for_adding[:3]
    technologies_for_removing = copy.copy(technologies_for_adding[3:])
    technologies_for_removing.extend(['lib', 'technology', 'type'])

    response = api.remove_project_technologies(
        id=project_id,
        data={'technologies': technologies_for_removing},
        token=auth_token
    )
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    project = api.get_project(id=project_id).data
    technologies_after_removing = project['technologies']

    assert technologies_after_removing == expected_technologies_after_removing, \
        logger.error(textwrap.dedent(f"""
            Remaining technologies after removing should be {expected_technologies_after_removing}, 
            but remain {technologies_after_removing}     
        """))


def test_take_part():
    created_specialist = create_specialists(projects=1)[0]
    project_id = created_specialist['own_projects'][0]['id']
    specialist_id = created_specialist['id']
    response = api.take_part(id=project_id, token=created_specialist['token'])
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    specialist_after_participating = api.get_specialist(id=created_specialist['id']).data

    new_current_project_id = specialist_after_participating['current_project'].get('id')

    assert new_current_project_id == project_id, logger.error(textwrap.dedent(f"""
        After participating specialist current project id should be {project_id}, 
        but equal {new_current_project_id}  
    """))

    specialist_projects_ids = [project['id'] for project in
                               specialist_after_participating['projects']]

    assert specialist_projects_ids == [project_id], logger.error(textwrap.dedent(f"""
        After participating specialist projects ids should be {[project_id]}, 
        but equal {specialist_projects_ids}
    """))

    project_after_participating = api.get_project(id=new_current_project_id).data

    members_ids = [member['id'] for member in project_after_participating['team']]

    assert specialist_id in members_ids, logger.error(textwrap.dedent(f"""
        After participating project with id {project_id} should have new teammate 
        with id {specialist_id}, but he is absent
    """))


def test_take_part_not_own_project():
    specialist_1, specialist_2 = create_specialists(count=2, projects=1)
    project_id = specialist_2['own_projects'][0]['id']
    response = api.take_part(id=project_id, token=specialist_1['token'])
    response_code = response.status_code

    assert response_code == HTTP_403_FORBIDDEN, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_403_FORBIDDEN}, but equal {response_code}
    """))

    error_message = response.data['detail']

    assert error_message == ERROR_MESSAGE.IS_PROJECT_OWNER, logger.error(textwrap.dedent(f"""
        Error message after status code 403 should be {ERROR_MESSAGE.IS_PROJECT_OWNER}, 
        but equal {error_message}
    """))
