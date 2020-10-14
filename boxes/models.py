from django.db import models
from core.models import CoreModel


class Box(CoreModel):
    class Meta:
        verbose_name_plural = "Boxes"

    name = models.CharField(max_length=120)
    address = models.CharField(max_length=240)
    certification_code = models.IntegerField()
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="box_owner"
    )
    coach = models.ManyToManyField("users.User", related_name="box_coaches", blank=True)

    def __str__(self):

        return self.name