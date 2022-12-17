from rest_framework.validators import ValidationError


def validate_password(password: str, min_length: int = 8, max_length: int = 30) -> bool:
    if min_length <= len(password) <= max_length:
        return True
    raise ValidationError({
        "detail": f'password must be at least {min_length} and no more than {max_length} characters'
    })
