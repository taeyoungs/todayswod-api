from django.db import models
from core.models import CoreModel


class Membership(CoreModel):

    TITLE_TERM = "term"
    TITLE_COUNT = "count"

    TITLE_CHOICES = (
        (TITLE_TERM, "Term"),
        (TITLE_COUNT, "Count"),
    )

    STATE_PROGRESS = "progress"
    STATE_EXPIRED = "expired"

    STATE_CHOICES = ((STATE_PROGRESS, "Progress"), (STATE_EXPIRED, "Expired"))

    title = models.CharField(max_length=80, choices=TITLE_CHOICES)
    state = models.CharField(
        max_length=80, choices=STATE_CHOICES, default=STATE_PROGRESS
    )
    cnt = models.IntegerField(null=True, blank=True)
    start_term = models.DateField(null=True, blank=True)
    end_term = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        "users.User", related_name="memberships", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} / {self.state}"