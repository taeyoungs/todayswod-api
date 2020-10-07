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
    content = models.CharField(max_length=120)
    box = models.ForeignKey(
        "boxes.Box", on_delete=models.CASCADE, related_name="alerts"
    )
