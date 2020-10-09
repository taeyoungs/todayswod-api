from django.db import models
from core.models import CoreModel


class Schedule(CoreModel):

    start_time = models.TimeField()
    end_time = models.TimeField()
    user_limit = models.IntegerField()
    box = models.ForeignKey(
        "boxes.Box", on_delete=models.CASCADE, related_name="schedules"
    )
    coach = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="schedules"
    )

    def __str__(self):
        # print(self.reservations)
        return f"{self.start_time} ~ {self.end_time}"