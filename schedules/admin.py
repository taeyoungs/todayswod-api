from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):

    list_display = (
        "start_time",
        "end_time",
        "user_limit",
        "box",
        "coach",
    )
