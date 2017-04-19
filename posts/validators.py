from django.core.exceptions import ValidationError


def validate_user(user, request_user):
    if user != request_user:
        raise ValidationError('''''')
