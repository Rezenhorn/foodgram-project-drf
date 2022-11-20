from django.core.validators import RegexValidator


class TagSlugValidator(RegexValidator):
    regex = r"^[-a-zA-Z0-9_]+$"
    message = ("Недопустимые символы в slug."
               "Допустимы только буквы, цифры и -/_")
