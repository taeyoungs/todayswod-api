from django.db import models
from core.models import CoreModel


class Alert(CoreModel):

    TYPE_NOTICE = "notice"
    TYPE_EVENT = "event"
    TYPE_MESSAGE = "message"

    TYPE_CHOCIES = (
        (TYPE_NOTICE, "Notice"),
        (TYPE_EVENT, "Event"),
        (TYPE_MESSAGE, "Message"),
    )

    alert_type = models.CharField(
        max_length=20, choices=TYPE_CHOCIES, default=TYPE_NOTICE
    )
    title = models.CharField(max_length=40)
    content = models.TextField()
    datetime = models.DateTimeField()
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="alerts",
        null=True,
        blank=True,
    )
    box = models.ForeignKey(
        "boxes.Box",
        on_delete=models.CASCADE,
        related_name="alerts",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.alert_type} - {self.title}"