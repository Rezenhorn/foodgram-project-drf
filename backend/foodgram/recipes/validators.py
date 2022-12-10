from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class TagSlugValidator(RegexValidator):
    regex = r"^[-a-zA-Z0-9_]+$"
    message = ("Invalid slug."
               "This value may contain only English letters, digits and -/_")


@deconstructible
class ColorHexValidator(RegexValidator):
    regex = r"^#([A-Fa-f0-9]){3,6}$"
    message = ("Invalid hex color code. ")
