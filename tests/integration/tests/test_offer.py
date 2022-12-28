import textwrap

from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from tests.integration.api import api
from tests.integration.config import logger
from tests.integration.utils import create_specialists


def test_add_to_team():
    sender, recipient = create_specialists(count=2, projects=1)
    sender_project_id = sender['own_projects'][0]['id']
    recipient_id = recipient['id']
    data = {'recipient_id': recipient_id, 'project_id': sender_project_id}
    response_after_creation_offer = api.add_to_team(data=data, token=sender['token'])
    response_code = response_after_creation_offer.status_code

    assert response_code == HTTP_201_CREATED, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_201_CREATED}, but equal {response_code}
    """))

    offer_id = response_after_creation_offer.data['id']
    response = api.response_to_offer(id=offer_id, data={'response': True}, token=recipient['token'])
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    recipient_after_accepted_offer = api.get_specialist(id=recipient_id).data
    recipient_current_project_id = recipient_after_accepted_offer['current_project']['id']
    recipient_projects = recipient_after_accepted_offer['projects']

    assert recipient_current_project_id == sender_project_id, logger.error(textwrap.dedent(f"""
        After accepted offer to join to project with id {sender_project_id}, recipient current
        project should be {sender_project_id}, but equal {recipient_current_project_id}
    """))

    assert len(recipient_projects) == 1, logger.error(textwrap.dedent(f"""
        After accepted offer to join to project team, recipient count projects should be 1, but
        equal {len(recipient_projects)} 
    """))

    assert recipient_projects[0]['id'] == sender_project_id, logger.error(textwrap.dedent(f"""
        After accepted offer to join to project team, recipient should contain project with id
        {sender_project_id}, but it's absent 
    """))

    project_after_add_new_teammate = api.get_project(id=sender_project_id).data
    project_team = project_after_add_new_teammate['team']

    assert len(project_team) == 1, logger.error(textwrap.dedent(f"""
        After adding new teammate with id {recipient_id} to project with id {sender_project_id},
        teammates count should be 1, but equal {len(project_team)}
    """))

    assert project_team[0]['id'] == recipient_id, logger.error(textwrap.dedent(f"""
        After adding new teammate with id {recipient_id} to project with id {sender_project_id},
        this specialist is absent in project team 
    """))


def test_join_to_team():
    sender, recipient = create_specialists(count=2, projects=1)
    recipient_project_id = recipient['own_projects'][0]['id']
    sender_id = sender['id']
    data = {'recipient_id': recipient['id'], 'project_id': recipient_project_id}
    response_after_creation_offer = api.join_to_team(data=data, token=sender['token'])
    response_code = response_after_creation_offer.status_code

    assert response_code == HTTP_201_CREATED, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_201_CREATED}, but equal {response_code}
    """))

    offer_id = response_after_creation_offer.data['id']
    response = api.response_to_offer(id=offer_id, data={'response': True}, token=recipient['token'])
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    sender_after_accepted_offer = api.get_specialist(id=sender_id).data

    sender_current_project_id = sender_after_accepted_offer['current_project']['id']
    sender_projects = sender_after_accepted_offer['projects']

    assert sender_current_project_id == recipient_project_id, logger.error(textwrap.dedent(f"""
        After accepted offer to join to project with id {recipient_project_id}, recipient current
        project should be {recipient_project_id}, but equal {sender_current_project_id}
    """))

    assert len(sender_projects) == 1, logger.error(textwrap.dedent(f"""
        After accepted offer to join to project team, recipient count projects should be 1, but
        equal {len(sender_projects)} 
    """))

    assert sender_projects[0]['id'] == recipient_project_id, logger.error(textwrap.dedent(f"""
        After accepted offer to join to project team, recipient should contain project with id
        {recipient_project_id}, but it's absent 
    """))

    project_after_add_new_teammate = api.get_project(id=recipient_project_id).data

    project_team = project_after_add_new_teammate['team']

    assert len(project_team) == 1, logger.error(textwrap.dedent(f"""
        After adding new teammate with id {sender_id} to project with id {recipient_project_id},
        teammates count should be 1, but equal {len(project_team)}
    """))

    assert project_team[0]['id'] == sender_id, logger.error(textwrap.dedent(f"""
        After adding new teammate with id {sender_id} to project with id {recipient_project_id},
        this specialist is absent in project team 
    """))


def test_give_ownership():
    sender, recipient = create_specialists(count=2, projects=1)
    sender_project_id = sender['own_projects'][0]['id']
    sender_id = sender['id']
    recipient_id = recipient['id']
    data = {'recipient_id': recipient_id, 'project_id': sender_project_id}
    response_after_creation_offer = api.give_ownership(data=data, token=sender['token'])
    response_code = response_after_creation_offer.status_code

    assert response_code == HTTP_201_CREATED, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_201_CREATED}, but equal {response_code}
    """))

    offer_id = response_after_creation_offer.data['id']
    response = api.response_to_offer(id=offer_id, data={'response': True}, token=recipient['token'])
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    sender_after_accepted_offer = api.get_specialist(id=sender_id).data
    sender_own_projects = sender_after_accepted_offer['own_projects']

    assert not sender_own_projects, logger.error(textwrap.dedent(f"""
        After giving the project ownership with id {sender_project_id}, sender don't have any 
        own_projects, but its own_projects equal {sender_own_projects}
    """))

    recipient_after_accepted_offer = api.get_specialist(id=recipient_id).data
    recipient_own_projects_ids = [project['id'] for project in
                                  recipient_after_accepted_offer['own_projects']]

    assert sender_project_id in recipient_own_projects_ids, logger.error(textwrap.dedent(f"""
        Recipient after accepted offer must have project with id {sender_project_id} in your 
        list of own_projects, but him own_projects ids equal {recipient_own_projects_ids}
    """))


def test_get_ownership():
    sender, recipient = create_specialists(count=2, projects=1)
    recipient_project_id = recipient['own_projects'][0]['id']
    sender_id = sender['id']
    recipient_id = recipient['id']
    data = {'recipient_id': recipient_id, 'project_id': recipient_project_id}
    response_after_creation_offer = api.get_ownership(data=data, token=sender['token'])
    response_code = response_after_creation_offer.status_code

    assert response_code == HTTP_201_CREATED, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_201_CREATED}, but equal {response_code}
    """))

    offer_id = response_after_creation_offer.data['id']
    response = api.response_to_offer(id=offer_id, data={'response': True}, token=recipient['token'])
    response_code = response.status_code

    assert response_code == HTTP_200_OK, logger.error(textwrap.dedent(f"""
        Invalid status code, should be {HTTP_200_OK}, but equal {response_code}
    """))

    sender_after_accepted_offer = api.get_specialist(id=sender_id).data
    sender_own_projects_ids = [project['id'] for project in
                               sender_after_accepted_offer['own_projects']]

    assert recipient_project_id in sender_own_projects_ids, logger.error(textwrap.dedent(f"""
        Sender after accepted offer must have project with id {recipient_project_id} in your 
        list of own_projects, but him own_projects ids equal {sender_own_projects_ids}
    """))

    recipient_after_accepted_offer = api.get_specialist(id=recipient_id).data
    recipient_own_projects = recipient_after_accepted_offer['own_projects']

    assert not recipient_own_projects, logger.error(textwrap.dedent(f"""
        After giving the project ownership with id {recipient_project_id}, recipient don't have any 
        own_projects, but its own_projects equal {recipient_own_projects}
    """))

# TODO write negative tests for offers
