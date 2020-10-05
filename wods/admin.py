from django.contrib import admin
from . import models


@admin.register(models.WodSort)
class WodSortAdmin(admin.ModelAdmin):

    pass


@admin.register(models.Wod)
class WodAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "box",
        "time",
        "rounds",
        "rest_sec",
        "round_sec",
    )
