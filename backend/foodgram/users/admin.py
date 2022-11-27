from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Subscription, User

admin.site.unregister(Group)
admin.site.register(Subscription)


@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    search_fields = ("username",)
    list_filter = ("email", "first_name")
    empty_value_display = "-пусто-"
