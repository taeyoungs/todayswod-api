from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    gender = models.CharField(max_length=10)
    box = models.ForeignKey(
        "boxes.Box",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
    )
    has_new_alert = models.BooleanField(default=False)
