from dataclasses import dataclass

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from core.models import Project


@dataclass
class ERROR_MESSAGE:
    IS_PROJECT_OWNER = "you must be the project owner"


class IsProjectOwner(BasePermission):
    message = ERROR_MESSAGE.IS_PROJECT_OWNER

    def has_permission(self, request, view):
        project_id = request.parser_context['kwargs']['project_id']
        return request.user.self_projects.filter(pk=project_id).exists()
