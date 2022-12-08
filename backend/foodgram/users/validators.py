from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.serializers import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class UsernameValidator(UnicodeUsernameValidator):
    """Prohibition to use the username 'me'."""

    def __call__(self, value):
        if value.lower() == "me":
            raise ValidationError("Username 'me' is prohibited.")
        return super().__call__(value)
