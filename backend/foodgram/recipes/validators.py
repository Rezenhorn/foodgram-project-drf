from django.core.validators import RegexValidator


class TagSlugValidator(RegexValidator):
    regex = r"^[-a-zA-Z0-9_]+$"
    message = ("Недопустимые символы в slug."
               "Допустимы только буквы, цифры и -/_")


class ColorHexValidator(RegexValidator):
    regex = r"/^#([0-9A-F]{3}){1,2}$/i"
    message = ("Invalid hex color code.")
