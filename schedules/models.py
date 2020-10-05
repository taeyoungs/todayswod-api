from django.db import models
from core.models import CoreModel


class Schedule(CoreModel):

    time = models.TimeField()
    user_limit = models.IntegerField()
    box = models.ForeignKey(
        "boxes.Box", on_delete=models.CASCADE, related_name="schedules"
    )
    coach = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="schedules"
    )