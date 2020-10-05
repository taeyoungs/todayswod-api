from django.db import models
from core.models import CoreModel


class WodSort(models.Model):

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Wod(CoreModel):

    title = models.ForeignKey("WodSort", on_delete=models.CASCADE, related_name="wods")
    content = models.TextField()
    box = models.ForeignKey("boxes.Box", on_delete=models.CASCADE, related_name="wods")
    comment = models.CharField(blank=True, max_length=120)
    time = models.IntegerField(null=True, blank=True)
    rounds = models.IntegerField(null=True, blank=True)
    rest_sec = models.IntegerField(null=True, blank=True)
    round_sec = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title.name