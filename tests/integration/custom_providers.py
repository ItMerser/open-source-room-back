from random import choice

from faker.providers import BaseProvider


class ProjectProvider(BaseProvider):
    projects = (
        'react',
        'polygon',
        'zeus',
        'world map',
        'divider',
        'defender',
        'tracker',
        'cs go',
        'dota2',
        'memory keeper',
        'world web',
        'cast',
        'closure room',
        'shell',
    )

    def project(self):
        return choice(self.projects)
