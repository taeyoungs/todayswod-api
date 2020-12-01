from django.contrib import admin
from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):

    list_display = (
        "alert_type",
        "title",
        "content",
        "user",
        "box",
        "datetime",
    )