from django.urls import reverse
from rest_framework.test import APIClient

from api.urls import URL_PATTERN_NAME


class API:
    client = APIClient()

    # TECHNOLOGIES API
    def get_languages(self):
        return self.client.get(reverse(URL_PATTERN_NAME.LANGUAGES))

    def get_technologies(self):
        return self.client.get(reverse(URL_PATTERN_NAME.TECHNOLOGIES))

    # SPECIALIST API
    def get_specialists(self):
        return self.client.get(reverse(URL_PATTERN_NAME.SPECIALISTS))

    def get_specialist(self, id: int):
        return self.client.get(reverse(
            URL_PATTERN_NAME.RETRIEVE_SPECIALIST,
            kwargs={'specialist_id': id}
        ))

    def create_specialist(self, data: dict):
        return self.client.post(reverse(URL_PATTERN_NAME.CREATE_SPECIALIST), data=data)

    def authenticate_specialist(self, data: dict):
        return self.client.post(reverse(URL_PATTERN_NAME.AUTHENTICATE_SPECIALIST), data=data)

    def update_specialist(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(reverse(URL_PATTERN_NAME.PATCH_SPECIALIST), data=data)

    def change_specialist_password(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(reverse(URL_PATTERN_NAME.CHANGE_SPECIALIST_PASSWORD), data=data)

    def delete_specialist(self, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.delete(reverse(URL_PATTERN_NAME.DELETE_SPECIALIST))

    def add_languages_to_specialist(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.ADD_LANGUAGES_TO_SPECIALIST),
            data=data
        )

    def remove_specialist_languages(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.REMOVE_SPECIALIST_LANGUAGES),
            data=data
        )

    def add_technologies_to_specialist(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.ADD_TECHNOLOGIES_TO_SPECIALIST),
            data=data
        )

    def remove_specialist_technologies(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.REMOVE_SPECIALIST_TECHNOLOGIES),
            data=data
        )

    # PROJECT API
    def get_projects(self):
        return self.client.get(reverse(URL_PATTERN_NAME.PROJECTS))

    def get_project(self, id: int):
        return self.client.get(reverse(
            URL_PATTERN_NAME.RETRIEVE_PROJECT,
            kwargs={'project_id': id}
        ))

    def create_project(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.post(reverse(URL_PATTERN_NAME.CREATE_PROJECT), data=data)

    def update_project(self, id: int, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.UPDATE_PROJECT, kwargs={'project_id': id}),
            data=data
        )

    def delete_project(self, id: int, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.delete(reverse(
            URL_PATTERN_NAME.DELETE_PROJECT,
            kwargs={'project_id': id}
        ))

    def add_languages_to_project(self, id: int, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.ADD_LANGUAGES_TO_PROJECT, kwargs={'project_id': id}),
            data=data
        )

    def remove_project_languages(self, id: int, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.REMOVE_PROJECT_LANGUAGES, kwargs={'project_id': id}),
            data=data
        )

    def add_technologies_to_project(self, id: int, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.ADD_TECHNOLOGIES_TO_PROJECT, kwargs={'project_id': id}),
            data=data
        )

    def remove_project_technologies(self, id: int, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.REMOVE_PROJECT_TECHNOLOGIES, kwargs={'project_id': id}),
            data=data
        )

    # OFFER API
    def add_to_team(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.post(reverse(URL_PATTERN_NAME.ADD_TO_TEAM), data=data)

    def join_to_team(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.post(reverse(URL_PATTERN_NAME.JOIN_TO_TEAM), data=data)

    def give_ownership(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.post(reverse(URL_PATTERN_NAME.GIVE_OWNERSHIP), data=data)

    def get_ownership(self, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.post(reverse(URL_PATTERN_NAME.GET_OWNERSHIP), data=data)

    def response_to_offer(self, id: int, data: dict, token: str):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return self.client.patch(
            reverse(URL_PATTERN_NAME.RESPONSE_TO_OFFER, kwargs={'offer_id': id}),
            data=data
        )


api = API()
