from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    is_owner = models.BooleanField(default=False)
    gender = models.CharField(max_length=10)
    box = models.ForeignKey(
        "boxes.Box",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
    )
