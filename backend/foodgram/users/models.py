from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель юзера."""

    username = models.CharField(
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        validators=(UnicodeUsernameValidator,),
        verbose_name="Никнейм пользователя"
    )
    email = models.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name="Имейл"
    )
    first_name = models.CharField(
        max_length=settings.FIRST_NAME_MAX_LENGTH,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=settings.LAST_NAME_MAX_LENGTH,
        verbose_name="Фамилия"
    )

    REQUIRED_FIELDS = ("username", "first_name", "last_name")
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ("-id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Subscription(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(User,
                             verbose_name="Подписчик",
                             on_delete=models.CASCADE,
                             related_name="follower")
    author = models.ForeignKey(User,
                               verbose_name="Автор",
                               on_delete=models.CASCADE,
                               related_name="following")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=["user", "author"],
                                    name="unique_follow"),
            models.CheckConstraint(check=~models.Q(user=models.F("author")),
                                   name="prevent_self_follow",),
        ]

    def __str__(self):
        return f"{self.user} follows {self.author}"
