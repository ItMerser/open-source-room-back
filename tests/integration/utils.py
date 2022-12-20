from random import choice

from core.models.choices import Direction, ProjectType
from tests.integration.api import api
from tests.integration.config import fake


def generate_creation_specialist_data(**kwargs) -> dict:
    nickname = fake.user_name()
    return {
        'nickname': nickname,
        'github_nickname': nickname,
        'password': fake.password(),
        'direction': choice(Direction.values),
        'email': fake.email(),
        'born_date': fake.date(),
        'name': fake.first_name(),
        'surname': fake.last_name(),
        'country': fake.country(),
        'city': fake.city(),
        **kwargs,
    }


def generate_updating_specialist_data(**kwargs) -> dict:
    return {
        'nickname': fake.user_name(),
        'github_nickname': fake.user_name(),
        'direction': choice(Direction.values),
        'email': fake.email(),
        'born_date': fake.date(),
        'name': fake.first_name(),
        'surname': fake.last_name(),
        'country': fake.country(),
        'city': fake.city(),
        **kwargs,
    }


def generate_project_data(**kwargs) -> dict:
    project_name = fake.project()
    return {
        'name': project_name,
        'github_name': project_name,
        'description': fake.sentence(),
        'version': '1.0',
        'type': choice(ProjectType.values),
        'is_private': False,
        'github': fake.url(),
        **kwargs,
    }


def add_projects_to_specialist(token: str, projects: int = 1, private_projects: int = 0) -> None:
    while projects:
        project_creation_data = generate_project_data()
        api.create_project(data=project_creation_data, token=token)
        projects -= 1
    while private_projects:
        project_creation_data = generate_project_data(is_private=True)
        api.create_project(data=project_creation_data, token=token)
        private_projects -= 1


def create_specialists(count: int = 1, projects: int = 0, private_projects: int = 0) -> list[dict]:
    specialists = []
    while count:
        specialist_creation_data = generate_creation_specialist_data()
        specialist = api.create_specialist(data=specialist_creation_data).data
        auth_token = specialist['token']
        add_projects_to_specialist(
            token=auth_token,
            projects=projects,
            private_projects=private_projects
        )

        retrieved_specialist = api.get_specialist(id=specialist['id']).data
        retrieved_specialist['token'] = auth_token
        specialists.append(retrieved_specialist)
        count -= 1
    return specialists
