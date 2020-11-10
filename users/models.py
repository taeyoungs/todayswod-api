from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    STATE_UNREGISTERED = "unregistered"
    STATE_PENDING = "pending"
    STATE_REGISTERED = "registered"

    STATE_CHOICES = (
        (STATE_UNREGISTERED, "Unregistered"),
        (STATE_PENDING, "Pending"),
        (STATE_REGISTERED, "Registered"),
    )

    gender = models.CharField(max_length=10)
    box = models.ForeignKey(
        "boxes.Box",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
    )
    has_new_alert = models.BooleanField(default=False)
    registration_state = models.CharField(
        max_length=40, choices=STATE_CHOICES, default=STATE_UNREGISTERED
    )
    certification_number = models.IntegerField(blank=True, null=True)
