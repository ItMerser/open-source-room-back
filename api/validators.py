from rest_framework.validators import ValidationError

from core.models import Project, Specialist


def validate_password(password: str, min_length: int = 8, max_length: int = 30) -> bool:
    if min_length <= len(password) <= max_length:
        return True
    raise ValidationError({
        "detail": f'password must be at least {min_length} and no more than {max_length} characters'
    })


def validate_offer_creation_data(data: dict) -> None:
    project_id, recipient_id = data.get('project_id'), data.get('recipient_id')
    if type(project_id) is not int:
        raise ValidationError({"detail": "invalid required param project_id, it must be int"})
    if type(recipient_id) is not int:
        raise ValidationError({"detail": "invalid required param recipient_id, it must be int"})

    project = Project.objects.filter(pk=project_id).exists()
    if project is False:
        raise ValidationError({"detail": f"project with id {project_id} doesn't exist"})
    recipient = Specialist.objects.filter(pk=recipient_id).exists()
    if recipient is False:
        raise ValidationError({"detail": f"recipient with id {recipient_id} doesn't exist"})


def validate_offer_response_data(data: dict) -> None:
    response = data.get('response')
    if type(response) is not bool:
        raise ValidationError({"detail": "invalid required param response, it must be bool"})
