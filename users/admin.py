from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = UserAdmin.list_display + (
        "gender",
        "box",
        "has_new_alert",
        "registration_state",
        "certification_number",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "gender",
                    "box",
                    "has_new_alert",
                    "registration_state",
                    "certification_number",
                ),
            },
        ),
    )
