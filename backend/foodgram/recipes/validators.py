from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class TagSlugValidator(RegexValidator):
    regex = r"^[-a-zA-Z0-9_]+$"
    message = ("Недопустимые символы в slug."
               "Допустимы только буквы, цифры и -/_")


@deconstructible
class ColorHexValidator(RegexValidator):
    regex = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    message = ("Invalid hex color code.")
