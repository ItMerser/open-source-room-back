import logging

from faker import Faker

from tests.integration.custom_providers import ProjectProvider

logger = logging.getLogger(__name__)

fake = Faker()
fake.add_provider(ProjectProvider)
