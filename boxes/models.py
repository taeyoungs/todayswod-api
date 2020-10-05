from django.db import models
from core.models import CoreModel


class Box(CoreModel):
    class Meta:
        verbose_name_plural = "Boxes"

    name = models.CharField(max_length=120)
    address = models.CharField(max_length=240)
    certification_code = models.IntegerField()

    def __str__(self):

        return self.name