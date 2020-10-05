from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = UserAdmin.list_display + (
        "gender",
        "box",
        "is_owner",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "is_owner",
                    "gender",
                    "box",
                ),
            },
        ),
    )
