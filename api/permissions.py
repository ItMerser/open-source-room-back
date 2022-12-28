from dataclasses import dataclass

from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from core.models import Offer, Project


@dataclass
class ERROR_MESSAGE:
    IS_PROJECT_OWNER = "you must be the project owner"
    IS_RECIPIENT = "you don't have such an offer"
    IS_NOT_RECIPIENT = "you cannot sent the offer to himself"
    SENDER_IS_PROJECT_OWNER = "you must be the project owner"
    RECIPIENT_IS_NOT_PROJECT_OWNER = "this recipient doesn't own the project"
    IS_NOT_TEAM_MEMBER = "you are the team member already"


class IsProjectOwner(BasePermission):
    message = ERROR_MESSAGE.IS_PROJECT_OWNER

    def has_permission(self, request, view):
        project_id = request.parser_context['kwargs']['project_id']
        return request.user.own_projects.filter(pk=project_id).exists()


class IsRecipient(BasePermission):
    message = ERROR_MESSAGE.IS_RECIPIENT

    def has_object_permission(self, request, view, obj):
        offer_id = request.parser_context['kwargs']['offer_id']
        try:
            offer = Offer.objects.get(pk=offer_id)
            return obj.id == offer.recipient.id
        except Offer.DoesNotExist:
            return False


class IsNotRecipient(BasePermission):
    message = ERROR_MESSAGE.IS_NOT_RECIPIENT

    def has_object_permission(self, request, view, obj):
        recipient_id = request.data['recipient_id']
        return obj.id != recipient_id


class SenderIsProjectOwner(BasePermission):
    message = ERROR_MESSAGE.SENDER_IS_PROJECT_OWNER

    def has_object_permission(self, request, view, obj):
        project_id = request.data['project_id']
        print(obj.own_projects.filter(pk=project_id))
        is_owner = obj.own_projects.filter(pk=project_id).exists()
        return is_owner


class RecipientIsProjectOwner(BasePermission):
    message = ERROR_MESSAGE.RECIPIENT_IS_NOT_PROJECT_OWNER

    def has_object_permission(self, request, view, obj):
        project_id = request.data['project_id']
        recipient_id = request.data['recipient_id']
        try:
            project = Project.objects.get(pk=project_id)
            return project.owner.id == recipient_id
        except Project.DoesNotExist:
            raise ValidationError({"detail": f"project with id {project_id} does not exist"})


class IsNotTeamMember(BasePermission):
    message = ERROR_MESSAGE.IS_NOT_TEAM_MEMBER

    def has_object_permission(self, request, view, obj):
        project_id = request.data['project_id']
        if obj.current_project:
            return obj.current_project.id != project_id
        return True
