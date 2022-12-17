from dataclasses import dataclass

from django.urls import path

from api.views.project import (
    ProjectsListApiView,
    ProjectRetrieveApiView,
    ProjectCreationApiView,
    ProjectUpdatingApiView,
    ProjectLanguagesAddingApiView,
    ProjectLanguagesDeletionApiView,
    ProjectTechnologiesAddingApiView,
    ProjectTechnologiesDeletionApiView,
    ProjectDeletionApiView,
)
from api.views.specialist import (
    SpecialistsListApiView,
    SpecialistRetrieveApiView,
    SpecialistCreationApiView,
    SpecialistAuthenticationApiView,
    SpecialistUpdatingApiView,
    SpecialistUpdatingPasswordApiView,
    SpecialistLanguagesAddingApiView,
    SpecialistLanguagesDeletionApiView,
    SpecialistTechnologiesAddingApiView,
    SpecialistTechnologiesDeletionApiView,
    SpecialistDeletionApiView,
)
from api.views.technology import LanguagesListApiView, TechnologiesListApiView


@dataclass
class URL_PATTERN_NAME:
    LANGUAGES = 'LANGUAGES'
    TECHNOLOGIES = 'TECHNOLOGIES'

    SPECIALISTS = 'SPECIALISTS'
    RETRIEVE_SPECIALIST = 'RETRIEVE_SPECIALIST'
    CREATE_SPECIALIST = 'CREATE_SPECIALIST'
    AUTHENTICATE_SPECIALIST = 'AUTHENTICATE_SPECIALIST'
    PATCH_SPECIALIST = 'PATCH_SPECIALIST'
    CHANGE_SPECIALIST_PASSWORD = 'CHANGE_SPECIALIST_PASSWORD'
    DELETE_SPECIALIST = 'DELETE_SPECIALIST'
    ADD_LANGUAGES_TO_SPECIALIST = 'ADD_LANGUAGES_TO_SPECIALIST'
    REMOVE_SPECIALIST_LANGUAGES = 'REMOVE_SPECIALIST_LANGUAGES'
    ADD_TECHNOLOGIES_TO_SPECIALIST = 'ADD_TECHNOLOGIES_TO_SPECIALIST'
    REMOVE_SPECIALIST_TECHNOLOGIES = 'REMOVE_SPECIALIST_TECHNOLOGIES'

    PROJECTS = 'PROJECTS'
    RETRIEVE_PROJECT = 'RETRIEVE_PROJECT'
    CREATE_PROJECT = 'CREATE_PROJECT'
    UPDATE_PROJECT = 'UPDATE_PROJECT'
    DELETE_PROJECT = 'DELETE_PROJECT'
    ADD_LANGUAGES_TO_PROJECT = 'ADD_LANGUAGES_TO_PROJECT'
    REMOVE_PROJECT_LANGUAGES = 'REMOVE_PROJECT_LANGUAGES'
    ADD_TECHNOLOGIES_TO_PROJECT = 'ADD_TECHNOLOGIES_TO_PROJECT'
    REMOVE_PROJECT_TECHNOLOGIES = 'REMOVE_PROJECT_TECHNOLOGIES'


urlpatterns = [
    path('languages/', LanguagesListApiView().as_view(), name=URL_PATTERN_NAME.LANGUAGES),
    path('technologies/', TechnologiesListApiView().as_view(), name=URL_PATTERN_NAME.TECHNOLOGIES),

    path('specialists/', SpecialistsListApiView.as_view(), name=URL_PATTERN_NAME.SPECIALISTS),
    path(
        'specialists/<int:specialist_id>/',
        SpecialistRetrieveApiView.as_view(),
        name=URL_PATTERN_NAME.RETRIEVE_SPECIALIST
    ),
    path(
        'specialists/creation',
        SpecialistCreationApiView.as_view(),
        name=URL_PATTERN_NAME.CREATE_SPECIALIST
    ),
    path(
        'specialists/authentication',
        SpecialistAuthenticationApiView.as_view(),
        name=URL_PATTERN_NAME.AUTHENTICATE_SPECIALIST
    ),
    path(
        'specialists/updating',
        SpecialistUpdatingApiView.as_view(),
        name=URL_PATTERN_NAME.PATCH_SPECIALIST),
    path(
        'specialists/updating/password',
        SpecialistUpdatingPasswordApiView.as_view(),
        name=URL_PATTERN_NAME.CHANGE_SPECIALIST_PASSWORD
    ),
    path(
        'specialists/deletion',
        SpecialistDeletionApiView.as_view(),
        name=URL_PATTERN_NAME.DELETE_SPECIALIST
    ),
    path(
        'specialists/languages/adding',
        SpecialistLanguagesAddingApiView.as_view(),
        name=URL_PATTERN_NAME.ADD_LANGUAGES_TO_SPECIALIST
    ),
    path(
        'specialists/languages/deletion',
        SpecialistLanguagesDeletionApiView.as_view(),
        name=URL_PATTERN_NAME.REMOVE_SPECIALIST_LANGUAGES
    ),
    path(
        'specialists/technologies/adding',
        SpecialistTechnologiesAddingApiView.as_view(),
        name=URL_PATTERN_NAME.ADD_TECHNOLOGIES_TO_SPECIALIST
    ),
    path(
        'specialists/technologies/deletion',
        SpecialistTechnologiesDeletionApiView.as_view(),
        name=URL_PATTERN_NAME.REMOVE_SPECIALIST_TECHNOLOGIES
    ),

    path('projects/', ProjectsListApiView.as_view(), name=URL_PATTERN_NAME.PROJECTS),
    path(
        'projects/<int:project_id>/',
        ProjectRetrieveApiView.as_view(),
        name=URL_PATTERN_NAME.RETRIEVE_PROJECT
    ),
    path(
        'projects/creation',
        ProjectCreationApiView.as_view(),
        name=URL_PATTERN_NAME.CREATE_PROJECT
    ),
    path(
        'projects/<int:project_id>/updating',
        ProjectUpdatingApiView.as_view(),
        name=URL_PATTERN_NAME.UPDATE_PROJECT
    ),
    path(
        'projects/<int:project_id>/deletion',
        ProjectDeletionApiView.as_view(),
        name=URL_PATTERN_NAME.DELETE_PROJECT
    ),
    path(
        'projects/<int:project_id>/languages/adding',
        ProjectLanguagesAddingApiView.as_view(),
        name=URL_PATTERN_NAME.ADD_LANGUAGES_TO_PROJECT
    ),
    path(
        'projects/<int:project_id>/languages/deletion',
        ProjectLanguagesDeletionApiView.as_view(),
        name=URL_PATTERN_NAME.REMOVE_PROJECT_LANGUAGES
    ),
    path(
        'projects/<int:project_id>/technologies/adding',
        ProjectTechnologiesAddingApiView.as_view(),
        name=URL_PATTERN_NAME.ADD_TECHNOLOGIES_TO_PROJECT
    ),
    path(
        'projects/<int:project_id>/technologies/deletion',
        ProjectTechnologiesDeletionApiView.as_view(),
        name=URL_PATTERN_NAME.REMOVE_PROJECT_TECHNOLOGIES
    ),
]
