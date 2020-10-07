from django.contrib import admin
from .models import Box


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "address",
        "certification_code",
        "owner",
    )

    filter_horizontal = ("coach",)
