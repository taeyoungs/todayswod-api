from django.db import models
from core.models import CoreModel


class Reservation(CoreModel):

    STATE_CONFIRMED = "confirmed"
    STATE_CANCELED = "canceled"
    STATE_PENDING = "pending"

    STATE_CHOICES = (
        (STATE_PENDING, "Pending"),
        (STATE_CONFIRMED, "Confirmed"),
        (STATE_CANCELED, "Canceled"),
    )

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="reservations"
    )
    state = models.CharField(
        max_length=20, default=STATE_PENDING, choices=STATE_CHOICES
    )
    schedule = models.ForeignKey(
        "schedules.Schedule", on_delete=models.CASCADE, related_name="reservations"
    )
